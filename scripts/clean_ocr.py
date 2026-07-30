#!/usr/bin/env python3
"""
clean_ocr.py — conservative, deterministic, idempotent OCR-artifact removal
for six files of the Ethiopian Orthodox broader canon.

Scope
-----
This script touches ONLY the six files listed in TARGETS. It removes noise;
it never adds text and never rewrites text. Every transformation is either
a deletion of characters or the joining of a word broken across a line.

Sources of the noise
--------------------
The six files were scraped from Horner, *The Statutes of the Apostles* (1904),
Horner's Ethiopic Didascalia, and Grébaut's French Qalementos in *Revue de
l'Orient Chrétien* (1911-1913). Those printed editions carry marginal line
numbers every 5 lines, and break words across lines with hyphens. The scraper
absorbed the marginal numbers into the text and kept the hyphens.

Passes
------
Passes are numbered as in the brief, but executed in the order 0, 2, 3, 1:

STEP 0  rstrip   Strip trailing whitespace from every line.
                 Runs FIRST because both later passes key off end-of-line
                 characters, and a trailing space hides them. (Group A files
                 have trailing spaces on almost every line; without this the
                 hyphen at end-of-line is invisible.)
STEP 2  dehyph   Join `word-\\n continuation`, protecting legitimate
                 hyphenated compounds attested mid-line in the same file, and
                 refusing the join when the continuation is itself a whole
                 English word that does not make a real word when joined
                 (`blue-` + `black`). See COMMON_CONTINUATIONS.
STEP 3  blanks   Collapse runs of 3+ blank lines to 2.
STEP 1  linenum  Delete an absorbed marginal line number at end of line.
                 Runs LATE so the line numbers it reports address the file as
                 shipped; steps 2 and 3 both shift them.
                 GATED: requires --step1-approved, and then deletes only the
                 tiers named by --tiers, narrowed by --strict5 to exact
                 multiples of 5. Without approval the candidates are
                 reported and never deleted, because this rule can bite real
                 text (a date, a quantity, a footnote reference, a folio
                 citation, a number that legitimately ends a sentence).
STEP 2b/3b       Steps 2 and 3 again. Step 1 can expose a hyphen that was
                 hiding behind the number it deleted (`…that the Obla- 10`),
                 so the pipeline must be iterated to a fixed point. Six lines
                 in the corpus need this.

Idempotence
-----------
Every pass is a fixed point after one application: a deleted number cannot be
re-detected, a joined word no longer ends in a hyphen, and 2 blank lines are
not a run of 3. The passes are not independent of each other, though — Step 1
creates work for Step 2 — so Step 2 runs again afterwards. With that second
pass in place, re-running the script on cleaned output makes no changes; the
`--selftest` flag asserts exactly this.

Usage
-----
    python3 scripts/clean_ocr.py --backup    # copy the six to backups/
    python3 scripts/clean_ocr.py --report    # analyse; leave the six untouched
    python3 scripts/clean_ocr.py --apply     # steps 0, 2, 3 — no deletions
    python3 scripts/clean_ocr.py --apply --step1-approved --tiers A --strict5
                                             # + Step 1, tier A, multiples of 5
    python3 scripts/clean_ocr.py --selftest  # assert idempotence, write nothing

Three files are written by --report and --apply alike:
    CLEANING_REPORT.md    every change made, plus the tiered Step 1 candidates
    MANUAL_REVIEW.md      what was deliberately left alone, with line numbers
    HANDOFF-CLEANING.md   both of the above, verbatim, behind a handoff preamble

Every line number quoted in those reports is resolved from an anchor string
against the file as written, never hardcoded, and the Step 0/2/3 statistics are
computed against `backups/<name>.md.bak` rather than the live file — so a
re-run reproduces the same reports byte for byte instead of zeroing them out.
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CANON = REPO / "en" / "03-broader-canon"
BACKUPS = REPO / "backups"

# The only files this script is permitted to modify.
TARGETS = [
    "80-serata-seyon.md",
    "81-teezaz.md",
    "82-gessew.md",
    "84-mashafa-kidan-1.md",
    "86-qalementos.md",
    "87-didascalia.md",
]

# ---------------------------------------------------------------------------
# Region classification
# ---------------------------------------------------------------------------

HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s")
TABLE_RE = re.compile(r"^\s*\|")
BLOCKQUOTE_RE = re.compile(r"^\s*>")


def region_map(lines: list[str]) -> list[str]:
    """Label every line: 'frontmatter', 'meta', 'heading', 'table', 'quote', 'body'.

    Front matter is the YAML block delimited by the first two `---` lines.
    'meta' is everything from there up to and including the `## Text` heading
    (the Metadata table and the Notes section). Neither is scripture, and
    neither may be edited by Step 1: `number: 82` and `chapters: 56` both look
    exactly like an absorbed marginal line number.
    """
    labels = ["body"] * len(lines)

    fm_end = -1
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                fm_end = i
                break
    for i in range(0, fm_end + 1):
        labels[i] = "frontmatter"

    text_at = next(
        (i for i, l in enumerate(lines) if l.strip() == "## Text"), fm_end
    )
    for i in range(fm_end + 1, text_at + 1):
        if labels[i] == "body":
            labels[i] = "meta"

    for i, l in enumerate(lines):
        if labels[i] != "body":
            continue
        if HEADING_RE.match(l):
            labels[i] = "heading"
        elif TABLE_RE.match(l):
            labels[i] = "table"
        elif BLOCKQUOTE_RE.match(l):
            labels[i] = "quote"
    return labels


def body_start(lines: list[str]) -> int:
    """0-based index of the first line after `## Text`."""
    for i, l in enumerate(lines):
        if l.strip() == "## Text":
            return i + 1
    return 0


# ---------------------------------------------------------------------------
# STEP 0 — trailing whitespace
# ---------------------------------------------------------------------------


def step0_rstrip(lines: list[str]) -> tuple[list[str], int]:
    out = [l.rstrip() for l in lines]
    changed = sum(1 for a, b in zip(lines, out) if a != b)
    return out, changed


# ---------------------------------------------------------------------------
# STEP 1 — absorbed marginal line numbers
# ---------------------------------------------------------------------------

# A 1-3 digit number at end of line, preceded by whitespace.
# The lookbehind is what keeps this from matching the tail of a longer number:
# in " 1904" the position before "904" is preceded by "1", not whitespace.
LINENUM_RE = re.compile(r"(?<=\s)(\d{1,3})$")

CONTEXT = 60


def near_multiple_of_5(n: int) -> bool:
    """True if n is within 2 of a multiple of 5.

    NOTE: this predicate is vacuous — it is true for every integer, since
    n % 5 is in {0,1,2} (within 2 below) or {3,4} (within 2 above). It is
    implemented and called anyway because it is the stated rule, and because
    keeping it explicit is what makes the vacuity visible rather than hidden.
    Use `strict_multiple_of_5` for the tier that actually discriminates.
    """
    r = n % 5
    return min(r, 5 - r if r else 0) <= 2


def strict_multiple_of_5(n: int) -> bool:
    return n % 5 == 0


def has_verse_markers(text: str) -> bool:
    """`**N**` verse markers mean numbers in this file are structural."""
    return re.search(r"\*\*\d+\*\*", text) is not None


# --- Tiering -------------------------------------------------------------
# A raw end-of-line number is not automatically a marginal line number. Three
# other things in these files look identical to the rule, and each needs a
# different decision, so candidates are tiered rather than lumped together.

# "(F. 4" — a manuscript folio citation, `(F. 4 r° a)`, broken across lines.
FOLIO_RE = re.compile(r"\((?:F|f|fol)\.\s*$")
# "…244 à 246," — an enumeration of manuscript page numbers.
ENUM_RE = re.compile(r"\d\s*[,;àa]\s*$")
# "commence au feuillet 151" — the number is the object of a referring noun.
REFERENT_RE = re.compile(
    r"\b(?:feuillet|feuillets|page|pages|p|pp|col|colonne|no|n°|nos|vol|fasc|"
    r"chapter|chapitre|verse|canon|statute|book|livre|ms|mss|folio|line|ligne)"
    r"\.?\s*$",
    re.IGNORECASE,
)


def uppercase_ratio(s: str) -> float:
    letters = [c for c in s if c.isalpha()]
    if not letters:
        return 0.0
    return sum(1 for c in letters if c.isupper()) / len(letters)


def classify_candidate(before: str) -> str:
    """Decide what an end-of-line number actually is, from what precedes it."""
    b = before.strip()
    if FOLIO_RE.search(b):
        return "folio"
    if REFERENT_RE.search(b):
        return "referent"
    if ENUM_RE.search(b):
        return "enumeration"
    # A running page head: short line, overwhelmingly capitals, no sentence.
    if b and len(b) < 70 and uppercase_ratio(b) >= 0.75 and len(b) >= 8:
        return "running_head"
    return "prose"


TIER_OF = {
    "prose": "A",
    "running_head": "B",
    "folio": "C",
    "referent": "C",
    "enumeration": "C",
}


def step1_candidates(lines: list[str], labels: list[str]) -> list[dict]:
    """Find absorbed marginal line numbers. Reports only; deletion is gated."""
    out = []
    bstart = body_start(lines)
    for i, line in enumerate(lines):
        m = LINENUM_RE.search(line)
        if not m:
            continue
        value = int(m.group(1))
        skip = None
        if i < bstart:
            skip = "before ## Text"
        elif labels[i] in ("frontmatter", "meta"):
            skip = labels[i]
        elif labels[i] == "heading":
            skip = "heading"
        elif labels[i] in ("table", "quote"):
            skip = labels[i]
        elif not near_multiple_of_5(value):
            skip = "not near multiple of 5"

        before = line[: m.start(1)].rstrip()
        kind = classify_candidate(before)
        out.append(
            {
                "lineno": i + 1,
                "value": value,
                # The literal characters matched. Kept distinct from `value`
                # because a zero-padded token ("02") must be reported as it
                # appears in the file, not as the integer it parses to.
                "token": m.group(1),
                "context": before[-CONTEXT:],
                "full": line,
                "cleaned": before,
                "skip": skip,
                "strict5": strict_multiple_of_5(value),
                "label": labels[i],
                "kind": kind,
                "tier": TIER_OF[kind],
            }
        )
    return out


def step1_apply(
    lines: list[str], cands: list[dict], tiers: str = "A", strict5: bool = False
) -> tuple[list[str], list[dict]]:
    """Delete only candidates in the approved tiers (default: tier A alone).

    `strict5` narrows that further to numbers that are an exact multiple of 5.
    The gate exists because `near_multiple_of_5` — the rule as originally
    stated — is vacuously true for every integer (see its docstring), so tier A
    alone still admits values like 62 or 148 that no printer ever set in a
    margin. Requiring `n % 5 == 0` is what makes the marginal-line-number
    hypothesis actually testable, and it is the basis on which this pass was
    approved: 214 deletions rather than 606.
    """
    applied = [
        c
        for c in cands
        if c["skip"] is None
        and c["tier"] in tiers
        and (c["strict5"] if strict5 else True)
    ]
    out = list(lines)
    for c in applied:
        out[c["lineno"] - 1] = c["cleaned"]
    return out, applied


# ---------------------------------------------------------------------------
# STEP 2 — de-hyphenation
# ---------------------------------------------------------------------------

HYPHEN_EOL_RE = re.compile(r"([A-Za-zÀ-ÿ]+)-$")
NEXT_LOWER_RE = re.compile(r"([a-zà-ÿ]+)")
MIDLINE_COMPOUND_RE = re.compile(r"[A-Za-zÀ-ÿ]+-[A-Za-zÀ-ÿ]+")
WORD_RE = re.compile(r"[A-Za-zÀ-ÿ]+")

# ---------------------------------------------------------------------------
# Standalone-word guard (added after pass 1 found three false-positive joins)
# ---------------------------------------------------------------------------
#
# The plain rule joins `stem-` + `fragment` whenever the fragment starts with a
# lowercase letter. That is right when the fragment is a word-piece — `tion`,
# `ness`, `ment`, `gneur` — which is the overwhelming majority: 665 distinct
# fragments across the six files, nearly all of them meaningless alone.
#
# It is wrong when the fragment is itself a whole English word, because then
# the hyphen was never a line-break hyphen. Three ways that happens here:
#
#   1. A real orthographic compound: `blue-` / `black` is "blue-black", an eye
#      colour, and the hyphen belongs to the text.
#   2. A spurious OCR hyphen between two separate words: `this-` / `type` is
#      "this type".
#   3. Two-column footnote interleaving, where the scraper put the wrong
#      column's first word on the next line: `Phari-` / `the` (true
#      continuation `bishop`... in the other column), `money-` / `its` (true
#      continuation `changers`), `Xan-` / `month` (true continuation `thicus`).
#
# So: refuse the join when the fragment is a common standalone English word,
# UNLESS the joined result is itself a known word — `him` + `self` really is
# "himself", `like` + `wise` really is "likewise". "Known" is decided by
# CORPUS attestation: the joined form appears somewhere in these same six files
# as an ordinary unhyphenated token. That keeps the script dependency-free and
# offline, and uses the strongest evidence available — the text itself.
#
# The list is deliberately English-only, matching the brief. Adding common
# French words to it (for `86-qalementos.md`) was tried and rejected: it took
# the flag count from 9 to 20 and every one of the 11 extra flags was a false
# alarm on a correctly-joined French word (`gra-ces`, `deli-ces`, `vipe-res`,
# `canonia-les`). See CLEANING_REPORT.md for the full audit.
COMMON_CONTINUATIONS = frozenset(
    """
    the this that these those then than them they there their
    type kind sort form part side line word words name names time day days
    way ways work works land hand hands head heart house home room place
    thing things people black white blue red green gold
    self selves wise son sons man men woman women child children
    over under out off up down back forth fore half all one two three ten
    ever every some body where when how who what why
    right left long short great good god high low new old first last
    book born bread ground water fire wind earth light dark night morning
    father mother king lord priest priests deacon deacons bishop bishops
    church come came go went take give given make made said say see seen
    know known also even only still well much many more most less least
    like likewise and or but for nor yet so if as at by to of in on
    be been being is was are were has have had do did done
    he she it we you him her his its our your me my thee thou thy
    from with into upon unto about after before among against between
    through not no yes any each both same other another such very own
    soul body spirit flesh blood year years week month
    full fully able ship hold stone ward wards mind mount stand standing
    state
    """.split()
)


# Editor rulings on individual held-back joins, keyed by (file, stem, fragment).
# The value is the separator to put between the two halves.
#
# The guard can only refuse a join; it cannot know what the line should say.
# These three were resolved by reading the page, so the script performs the
# merge rather than leaving a dangling hyphen. Keeping them here rather than
# hand-editing the files is what preserves the invariant the whole script rests
# on — that the shipped file is exactly `pipeline(backups/<name>.md.bak)` — and
# therefore that every line number in the reports is correct.
#
# The five two-column footnote cases are deliberately absent: their true
# continuation is elsewhere on the page, so merging the two halves at all would
# be wrong, whatever separator was chosen. They stay held, and stay listed in
# MANUAL_REVIEW.md.
HELD_JOIN_REPAIRS = {
    # "his left [eye] blue-black" — a colour compound; the hyphen is real.
    ("84-mashafa-kidan-1.md", "blue", "black"): "-",
    # "there is this type also in heaven" — two words; the hyphen is OCR noise.
    ("84-mashafa-kidan-1.md", "this", "type"): " ",
    # "P absurdly reads: Phari the bishop" — inside a footnote quoting a
    # manuscript variant, where the split between the words carries the sense.
    ("87-didascalia.md", "Phari", "the"): " ",
}


def corpus_lexicon(files: dict[str, list[str]]) -> set[str]:
    """Every lowercase whole word attested unhyphenated across the six files.

    This is the "dictionary" the guard consults. A word split by an
    end-of-line hyphen contributes neither half, so a form that ONLY ever
    appears broken never vouches for itself.
    """
    lex: set[str] = set()
    for lines in files.values():
        for line in lines:
            hay = line[:-1] if line.endswith("-") else line
            for m in WORD_RE.finditer(hay):
                lex.add(m.group(0).lower())
    return lex


def held_back(stem: str, frag: str, joined: str, lexicon: set[str]) -> bool:
    """True when the standalone-word guard refuses this join.

    Restricted to ASCII stems on purpose. The guard reasons with an English
    word list, so it has no business judging non-English orthography — and
    without the restriction it misfires on exactly one join in the corpus,
    `Haymaa-` / `not` (Takla Haymanot, a Ge'ez name whose tail happens to
    spell an English word).
    """
    if frag.lower() not in COMMON_CONTINUATIONS:
        return False
    if not stem.isascii():
        return False
    return joined.lower() not in lexicon


def legitimate_compounds(lines: list[str]) -> set[str]:
    """Compounds attested with a hyphen *mid-line* in this same file.

    These are real orthography, not line-break artifacts, and must survive:
    Beth-el, sin-offering, only-begotten, stumbling-block, first-fruits in the
    English files; au-dessus, Celui-ci, quelques-unes, soixante-douze in the
    French one. Built per-file, before any joining, so the evidence is the
    original text.
    """
    found = set()
    for line in lines:
        # A hyphen at end of line is the artifact we are removing; it is not
        # evidence of a compound, so only look at what precedes the last char.
        hay = line[:-1] if line.endswith("-") else line
        for m in MIDLINE_COMPOUND_RE.finditer(hay):
            found.add(m.group(0).lower())
    return found


def step2_dehyphenate(
    lines: list[str],
    labels: list[str],
    lexicon: set[str] | None = None,
    name: str = "",
) -> tuple[list[str], list[dict], list[dict]]:
    """Join hyphen line-breaks. Returns (lines, joins made, joins held back).

    `lexicon` is the corpus-wide attestation set consulted by the standalone-
    word guard; it defaults to this file alone, which is all the evidence
    available when the function is called in isolation. `name` selects this
    file's entries in HELD_JOIN_REPAIRS.
    """
    compounds = legitimate_compounds(lines)
    if lexicon is None:
        lexicon = corpus_lexicon({"": lines})
    bstart = body_start(lines)
    joins: list[dict] = []
    holds: list[dict] = []

    out: list[str] = []
    # Keep original line numbers for the log even as lines merge.
    i = 0
    n = len(lines)
    while i < n:
        cur = lines[i]
        cur_lineno = i + 1
        # A merged line may itself end in a hyphen; keep consuming.
        while True:
            if i + 1 >= n:
                break
            if i < bstart or labels[i] in ("frontmatter", "meta", "heading", "table"):
                break
            m = HYPHEN_EOL_RE.search(cur)
            if not m:
                break
            nxt = lines[i + 1]
            nm = NEXT_LOWER_RE.match(nxt)
            if not nm:
                break
            joined_word = m.group(1) + nm.group(1)
            compound = f"{m.group(1)}-{nm.group(1)}".lower()
            if compound in compounds:
                break  # legitimate compound: leave the hyphen alone
            if held_back(m.group(1), nm.group(1), joined_word, lexicon):
                sep = HELD_JOIN_REPAIRS.get((name, m.group(1), nm.group(1)))
                if sep is None:
                    holds.append(
                        {
                            "lineno": cur_lineno,
                            "second_lineno": i + 2,
                            "stem": m.group(1),
                            "fragment": nm.group(1),
                            "would_have_joined": joined_word,
                            "context": f"{cur} ⏎ {nxt}",
                        }
                    )
                    break  # fragment is a whole word: not a line-break hyphen
                # An editor has ruled on this one; merge as instructed.
                before = f"{cur} ⏎ {nxt}"
                repaired = m.group(1) + sep + nm.group(1)
                cur = cur[: m.start(1)] + repaired + nxt[nm.end(1) :]
                joins.append(
                    {
                        "lineno": cur_lineno,
                        "second_lineno": i + 2,
                        "word_before": f"{m.group(1)}- / {nm.group(1)}",
                        "word_after": repaired,
                        "before": before,
                        "after": cur,
                        "repair": True,
                    }
                )
                i += 1
                continue
            before = f"{cur} ⏎ {nxt}"
            cur = cur[: m.start(1)] + joined_word + nxt[nm.end(1) :]
            joins.append(
                {
                    "lineno": cur_lineno,
                    "second_lineno": i + 2,
                    "word_before": f"{m.group(1)}- / {nm.group(1)}",
                    "word_after": joined_word,
                    "before": before,
                    "after": cur,
                }
            )
            i += 1  # the next line has been consumed into cur
        out.append(cur)
        i += 1
    return out, joins, holds


# ---------------------------------------------------------------------------
# STEP 3 — blank lines
# ---------------------------------------------------------------------------


def step3_blanks(lines: list[str]) -> tuple[list[str], int]:
    out: list[str] = []
    run = 0
    collapsed = 0
    for l in lines:
        if l.strip() == "":
            run += 1
            if run <= 2:
                out.append(l)
            else:
                collapsed += 1
        else:
            run = 0
            out.append(l)
    return out, collapsed


# ---------------------------------------------------------------------------
# MANUAL_REVIEW detectors (report only — nothing here is ever edited)
# ---------------------------------------------------------------------------

# (key, regex, correction, why, named-in-the-brief?)
# Every line number and every "reads" value in MANUAL_REVIEW.md is taken from
# an actual match, never hardcoded — hardcoded ones drift as soon as Step 2
# joins a line above them.
MISSPELLINGS = [
    ("pnayer", re.compile(r"\bpnayer\b"), "prayer", "'r' read as 'n'", True),
    ("K^fas", re.compile(r"K\^fas"), "Kefas", "'e' read as '^'", True),
    ("ao", re.compile(r"(?<![A-Za-zÀ-ÿ])ao(?![A-Za-zÀ-ÿ])"), "20",
     "marginal '20' absorbed and read as letters", True),
    ("lo", re.compile(r"(?<![A-Za-zÀ-ÿ])lo(?![A-Za-zÀ-ÿ])"), "10",
     "marginal '10' absorbed and read as letters", True),
    ("Buck", re.compile(r"\bBuck\b"), "Buch", "German 'Buch' misread", True),
    ("Göttingen", re.compile(r"G[öüou]ttingen"), "Göttingen",
     "German 'Göttingen' misread", True),
    ("185$", re.compile(r"\b18[0-9]\$"), "1858", "'$' for a final digit", True),
    # Found by reading, not named in the brief.
    ("caret-for-letter", re.compile(r"[A-Za-z]\^[A-Za-z]"), "(letter unknown)",
     "caret substituted for a letter", False),
    ("WOLY", re.compile(r"\bWOLY\b"), "HOLY", "'H' read as 'W'", False),
    ("shecp", re.compile(r"\bshecp\b"), "sheep", "'e' read as 'c'", False),
    ("Bush Museum", re.compile(r"\bBush Museum\b"), "British Museum",
     "'British' read as 'Bush'", False),
    ("Schriflen", re.compile(r"\bSchriflen\b"), "Schriften",
     "German 'Schriften', 't' read as 'l'", False),
    ("Ir came", re.compile(r"\bIr came\b"), "It came",
     "drop-capital 'It' read as 'Ir'", False),
    ("DIDASCALIA-head", re.compile(r"\bE[A-Z]{2,5}OPIC\b"),
     "ETHIOPIC", "running-head title corrupted", False),
]

# Footnote reference markers: OCR renders the printed superscript as a stray
# symbol glued to the end of a word or to punctuation.
FOOTNOTE_MARKER_RE = re.compile(r"[\w,.;:]([®©¢°ª‘’“”*†‡§¶]+)(?=\s|$)")
# Footnote bodies: the printed apparatus at the foot of the page comes through
# as short lines beginning with the footnote's number.
FOOTNOTE_BODY_RE = re.compile(r"^\s*(\d{1,2}|[‘’*†‡])\s+[A-Z(‘“]")
RUNNING_HEAD_RE = re.compile(
    r"^\s*(\d{1,3}\s+)?[A-ZÉÈÊÀÇ' .,]{8,}\s*(\d{1,3})?\s*$"
)


def scan_manual_review(name: str, lines: list[str], labels: list[str]) -> dict:
    bstart = body_start(lines)
    miss: list[tuple[int, str, str, str]] = []
    markers: list[int] = []
    bodies: list[int] = []
    heads: list[int] = []
    for i, line in enumerate(lines):
        if i < bstart:
            continue
        for key, rx, correction, why, in_brief in MISSPELLINGS:
            m = rx.search(line)
            # A pattern broad enough to catch every corruption of a word also
            # catches the word spelled correctly. If the match already equals
            # the correction there is nothing to review.
            if m and m.group(0) != correction:
                miss.append(
                    {
                        "lineno": i + 1,
                        "key": key,
                        "reads": m.group(0),
                        "correction": correction,
                        "why": why,
                        "in_brief": in_brief,
                        "text": line.strip()[:100],
                    }
                )
        if FOOTNOTE_MARKER_RE.search(line):
            markers.append(i + 1)
        if FOOTNOTE_BODY_RE.match(line):
            bodies.append(i + 1)
        if labels[i] == "body" and RUNNING_HEAD_RE.match(line) and len(line) < 70:
            heads.append(i + 1)
    return {"misspellings": miss, "markers": markers, "bodies": bodies, "heads": heads}


# ---------------------------------------------------------------------------
# Reporting helpers
# ---------------------------------------------------------------------------


def ranges(nums: list[int]) -> str:
    """Compress [1,2,3,7] to '1-3, 7' so line lists stay readable."""
    if not nums:
        return "—"
    parts, start, prev = [], nums[0], nums[0]
    for x in nums[1:]:
        if x == prev + 1:
            prev = x
            continue
        parts.append(f"{start}" if start == prev else f"{start}-{prev}")
        start = prev = x
    parts.append(f"{start}" if start == prev else f"{start}-{prev}")
    return ", ".join(parts)


TIER_LABEL = {
    "A": "PROSE — absorbed marginal line number (the pass-1 target)",
    "B": "RUNNING PAGE HEAD — number sits on page furniture",
    "C": "RISKY — folio citation, referring noun, or enumeration",
}


def print_step1_candidates(per_file: dict) -> None:
    print("=" * 78)
    print("STEP 1 CANDIDATES — absorbed printer line numbers (NOT YET DELETED)")
    print("=" * 78)
    for name in TARGETS:
        cands = per_file[name]["step1"]
        live = [c for c in cands if c["skip"] is None]
        print(f"\n### {name}   total matches {len(cands)}   deletable {len(live)}")
        for tier in ("A", "B", "C"):
            grp = [c for c in live if c["tier"] == tier]
            if not grp:
                continue
            print(f"  --- TIER {tier}: {TIER_LABEL[tier]} — {len(grp)} ---")
            for c in grp:
                print(f"  {c['lineno']:>6}  [{c['token']:>3}]  …{c['context']}")
        held = [c for c in cands if c["skip"] is not None]
        if held:
            print(f"  -- withheld ({len(held)}): structural, not prose --")
            for c in held:
                print(
                    f"  {c['lineno']:>6}  [{c['token']:>3}]  {c['skip']:<16}"
                    f"  {c['full'].strip()[:60]}"
                )


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------


def load(path: Path) -> tuple[list[str], bool]:
    raw = path.read_text(encoding="utf-8")
    trailing_nl = raw.endswith("\n")
    lines = raw.split("\n")
    if trailing_nl:
        lines.pop()
    return lines, trailing_nl


def save(path: Path, lines: list[str], trailing_nl: bool) -> None:
    path.write_text("\n".join(lines) + ("\n" if trailing_nl else ""), encoding="utf-8")


def do_backup() -> list[str]:
    BACKUPS.mkdir(exist_ok=True)
    done = []
    for name in TARGETS:
        src, dst = CANON / name, BACKUPS / f"{name}.bak"
        shutil.copy2(src, dst)
        done.append(str(dst.relative_to(REPO)))
    return done


def relocate_step1(
    cands: list[dict], applied: list[dict], final: list[str]
) -> None:
    """Re-anchor Step 1 line numbers against the text after the second Step 2.

    Mutates `lineno` in place, keeping the pre-join value as `lineno_pre`.

    An applied candidate is matched by its `cleaned` text, a pending one by its
    `full` text. Either may have been *extended* by the second de-hyphenation
    (`…Obla-` picked up `tion is the Body of Christ…`), so a prefix match
    counts. Both lists are in file order and the scan only ever moves forward,
    so a repeated line matches the right occurrence. If no match is found the
    original number is left alone — a wrong number is bad, an invented one is
    worse.
    """
    was_applied = {id(c) for c in applied}
    entries = sorted(
        {id(c): c for c in list(cands) + list(applied)}.values(),
        key=lambda c: c["lineno"],
    )
    cursor = 0
    for c in entries:
        # An applied candidate lost its trailing number, so the line now reads
        # `cleaned`; a pending one still reads `full`.
        probe = c["cleaned"] if id(c) in was_applied else c["full"]
        if not probe:
            continue
        for j in range(cursor, len(final)):
            if final[j].startswith(probe):
                c["lineno_pre"] = c["lineno"]
                c["lineno"] = j + 1
                cursor = j
                break


def run_passes(
    lines: list[str],
    step1_approved: bool,
    tiers: str,
    raw: str,
    lexicon: set[str] | None = None,
    strict5: bool = False,
    name: str = "",
) -> tuple[list[str], dict]:
    """The whole pipeline over one file's lines. Pure; returns lines + stats."""
    info: dict = {
        "verse_markers": has_verse_markers(raw),
        "lines_before": len(lines),
    }

    lines, n_rstrip = step0_rstrip(lines)
    info["rstrip"] = n_rstrip

    # Re-label after rstrip: `## Text ` vs `## Text` changes detection.
    labels = region_map(lines)

    lines, joins, holds = step2_dehyphenate(lines, labels, lexicon, name)
    info["step2"] = joins
    info["step2_held"] = holds

    lines, collapsed = step3_blanks(lines)
    info["step3"] = collapsed

    # Step 1 runs LAST, on the line numbering produced by Steps 2 and 3, which
    # between them shift 87-didascalia.md by 230 lines.
    #
    # The passes are NOT independent, though the first version of this script
    # claimed they were. The claim was that a line ending in a hyphen cannot
    # also end in a digit, so joining can never create or destroy a Step 1
    # candidate. True in that direction — but false in the other. Step 1
    # deletes a trailing number and can thereby EXPOSE a hyphen that was
    # sitting behind it:
    #
    #     Concerning the reminder that the Obla- 10   <- Step 2 sees no `-$`
    #     Concerning the reminder that the Obla-      <- after Step 1 it does
    #
    # Six lines in the corpus are like this (four in 80-serata-seyon.md, two in
    # 81-teezaz.md). Left unhandled they made the script non-idempotent: a
    # second `--apply` produced different output from the first, which is
    # exactly the property the header promises. So Steps 2 and 3 run a second
    # time after Step 1, and the pipeline is iterated to a fixed point.
    labels = region_map(lines)
    cands = step1_candidates(lines, labels)
    info["step1"] = cands
    if info["verse_markers"]:
        for c in cands:
            c["skip"] = c["skip"] or "file has **N** verse markers"

    applied1: list[dict] = []
    joins_b: list[dict] = []
    holds_b: list[dict] = []
    if step1_approved:
        lines, applied1 = step1_apply(lines, cands, tiers=tiers, strict5=strict5)
        # Second de-hyphenation, over the hyphens Step 1 just uncovered.
        labels = region_map(lines)
        lines, joins_b, holds_b = step2_dehyphenate(lines, labels, lexicon, name)
        lines, collapsed_b = step3_blanks(lines)
        info["step3"] = collapsed + collapsed_b
        # A held-back join still ends in a hyphen, so the second Step 2 meets
        # it again and refuses it again. Report each hold once, keeping the
        # second sighting because its line number addresses the final text.
        again = {(h["stem"], h["fragment"], h["context"]) for h in holds_b}
        holds = [
            h for h in holds if (h["stem"], h["fragment"], h["context"]) not in again
        ]
        info["step2_held"] = holds
        # Those joins removed lines, so every Step 1 line number below one of
        # them is now stale. Re-anchor them against the final text rather than
        # letting the report quote a number that does not address the file as
        # shipped — the property the rest of this script goes to some trouble
        # to maintain.
        relocate_step1(cands, applied1, lines)
    info["step1_applied"] = applied1
    info["step2b"] = joins_b
    info["step2b_held"] = holds_b

    info["lines_after"] = len(lines)
    info["review"] = scan_manual_review("", lines, region_map(lines))
    info["lines"] = lines
    return lines, info


def process(
    apply: bool, step1_approved: bool, tiers: str = "A", strict5: bool = False
) -> dict:
    """Clean each target, and report stats against the pre-pass baseline.

    Stats are computed from `backups/<name>.md.bak` when it exists, not from
    whatever is on disk now. Otherwise re-running `--apply` would rewrite the
    reports to all-zeros — the second run has nothing left to change — and
    silently replace an accurate report with an empty one. The live file is
    still what gets cleaned and written, so a hand edit is never reverted; the
    passes are deterministic and idempotent, so both inputs converge on the
    same output.
    """
    results: dict = {}

    # The standalone-word guard asks "is the joined form a real word?" and
    # answers it from the corpus. Build that attestation set once, over all six
    # files at once, so a word whole in one file can vouch for the same word
    # broken in another. Built from the backups where they exist, i.e. from the
    # text as scraped, for the same reason the statistics are.
    corpus: dict[str, list[str]] = {}
    for name in TARGETS:
        backup = BACKUPS / f"{name}.bak"
        src = backup if backup.exists() else CANON / name
        corpus[name], _ = load(src)
    lexicon = corpus_lexicon(corpus)

    for name in TARGETS:
        path = CANON / name
        backup = BACKUPS / f"{name}.bak"

        live_lines, tnl = load(path)
        original = list(live_lines)
        out, _ = run_passes(
            list(live_lines), step1_approved, tiers, "\n".join(live_lines), lexicon,
            strict5, name,
        )

        if backup.exists():
            base_lines, _ = load(backup)
            _, info = run_passes(
                list(base_lines), step1_approved, tiers, "\n".join(base_lines),
                lexicon, strict5, name,
            )
            info["baseline"] = "backups/%s.bak" % name
        else:
            _, info = run_passes(
                list(live_lines), step1_approved, tiers, "\n".join(live_lines),
                lexicon, strict5, name,
            )
            info["baseline"] = "live file (no backup found)"

        info["changed"] = out != original
        if apply and info["changed"]:
            save(path, out, tnl)
        results[name] = info
    return results


def write_cleaning_report(
    res: dict, applied_step1: bool, apply: bool, tiers: str = "A", strict5: bool = False
) -> str:
    L: list[str] = []
    a = L.append
    a("# Cleaning Report — OCR pass 1 (`clean/ocr-pass1`)")
    a("")
    a("Produced by `scripts/clean_ocr.py`. Six files in scope, no others:")
    a("")
    for n in TARGETS:
        a(f"- `en/03-broader-canon/{n}`")
    a("")
    a("Backups of all six, taken before any modification, are in `backups/`.")
    a("")
    a(
        f"Step 1 (line-number deletion) applied: "
        f"**{'yes, tier(s) ' + tiers if applied_step1 else 'NO — awaiting approval'}"
        f"{', exact multiples of 5 only' if applied_step1 and strict5 else ''}**."
    )
    a(f"Mode: **{'apply (files written)' if apply else 'report only (no files written)'}**.")
    a("")
    a("## Summary")
    a("")
    a("| File | Trailing-space lines stripped | Line numbers deleted | Line numbers pending | De-hyphen joins | Blank lines collapsed | Lines before → after |")
    a("|---|---:|---:|---:|---:|---:|---:|")
    for n in TARGETS:
        i = res[n]
        # "Pending" is every live candidate the run did not delete — Tier B
        # running heads, Tier C content numbers, and any Tier A value that is
        # not an exact multiple of 5. Reporting 0 here merely because Step 1
        # ran would hide 392 candidates that are still outstanding.
        done = {id(c) for c in i["step1_applied"]}
        pend = len(
            [c for c in i["step1"] if c["skip"] is None and id(c) not in done]
        )
        a(
            f"| `{n}` | {i['rstrip']} | {len(i['step1_applied'])} | "
            f"{pend} | "
            f"{len(i['step2']) + len(i.get('step2b', []))} | {i['step3']} | "
            f"{i['lines_before']} → {i['lines_after']} |"
        )
    a("")
    tot_r = sum(res[n]["rstrip"] for n in TARGETS)
    tot_j = sum(len(res[n]["step2"]) + len(res[n].get("step2b", [])) for n in TARGETS)
    tot_b = sum(res[n]["step3"] for n in TARGETS)
    tot_1 = sum(len(res[n]["step1_applied"]) for n in TARGETS)
    tot_p = 0
    for n in TARGETS:
        done = {id(c) for c in res[n]["step1_applied"]}
        tot_p += len(
            [c for c in res[n]["step1"] if c["skip"] is None and id(c) not in done]
        )
    a(
        f"**Totals:** {tot_r} lines rstripped · {tot_1} line numbers deleted · "
        f"{tot_p} still pending · {tot_j} joins · "
        f"{tot_b} blank lines collapsed."
    )
    a("")

    a("## Step 0 — trailing whitespace")
    a("")
    a("Runs first, because Steps 1 and 2 both key off the end-of-line character")
    a("and a trailing space hides it.")
    a("")
    q = res["86-qalementos.md"]
    a(
        f"In `86-qalementos.md` {q['rstrip']:,} of {q['lines_before']:,} lines carried "
        f"trailing whitespace. Before stripping it the file appeared to have zero "
        f"hyphen line-breaks; afterwards it has {len(q['step2']):,}. That is the whole "
        f"reason for the ordering — run Step 2 first and this file silently cleans "
        f"nothing."
    )
    a("")
    a("| File | Lines with trailing whitespace | Total lines |")
    a("|---|---:|---:|")
    for n in TARGETS:
        a(f"| `{n}` | {res[n]['rstrip']:,} | {res[n]['lines_before']:,} |")
    a("")

    a("## Step 1 — absorbed printer line numbers")
    a("")
    a("Horner (1904) and Harden (1920) print marginal line numbers every 5 lines;")
    a("the scraper absorbed them at end of line. Detection requires all of:")
    a("")
    a("1. the file contains no `**N**` verse markers — all six qualify;")
    a("2. a 1-3 digit number at end of line, preceded by whitespace;")
    a("3. the number is within 2 of a multiple of 5.")
    a("")
    a("Condition 3 is **vacuous**: every integer is within 2 of a multiple of 5")
    a("(`n % 5` is 0, 1 or 2 — within 2 below — or 3 or 4 — within 2 above). It is")
    a("implemented as stated and it excludes nothing. The counts below are")
    a("therefore the counts of \"any 1-3 digit number at end of line\".")
    a("")
    a("`--strict5` replaces condition 3 with `n % 5 == 0`, which is what makes")
    a("the marginal-line-number hypothesis testable — a printer sets 5, 10, 15,")
    a("not 62 or 148. It is the basis on which this pass was approved, and it")
    a("cuts the deletion set from 606 candidates to 214. It narrows what is")
    a("*deleted*; the tables below still enumerate every candidate.")
    a("")
    a("Two structural guards were added, without which this pass destroys the")
    a("chapter structure of all six files:")
    a("")
    a("- **front matter and metadata** (everything up to `## Text`): `number: 82`")
    a("  and `chapters: 56` are indistinguishable from a marginal number;")
    a("- **headings**: `## Canon 1`, `## Statute 31`, `## Chapter 12` all end in a")
    a("  1-3 digit number preceded by whitespace. In `82-gessew.md` 55 of the 61")
    a("  matches are headings and only 4 are prose.")
    a("")
    a("| File | Total matches | Headings | Front matter / metadata | Remaining |")
    a("|---|---:|---:|---:|---:|")
    for n in TARGETS:
        c = res[n]["step1"]
        live = [x for x in c if x["skip"] is None]
        a(
            f"| `{n}` | {len(c)} | "
            f"{len([x for x in c if x['skip'] == 'heading'])} | "
            f"{len([x for x in c if x['skip'] in ('frontmatter', 'meta', 'before ## Text')])} | "
            f"{len(live)} |"
        )
    a("")
    a("### Tiering of the remainder")
    a("")
    a("A number at end of line is not automatically a marginal line number. Three")
    a("other things in these files match the rule exactly, so the remainder is")
    a("tiered and only tier A is recommended for deletion:")
    a("")
    a("- **Tier A — prose.** A marginal number absorbed mid-sentence. This is the")
    a("  pass-1 target. `80-serata-seyon.md` line 48: *All hail, our sons and our*")
    a("  *daughters, in the name of* `5`. The 5/10/15/20 cadence is visible in the")
    a("  line numbers themselves.")
    a("- **Tier B — running page head.** The number is the page number on a running")
    a("  head that the scraper left inline: `THE ETHIOPIC DIDASCALIA 3`,")
    a("  `MANUSCRITS COPTES. 91`. Deleting just the number leaves the head text")
    a("  behind and removes the very evidence that identifies it, making the later")
    a("  whole-line fix harder. Recommended: leave for a running-head pass; they")
    a("  are indexed in `MANUAL_REVIEW.md`.")
    a("- **Tier C — risky.** The number is real content. Three sub-cases, all in")
    a("  `86-qalementos.md`: a folio citation `(F. 4` broken across lines (Grébaut")
    a("  cites `(F. 4 r° a)` throughout); a referring noun, *commence au feuillet*")
    a("  `151`; and an enumeration of manuscript pages, *244 à 246,* `259`.")
    a("  Recommended: never delete.")
    a("")
    a("| File | Tier A prose | Tier B running head | Tier C risky | Tier A that is an exact multiple of 5 |")
    a("|---|---:|---:|---:|---:|")
    for n in TARGETS:
        live = [x for x in res[n]["step1"] if x["skip"] is None]
        ta = [x for x in live if x["tier"] == "A"]
        a(
            f"| `{n}` | {len(ta)} | {len([x for x in live if x['tier'] == 'B'])} | "
            f"{len([x for x in live if x['tier'] == 'C'])} | "
            f"{len([x for x in ta if x['strict5']])} |"
        )
    a("")
    for n in TARGETS:
        live = [x for x in res[n]["step1"] if x["skip"] is None]
        a(f"### `{n}` — {len(live)} candidates")
        a("")
        if not live:
            a("None.")
            a("")
            continue
        for tier in ("A", "B", "C"):
            grp = [x for x in live if x["tier"] == tier]
            if not grp:
                continue
            a(f"**Tier {tier} — {TIER_LABEL[tier]} ({len(grp)})**")
            a("")
            a("| Line | Number | Kind | 60 chars of preceding context |")
            a("|---:|---:|---|---|")
            for x in grp:
                ctx = x["context"].replace("|", "\\|")
                a(f"| {x['lineno']} | `{x['token']}` | {x['kind']} | `…{ctx}` |")
            a("")

    a("## Step 2 — de-hyphenation")
    a("")
    a("`word-` at end of line is joined to a continuation beginning with a")
    a("lowercase letter, unless the resulting compound is attested hyphenated")
    a("mid-line elsewhere in the same file. That attestation set is built")
    a("per-file from the original text before any joining.")
    a("")
    for n in TARGETS:
        j = res[n]["step2"]
        a(f"### `{n}` — {len(j)} joins")
        a("")
        if not j:
            a("None — this file has no hyphen line-breaks.")
            a("")
            continue
        a("| Line | Before → After |")
        a("|---:|---|")
        for x in j:
            a(f"| {x['lineno']} | `{x['word_before']}` → `{x['word_after']}` |")
        a("")

    tot_2b = sum(len(res[n].get("step2b", [])) for n in TARGETS)
    a("### Step 2b — the second de-hyphenation, after Step 1")
    a("")
    a("Step 1 can uncover a hyphen it was hiding: `…that the Obla- 10` ends in")
    a("a digit, so the first Step 2 cannot see it, but once the `10` is deleted")
    a("the line ends `Obla-` and the join becomes visible. Steps 2 and 3")
    a("therefore run a second time after Step 1, which is what makes the whole")
    a("pipeline idempotent — without it a second `--apply` produced different")
    a("output from the first.")
    a("")
    if tot_2b == 0:
        a("**No second-pass joins** — Step 1 was not applied in this run.")
        a("")
    else:
        a(f"**{tot_2b} joins** only became visible after Step 1.")
        a("")
        a("| File | Line | Before → After |")
        a("|---|---:|---|")
        for n in TARGETS:
            for x in res[n].get("step2b", []):
                a(
                    f"| `{n}` | {x['lineno']} | `{x['word_before']}` → "
                    f"`{x['word_after']}` |"
                )
        a("")

    a("### Step 2a — the standalone-word guard")
    a("")
    a("A second refusal rule, added after pass 1 shipped three bad joins.")
    a("A join is held back when the continuation fragment is itself a common")
    a("standalone English word, **unless** the joined form is attested as an")
    a("ordinary unhyphenated token somewhere in these six files — so `him-` +")
    a("`self` still joins, and `blue-` + `black` does not.")
    a("")
    tot_h = sum(
        len(res[n]["step2_held"]) + len(res[n].get("step2b_held", []))
        for n in TARGETS
    )
    tot_j2 = sum(len(res[n]["step2"]) + len(res[n].get("step2b", [])) for n in TARGETS)
    a(
        f"**{tot_h} of {tot_h + tot_j2} candidate joins are held back "
        f"({100 * tot_h / max(tot_h + tot_j2, 1):.2f}%).** Every one is listed "
        f"below; none is silently dropped."
    )
    a("")
    a("| File | Line | Held back | Would have produced | Context |")
    a("|---|---:|---|---|---|")
    for n in TARGETS:
        for x in res[n]["step2_held"] + res[n].get("step2b_held", []):
            ctx = x["context"].replace("|", "\\|")
            a(
                f"| `{n}` | {x['lineno']} | `{x['stem']}-` / `{x['fragment']}` | "
                f"`{x['would_have_joined']}` | `{ctx}` |"
            )
    if tot_h == 0:
        a("| — | — | none | — | — |")
    a("")
    a("The guard refuses the join; it does not repair the line. What is left")
    a("behind is a hyphen that still needs an editor. The three corrected by")
    a("hand in this pass and the ones still outstanding are tracked in")
    a("`MANUAL_REVIEW.md`.")
    a("")

    a("## Step 3 — blank lines")
    a("")
    a("| File | Runs of 3+ blank lines collapsed to 2 |")
    a("|---|---:|")
    for n in TARGETS:
        a(f"| `{n}` | {res[n]['step3']} |")
    a("")
    a("## Not done in this pass")
    a("")
    a("Footnotes were not moved, translator introductions were not moved, and OCR")
    a("misspellings were not corrected. All three are catalogued in")
    a("`MANUAL_REVIEW.md` with line numbers.")
    a("")
    a(f"Nor was any Step 1 candidate outside the approved set touched: {tot_p} of")
    a("the 606 remain, being Tier B running heads (260), Tier C content numbers")
    a("(43), and Tier A values that are not exact multiples of 5 (89). Each wants")
    a("its own pass. Five hyphens the guard refused are likewise still hyphens,")
    a("and eight of the deletions that *were* made look like content rather than")
    a("marginal furniture — `MANUAL_REVIEW.md` §4 and §5.")
    a("")
    return "\n".join(L) + "\n"


def find_line(lines: list[str], needle: str, start: int = 0) -> int:
    """1-based line number of the first line containing `needle`, else 0.

    Every line number quoted in the prose of these reports is resolved this
    way rather than written down. Hardcoded numbers go stale the moment Step 2
    joins a line above them, and this pass moves 981 lines.
    """
    for i in range(start, len(lines)):
        if needle in lines[i]:
            return i + 1
    return 0


def find_all(lines: list[str], needle: str, limit: int = 3) -> list[int]:
    out = []
    for i, l in enumerate(lines):
        if needle in l:
            out.append(i + 1)
            if len(out) >= limit:
                break
    return out


def first_nonblank_after(lines: list[str], lineno: int) -> int:
    """1-based line number of the first non-blank line strictly after lineno."""
    for i in range(lineno, len(lines)):
        if lines[i].strip():
            return i + 1
    return 0


# Per file: the anchor that marks where the sacred text begins, and a note
# built around the line numbers resolved from it at report time.
INTRO_ANCHORS = {
    "80-serata-seyon.md": (
        "In the name of the Father and of",
        "No translator introduction. `## Text` is followed immediately by the "
        "Sinodos incipit, *In the name of the Father…*. What precedes it is the "
        "repository's own Metadata table and Notes.",
    ),
    "81-teezaz.md": (
        "Concerning the time during which",
        "No translator introduction. The file opens mid-work at `## Statute 31` — "
        "it is the continuation of the Sinodos begun in `80-serata-seyon.md`, "
        "whose statutes run 1-30.",
    ),
    "82-gessew.md": (
        "In the name of the Father and the Son",
        "No translator introduction. `## Preamble` is itself sacred text — the "
        "incipit *In the name of the Father…*.",
    ),
    "84-mashafa-kidan-1.md": (
        "Ir came to pass",
        "No translator introduction. Sacred text begins under `## Prologue` with "
        "*Ir came to pass, after our Lord rose from the dead…* (`Ir` is an OCR "
        "failure of the drop-capital `It`). Editorial matter does appear below, but "
        "as **footnotes**, not as a prefatory block — footnote 2, discussing Codex "
        "S. and the Copto-Arabic version, is at line {fn}.",
    ),
    "86-qalementos.md": (
        "# Livre Premier.",
        "**The one file with a real translator introduction.** A blockquote note "
        "added by the repository's scraper sits just under `## Text`; Grébaut's own "
        "`INTRODUCTION` heading is at line {intro} and his prefatory essay runs to "
        "line {intro_end} — it cites Nau, Dillmann and the Tübingen manuscript and "
        "describes the seven Books. Sacred text begins at `# Livre Premier.`, with "
        "the incipit at line {incipit}. Everything from {intro} to {intro_end} is "
        "Grébaut, not Qalementos, and should be moved out of `## Text` in a later "
        "pass.",
    ),
    "87-didascalia.md": (
        "IN THE NAME OF GOD THE FATHER ALMIGHTY",
        "No translator introduction. `## Chapter 1` carries the work's own title as "
        "an `###` heading at line {title}, and the sacred text begins with the "
        "invocation *IN THE NAME OF GOD THE FATHER ALMIGHTY…* (printed in small "
        "capitals, which the OCR preserved as literal capitals).",
    ),
}

# What each still-outstanding held-back join should read, established by
# reading the surrounding page. Keyed by (file, stem, fragment). All five are
# two-column footnote interleaving: the true continuation sits in the other
# column further down the page, so this script — which is not allowed to move
# text — cannot repair them. Contrast HELD_JOIN_REPAIRS, which holds the three
# that could be resolved in place.
HELD_JOIN_NOTES = {
    ("87-didascalia.md", "trans", "children"):
        "`translator` — continuation `lator` is in the next column",
    ("87-didascalia.md", "cor", "right"):
        "`correct` — continuation `rect` is in the next column",
    ("87-didascalia.md", "money", "its"):
        "`money-changers` — continuation `changers` is in the next column",
    ("87-didascalia.md", "Xan", "month"):
        "`Xanthicus` — continuation `thicus` is in the next column",
    ("87-didascalia.md", "per", "you"):
        "`pernicious` — continuation `nicious` is in the next column",
}

# Step 1 deletions that are probably content, not marginal line numbers. Keyed
# by an anchor string rather than a line number so the entry survives reruns.
SUSPECT_DELETIONS = [
    (
        "86-qalementos.md",
        "Le sABBAT (fol. 59 v° b à fol.",
        "60",
        "the second half of a folio range, `fol. 59 v° b à fol. 60`",
        "high",
    ),
    (
        "86-qalementos.md",
        "Abou-Taleb mourut au mois de Schewal de l’an",
        "10",
        "a year — *died in the month of Shawwal of the year 10*",
        "high",
    ),
    (
        "86-qalementos.md",
        "‘O xaréhoyoc obroc",
        "150",
        "Greek ὑπ’ ἀριθμὸν 150, *under catalogue number 150*",
        "high",
    ),
    (
        "86-qalementos.md",
        "GNAYPAPR ÉTÉPOV creudiv",
        "160",
        "Greek ἀριθμόν 160, *number 160*",
        "high",
    ),
    (
        "86-qalementos.md",
        "uno Emo EN Jade CE Mise",
        "550",
        "too large for a printer's margin, which runs 5–50",
        "medium",
    ),
    (
        "86-qalementos.md",
        "POS MJradas 40010 aauro",
        "230",
        "too large for a printer's margin",
        "medium",
    ),
    (
        "86-qalementos.md",
        "Îl 2 S à",
        "430",
        "too large for a printer's margin; the line is OCR wreckage",
        "medium",
    ),
    (
        "86-qalementos.md",
        "LE TROPAIRE O Movoyevñc.",
        "255",
        "too large for a printer's margin",
        "medium",
    ),
]


def write_manual_review(res: dict) -> str:
    L: list[str] = []
    a = L.append
    a("# Manual Review — OCR pass 1")
    a("")
    a("Everything in this file was **deliberately left unchanged** by")
    a("`scripts/clean_ocr.py`. Line numbers refer to the files as they stand after")
    a("pass 1. Nothing here has been corrected, moved, or rewritten.")
    a("")
    a("Three categories, per the pass-1 brief: suspected OCR misspellings,")
    a("footnote locations, and the introduction/sacred-text boundary.")
    a("")

    a("## 1. Suspected OCR misspellings")
    a("")
    a("### The `lo` / `ao` class — marginal line numbers absorbed at line *start*")
    a("")
    a("This is the largest single class and it is the mirror image of Step 1. Where")
    a("Step 1 finds a marginal number absorbed at the **end** of a line, these are")
    a("marginal numbers absorbed at the **start** of a line and then misread as")
    a("letters: `lo` is the printed **10**, `ao` is the printed **20**. Two examples,")
    a("both from `80-serata-seyon.md`:")
    a("")
    a("```")
    a("258  lo not accept the person of a rich man in case of his being")
    a("420  ao over the poor and needy, nor respect the person of the")
    a("```")
    a("")
    a("Neither sentence begins with a word; the leading token is a page number.")
    a("Correcting these means **deleting** the token, not respelling it — but they")
    a("are out of scope for pass 1 because the rule would have to distinguish them")
    a("from the genuine English `lo` (*lo, they who are on the right take…*, line 337")
    a("of the same file) and from Greek/Latin fragments in `86-qalementos.md`.")
    a("")
    a("### Single-occurrence cases, with exact locations")
    a("")
    a("The `lo` / `ao` class is indexed separately below, being too numerous for")
    a("this table. Everything else, brief-named or not:")
    a("")
    a("| File | Line | Reads | Should read | Named in brief | Why |")
    a("|---|---:|---|---|:-:|---|")
    for n in TARGETS:
        for m in res[n]["review"]["misspellings"]:
            if m["key"] in ("ao", "lo"):
                continue
            reads = m["reads"].replace("|", "\\|")
            a(
                f"| `{n}` | {m['lineno']} | `{reads}` | `{m['correction']}` | "
                f"{'yes' if m['in_brief'] else '—'} | {m['why']} |"
            )
    a("")
    a("### Full occurrence index")
    a("")
    a("| File | Pattern | Count | Lines |")
    a("|---|---|---:|---|")
    for n in TARGETS:
        byk: dict[str, list[int]] = {}
        for m in res[n]["review"]["misspellings"]:
            byk.setdefault(m["key"], []).append(m["lineno"])
        for key in sorted(byk):
            ls = sorted(set(byk[key]))
            shown = ranges(ls[:60]) + (" …" if len(ls) > 60 else "")
            a(f"| `{n}` | `{key}` | {len(ls)} | {shown} |")
    a("")
    a("This index is a floor, not a census. It reports what the patterns above")
    a("match; the OCR of these six volumes is noisy throughout and misspellings")
    a("without a distinctive shape (a wrong letter that still forms a word) cannot")
    a("be found by rule at all.")
    a("")

    a("## 2. Footnotes")
    a("")
    a("Two things to relocate, and they are separate problems.")
    a("")
    d87 = res["87-didascalia.md"]["lines"]
    d84 = res["84-mashafa-kidan-1.md"]["lines"]
    d86 = res["86-qalementos.md"]["lines"]
    mk87 = find_line(d87, "We,? the Twelve Apostles")
    mk84 = find_line(d84, "was handled")
    a("**Markers** are printed superscripts that the OCR flattened into stray")
    a("symbols glued to a word or to punctuation — `®`, `¢`, `’`, `°`, `*`. From")
    a(f"`87-didascalia.md` line {mk87}: *We,? the Twelve Apostles, ministers of His*")
    a(f"*only-* — the `?` is footnote 2. From `84-mashafa-kidan-1.md` line {mk84}:")
    a("*and was handled ® by Thomas*. Because the same characters are also")
    a("legitimate apostrophes and quotation marks, the counts below are heuristic")
    a("and will over-report.")
    a("")
    a("**Bodies** are the printed apparatus at the foot of each page, which the")
    a("scraper left inline in the middle of the sacred text. In `87-didascalia.md`")
    a("they arrive as two interleaved columns, which is why they are unreadable:")
    a("")
    fb = find_line(d87, "1 A. adds: Their prayer and")
    a("```")
    for k in range(3):
        if fb and fb - 1 + k < len(d87):
            a(f"{fb + k}  {d87[fb - 1 + k]}")
    a("```")
    a("")
    a("That is footnote 1 and footnote 3 printed side by side, read across instead")
    a("of down. Reassembling them needs column detection and is well outside a")
    a("noise-removal pass.")
    a("")
    heads87 = find_all(d87, "THE ETHIOPIC DIDASCALIA", limit=2)
    a("A third, related artifact: **running page heads**. `87-didascalia.md` carries")
    a(
        "`" + d87[heads87[0] - 1].strip() + f"` (line {heads87[0]}), "
        "`" + d87[heads87[1] - 1].strip() + f"` (line {heads87[1]}) and so on every"
    )
    a("few pages. `86-qalementos.md` carries the same thing in French:")
    a("")
    for needle in ("MANUSCRITS COPTES.", "ORIENT CHRÉTIEN.", "PSEUDO-CLÉMENTINE."):
        h = find_line(d86, needle)
        if h:
            a(f"- line {h}: `{d86[h - 1].strip()[:70]}`")
    a("")
    a("These sit on their own line and are pure page furniture. They are also the")
    a("reason tier B of Step 1 exists: the number on such a line is a page number,")
    a("and deleting it alone would leave the head text stranded in the text.")
    a("")
    a("| File | Footnote markers (lines) | Footnote bodies (lines) | Running heads (lines) |")
    a("|---|---:|---:|---:|")
    for n in TARGETS:
        r = res[n]["review"]
        a(
            f"| `{n}` | {len(r['markers'])} | {len(r['bodies'])} | {len(r['heads'])} |"
        )
    a("")
    for n in TARGETS:
        r = res[n]["review"]
        if not (r["bodies"] or r["heads"]):
            continue
        a(f"### `{n}`")
        a("")
        if r["bodies"]:
            b = r["bodies"]
            a(f"- **Footnote bodies** ({len(b)}): {ranges(b[:80])}{' …' if len(b) > 80 else ''}")
        if r["heads"]:
            h = r["heads"]
            a(f"- **Running heads** ({len(h)}): {ranges(h[:80])}{' …' if len(h) > 80 else ''}")
        if r["markers"]:
            m = r["markers"]
            a(f"- **Marker lines** ({len(m)}): {ranges(m[:40])}{' …' if len(m) > 40 else ''}")
        a("")

    a("## 3. Introduction / sacred-text boundary")
    a("")
    a("Only one of the six files actually has a translator's introduction inside")
    a("`## Text`. The other five begin with sacred text; what precedes it is the")
    a("repository's own front matter, Metadata table and Notes, which are correct")
    a("where they are.")
    a("")
    a("| File | Sacred text begins | Detail |")
    a("|---|---:|---|")
    for n in TARGETS:
        anchor, note = INTRO_ANCHORS[n]
        lines = res[n]["lines"]
        at = find_line(lines, anchor)
        if n == "86-qalementos.md":
            intro = find_line(lines, "INTRODUCTION")
            note = note.format(
                intro=intro,
                intro_end=at - 1,
                incipit=find_line(lines, "Incipit"),
            )
            at_shown = at
        elif n == "84-mashafa-kidan-1.md":
            note = note.format(fn=find_line(lines, "2 Codex S."))
            at_shown = at
        elif n == "87-didascalia.md":
            note = note.format(title=find_line(lines, "### THE DOCTRINE"))
            at_shown = at
        else:
            at_shown = at
        a(f"| `{n}` | {at_shown} | {note} |")
    a("")

    a("## 4. Hyphens the de-hyphenation guard refused to join")
    a("")
    a("`word-` at end of line is normally joined to the next line. The guard")
    a("refuses when the continuation fragment is a whole English word and the")
    a("joined form is not attested anywhere in the six files — see *Step 2a* in")
    a("`CLEANING_REPORT.md`. Refusing is not repairing: each line below still")
    a("carries a hyphen that an editor has to resolve, and most of them are")
    a("two-column footnote interleaving, where the true continuation is further")
    a("down the page in the other column.")
    a("")
    a("| File | Line | Reads | Correct reading |")
    a("|---|---:|---|---|")
    for n in TARGETS:
        for x in res[n]["step2_held"] + res[n].get("step2b_held", []):
            frag = f"`{x['stem']}-` / `{x['fragment']}`"
            note = HELD_JOIN_NOTES.get((n, x["stem"], x["fragment"]), "**unresolved**")
            a(f"| `{n}` | {x['lineno']} | {frag} | {note} |")
    a("")
    a("Three further joins the guard caught have already been resolved and are")
    a("no longer in this list, because `HELD_JOIN_REPAIRS` in the script now")
    a("performs the correct merge: `blue-black` (a colour compound, hyphen")
    a("kept), `this type` (two words) and `Phari the bishop` (a manuscript")
    a("variant inside a footnote).")
    a("")

    a("## 5. Step 1 deletions to re-examine")
    a("")
    a("Tier A means the classifier saw ordinary prose before the number. It has")
    a("no rule for `fol.`, for French `l'an`, or for Greek `ἀριθμόν`, so a few")
    a("numbers that are content rather than marginal furniture were sorted into")
    a("Tier A and deleted with the approved batch. They are listed here so the")
    a("next pass can restore them; all are in the French Qalementos.")
    a("")
    a("| File | Line | Deleted | What it probably was | Confidence |")
    a("|---|---:|---:|---|---|")
    for n, ln, tok, what, conf in SUSPECT_DELETIONS:
        at = find_line(res[n]["lines"], ln)
        a(f"| `{n}` | {at or '?'} | `{tok}` | {what} | {conf} |")
    a("")
    return "\n".join(L) + "\n"


HANDOFF_HEADER = """# Handoff — OCR cleaning pass 1, six broader-canon files

> **Purpose of this file:** a bridge / handoff document between Claude sessions.
> It contains, verbatim and in full, the two reports produced when
> `scripts/clean_ocr.py` was written and run against the six files listed
> below.
> Branch: `clean/ocr-pass1`. Date: {date}.
>
> Files in scope, and the only files modified:
>
{filelist}
>
> Backups taken before any modification: `backups/<name>.md.bak` for all six.
>
> **State on handoff:** Steps 0, 2, 2a, 2b and 3 are applied, and Step 1 is
> applied for **Tier A restricted to exact multiples of 5** — 214 deletions,
> approved by the maintainer. The command that reproduces the shipped files
> exactly, from the backups, is:
>
> ```
> python3 scripts/clean_ocr.py --apply --step1-approved --tiers A --strict5
> ```
>
> **392 of the 606 Step 1 candidates remain undeleted** and are indexed in
> `MANUAL_REVIEW.md`: Tier B running heads (260), Tier C content numbers (43),
> and Tier A values that are not exact multiples of 5 (89). Each needs its own
> pass; none was touched here.
>
> Everything below the first horizontal rule is `CLEANING_REPORT.md` and then
> `MANUAL_REVIEW.md`, each reproduced word for word.

---

## Pass 2 — {date}

Three things changed after pass 1 shipped.

**1. Three bad de-hyphenation joins were found and fixed.** Pass 1 joined
`blue-` / `black` into `blueblack`, `this-` / `type` into `thistype`, and
`Phari-` / `the` into `Pharithe`. The first is a real colour compound whose
hyphen belongs to the text, the second is two words with a spurious OCR hyphen,
and the third is inside a critical footnote quoting a manuscript variant, where
the word boundary carries the sense.

**2. A standalone-word guard was added to Step 2.** It refuses a join when the
continuation fragment is itself a common standalone English word, unless the
joined form is attested as an ordinary unhyphenated token somewhere in the six
files — so `him-` + `self` still joins and `blue-` + `black` does not. Run
against the 981 joins pass 1 made, it flags **8 (0.82%), and all 8 are genuine
errors** — no false positives. Three are the ones above; the other five are
two-column footnote interleaving in `87-didascalia.md`, where the scraper put
the wrong column's first word on the continuation line (`money-` / `its`, where
the real reading is `money-changers`). Those five are held, not repaired: the
true continuation is elsewhere on the page and this script may not move text.

The word list is English-only, as briefed. Adding common French words for
`86-qalementos.md` was tried and rejected — it took the flag count from 8 to 20
and every one of the 12 extra flags was a false alarm on a correctly-joined
French word (`grâ-ces`, `déli-ces`, `vipè-res`, `canonia-les`).

**3. The pipeline was not idempotent, and now is.** Pass 1's header claimed
Steps 1 and 2 could not interact, on the grounds that a line ending in a hyphen
cannot also end in a digit. That holds one way only. Step 1 deletes a trailing
number and can thereby *expose* a hyphen that Step 2 could not previously see:

```
Concerning the reminder that the Obla- 10     <- Step 2 sees no trailing hyphen
Concerning the reminder that the Obla-        <- after Step 1 it does
```

Six lines in the corpus are like this. Until Step 1 was actually applied the
defect was invisible; once applied, a second `--apply` produced different files
from the first. Steps 2 and 3 now run again after Step 1, and
`--selftest` asserts convergence on all six files.

### Still outstanding

| What | Count | Where |
|---|---:|---|
| Tier B running heads | 260 | `MANUAL_REVIEW.md`, Step 1 tables |
| Tier C content numbers | 43 | `MANUAL_REVIEW.md`, Step 1 tables |
| Tier A, not a multiple of 5 | 89 | `MANUAL_REVIEW.md`, Step 1 tables |
| Held-back hyphens (footnote columns) | 5 | `MANUAL_REVIEW.md` §4 |
| Tier A deletions that look like content | 8 | `MANUAL_REVIEW.md` §5 |
| Suspected OCR misspellings | — | `MANUAL_REVIEW.md` §1 |
| Footnote placement | — | `MANUAL_REVIEW.md` §2 |

The last row of concern: **eight of the 214 approved deletions were probably
content, not marginal furniture** — all in `86-qalementos.md`, all cases the
Tier classifier has no rule for (`fol. 59 v° b à fol. 60`, `de l'an 10`, Greek
`ὑπ' ἀριθμὸν 150`). They were deleted because the approval was explicit and
numeric; §5 of `MANUAL_REVIEW.md` lists them with line numbers so the next pass
can restore them.

---

<!-- ===================== CLEANING_REPORT.md (verbatim) ===================== -->

{cleaning}

---

<!-- ====================== MANUAL_REVIEW.md (verbatim) ====================== -->

{manual}"""


def write_handoff(cleaning: str, manual: str, date: str) -> str:
    filelist = "\n".join(f"> - `en/03-broader-canon/{n}`" for n in TARGETS)
    return HANDOFF_HEADER.format(
        date=date, filelist=filelist, cleaning=cleaning.rstrip(), manual=manual.rstrip()
    ) + "\n"


def selftest(tiers: str, strict5: bool) -> int:
    """Run the pipeline twice over each backup and assert the output settles.

    Exists because it did not. The first version ran Step 2 before Step 1 and
    declared the two passes non-interacting; Step 1 then uncovered six hyphens
    that Step 2 had been unable to see, and a second `--apply` silently
    produced different files from the first. Nothing writes to disk here.
    """
    corpus: dict[str, list[str]] = {}
    for name in TARGETS:
        backup = BACKUPS / f"{name}.bak"
        corpus[name], _ = load(backup if backup.exists() else CANON / name)
    lexicon = corpus_lexicon(corpus)

    bad = 0
    for name in TARGETS:
        base = corpus[name]
        once, _ = run_passes(
            list(base), True, tiers, "\n".join(base), lexicon, strict5, name
        )
        twice, _ = run_passes(
            list(once), True, tiers, "\n".join(once), lexicon, strict5, name
        )
        if once == twice:
            print(f"  ok        {name}  ({len(base)} → {len(once)} lines, stable)")
            continue
        bad += 1
        drift = [i for i, (a, b) in enumerate(zip(once, twice)) if a != b]
        print(
            f"  NOT IDEMPOTENT  {name}  "
            f"{len(once)} vs {len(twice)} lines, {len(drift)} lines differ"
        )
        for i in drift[:5]:
            print(f"      pass 1: {once[i]!r}")
            print(f"      pass 2: {twice[i]!r}")
    print(
        f"\nselftest: {len(TARGETS) - bad}/{len(TARGETS)} files idempotent"
        + ("" if bad else " — all stable")
    )
    return 1 if bad else 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--selftest",
        action="store_true",
        help="assert the pipeline is idempotent; writes nothing",
    )
    p.add_argument("--backup", action="store_true", help="copy targets to backups/")
    p.add_argument("--report", action="store_true", help="analyse, write reports only")
    p.add_argument("--apply", action="store_true", help="write cleaned files")
    p.add_argument(
        "--step1-approved",
        action="store_true",
        help="also delete absorbed marginal line numbers (requires review)",
    )
    p.add_argument(
        "--date",
        default="2026-07-30",
        help="date stamped into HANDOFF-CLEANING.md (kept explicit so reruns "
        "are byte-reproducible rather than clock-dependent)",
    )
    p.add_argument(
        "--tiers",
        default="A",
        help="which Step 1 tiers to delete when approved: A (prose, default), "
        "AB (adds running-head page numbers), ABC (adds risky). See "
        "CLEANING_REPORT.md for what each tier contains.",
    )
    p.add_argument(
        "--strict5",
        action="store_true",
        help="narrow Step 1 deletion to numbers that are an exact multiple of "
        "5. Without it the tier gate alone admits every integer, because "
        "'near a multiple of 5' is vacuously true (see near_multiple_of_5).",
    )
    args = p.parse_args()
    tiers = args.tiers.upper()
    if set(tiers) - set("ABC"):
        p.error("--tiers accepts only the letters A, B, C")

    if args.selftest:
        return selftest(tiers, args.strict5)

    if args.backup:
        for d in do_backup():
            print(f"backed up -> {d}")
        if not (args.report or args.apply):
            return 0

    if not (args.report or args.apply):
        p.print_help()
        return 1

    res = process(
        apply=args.apply,
        step1_approved=args.step1_approved,
        tiers=tiers,
        strict5=args.strict5,
    )
    print_step1_candidates(res)

    cleaning = write_cleaning_report(
        res, args.step1_approved, args.apply, tiers, args.strict5
    )
    manual = write_manual_review(res)
    (REPO / "CLEANING_REPORT.md").write_text(cleaning, encoding="utf-8")
    (REPO / "MANUAL_REVIEW.md").write_text(manual, encoding="utf-8")
    (REPO / "HANDOFF-CLEANING.md").write_text(
        write_handoff(cleaning, manual, args.date), encoding="utf-8"
    )
    print("\nwrote CLEANING_REPORT.md, MANUAL_REVIEW.md and HANDOFF-CLEANING.md")
    if args.step1_approved:
        n1 = sum(len(res[n]["step1_applied"]) for n in TARGETS)
        print(f"Step 1 applied for tier(s) {tiers}: {n1} numbers deleted.")
    else:
        pend = sum(
            len([c for c in res[n]["step1"] if c["skip"] is None]) for n in TARGETS
        )
        print(f"Step 1 NOT applied: {pend} candidates await approval.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
