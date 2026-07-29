#!/usr/bin/env python3
"""Rebuild en/01-old-testament/06-ethiopian-ot/45-jubilees.md from R.H. Charles's
translation of the Book of Jubilees (1902/1917).

The file previously held only Charles's chapter *summaries*: an earlier scraper
read the sacred-texts.com table-of-contents page instead of the chapter pages,
yielding ~46 words per chapter. This script replaces everything after the
"## Text" marker with the full body text, verbatim.

Primary source
    https://www.globalgreyebooks.com/online-ebooks/r-h-charles_book-of-jubilees_complete-text.html
    A clean HTML transcription. Every verse is its own <p>, prefixed with
    Charles's verse number; each chapter's first verse is prefixed with a Roman
    numeral. Footnote references are <a><sup>[n]</sup></a> and are dropped.

Fallback (only used if the primary cannot be fetched or yields no chapters)
    https://archive.org/stream/CHARLESBookOfJubilees/CHARLES_Book_of_Jubilees_djvu.txt
    Raw OCR of Charles's commentary edition. The scan interleaves body text with
    the commentary apparatus, breaks words across lines, and carries substantial
    OCR corruption. Recovery is therefore best-effort: chapters that cannot be
    segmented confidently are emitted as MISSING rather than guessed at.

Nothing is paraphrased, summarised, modernised or "improved". Chapters that
cannot be retrieved get a MISSING marker instead of invented content.

Usage
    python3 scripts/fetch_jubilees.py                # fetch, back up, rewrite, report
    python3 scripts/fetch_jubilees.py --dry-run      # report only, touch nothing
    python3 scripts/fetch_jubilees.py --cache DIR    # reuse/store downloaded pages
    python3 scripts/fetch_jubilees.py --source fallback
"""

from __future__ import annotations

import argparse
import copy
import html
import re
import sys
import unicodedata
from pathlib import Path

try:
    import requests
except ImportError:  # pragma: no cover
    sys.exit("error: requests is required (pip install requests)")

try:
    from bs4 import BeautifulSoup
except ImportError:  # pragma: no cover
    sys.exit("error: beautifulsoup4 is required (pip install beautifulsoup4)")


REPO_ROOT = Path(__file__).resolve().parent.parent
TARGET = REPO_ROOT / "en" / "01-old-testament" / "06-ethiopian-ot" / "45-jubilees.md"
BACKUP = REPO_ROOT / "backups" / "45-jubilees.md.bak"

PRIMARY_URL = (
    "https://www.globalgreyebooks.com/online-ebooks/"
    "r-h-charles_book-of-jubilees_complete-text.html"
)
FALLBACK_URL = (
    "https://archive.org/stream/CHARLESBookOfJubilees/"
    "CHARLES_Book_of_Jubilees_djvu.txt"
)

N_CHAPTERS = 50
TEXT_MARKER = "## Text"
MIN_CHAPTER_WORDS = 150  # below this, assume the summary-scrape bug recurred

USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) Bible-Ethiopienne/1.0 "
    "(public-domain text preservation)"
)


# --------------------------------------------------------------------------
# Roman numerals
# --------------------------------------------------------------------------

def _roman(n: int) -> str:
    out = ""
    for value, sym in ((50, "L"), (40, "XL"), (10, "X"), (9, "IX"),
                       (5, "V"), (4, "IV"), (1, "I")):
        while n >= value:
            out += sym
            n -= value
    return out


ROMAN_TO_INT = {_roman(n): n for n in range(1, N_CHAPTERS + 1)}
# The primary transcription has one OCR slip: chapter VI is typeset "V1."
ROMAN_TO_INT["V1"] = 6

_ROMAN_ALT = "|".join(sorted(ROMAN_TO_INT, key=len, reverse=True))

# Chapter opener: optional leading Anno Mundi gloss, then a Roman numeral.
CHAPTER_RE = re.compile(r"^(?:\((?P<gloss>[^()]*)\)\s*)?(?P<roman>" + _ROMAN_ALT + r")\.\s+")

# Verse opener: optional leading Anno Mundi gloss, then an arabic number
# followed either by punctuation, or by a space when the next word clearly
# starts a sentence (Charles's transcriber sometimes omits the period).
VERSE_RE = re.compile(
    r"^(?:\((?P<gloss>[^()]*)\)\s*)?(?P<num>\d{1,3})\s*[.,:;]\s+"
    r"|^(?P<num2>\d{1,3})\s+(?=[A-Z“(\[†])"
)

# A paragraph that is nothing but a chronological marker, e.g. "(8 A.M.)" or
# "2450 A.M. (A.M. = Anno Mundi)". In print these are marginal notes attached to
# the passage that follows, so they are carried forward onto the next verse.
CHRON_ONLY_RE = re.compile(
    r"^\(?\s*[\d\s\-–?]+A\.?\s?M\.?\s*\)?[\s.]*"
    r"(?:\(\s*A\.M\.\s*=\s*Anno\s+Mundi\s*\))?$",
    re.IGNORECASE,
)

# The transcriber's expansion of the abbreviation — editorial, not Charles.
ABBREV_GLOSS_RE = re.compile(r"\(\s*A\.M\.\s*=\s*Anno\s+Mundi\s*\)", re.IGNORECASE)

# The publisher's end-of-book marker, which is not part of the text.
BACK_MATTER_RE = re.compile(r"^(?:THE\s+END|FINIS)\.?$", re.IGNORECASE)

# The book's own closing colophon. It belongs to the text but not to any verse,
# so it is set after the last chapter rather than folded into Jubilees 50:13.
COLOPHON_RE = re.compile(
    r"^Herewith is completed the account of the division of the days\.?$",
    re.IGNORECASE,
)


# --------------------------------------------------------------------------
# Fetching
# --------------------------------------------------------------------------

def decode_body(response) -> str:
    """Decode a response as UTF-8 when possible.

    Neither source sends a charset in its Content-Type header, so requests falls
    back to ISO-8859-1 and mangles Charles's curly quotes and his transliterated
    names (Lûbâr, Mastêmâ). Both pages are in fact UTF-8, and the curly quotes
    matter: verse splitting keys off them.
    """
    raw = response.content
    declared = re.search(rb'charset=["\']?([\w-]+)', raw[:4096], re.IGNORECASE)
    candidates = ["utf-8"]
    if declared:
        candidates.insert(0, declared.group(1).decode("ascii", "ignore").lower())
    for encoding in candidates:
        try:
            return raw.decode(encoding)
        except (UnicodeDecodeError, LookupError):
            continue
    return raw.decode(response.encoding or "utf-8", errors="replace")


def fetch(url: str, cache_dir: Path | None) -> str:
    """Return the body of `url`, using `cache_dir` as a read-through cache."""
    slug = re.sub(r"[^A-Za-z0-9]+", "_", url)[-80:]
    cached = cache_dir / slug if cache_dir else None
    if cached and cached.exists():
        print(f"  using cached copy: {cached}")
        return cached.read_text(encoding="utf-8", errors="replace")

    last_error: Exception | None = None
    for attempt in (1, 2, 3):
        try:
            response = requests.get(
                url, headers={"User-Agent": USER_AGENT}, timeout=60
            )
            response.raise_for_status()
            body = decode_body(response)
            print(f"  fetched {len(body):,} chars from {url}")
            if cached:
                cache_dir.mkdir(parents=True, exist_ok=True)
                cached.write_text(body, encoding="utf-8")
            return body
        except Exception as exc:  # network, HTTP status, decoding
            last_error = exc
            print(f"  attempt {attempt} failed: {exc}", file=sys.stderr)
    raise RuntimeError(f"could not fetch {url}: {last_error}")


# --------------------------------------------------------------------------
# Shared text helpers
# --------------------------------------------------------------------------

def normalise(text: str) -> str:
    """Collapse whitespace without altering any word."""
    text = text.replace("\xa0", " ").replace("​", "")
    return re.sub(r"\s+", " ", text).strip()


def split_run_on_verses(text: str, first_num: int) -> list[list]:
    """Split a block that packs several verses into one paragraph.

    Charles's transcriber occasionally runs verses together, e.g. Jubilees 5
    carries "27. ... days. 28. And the ark went ..." in a single <p>, and
    Jubilees 27:1-13 arrive as one block. Splitting is driven strictly by the
    *next expected* verse number, so an incidental numeral in the prose cannot
    trigger a spurious break.
    """
    pieces: list[list] = []
    current, buffer = first_num, text
    while True:
        nxt = current + 1
        match = re.search(
            r"\s" + str(nxt) + r"\s*[.,:;]\s+(?=[A-Z“(\[†])", buffer
        )
        if not match:
            break
        pieces.append([current, buffer[: match.start()].strip()])
        buffer = buffer[match.end():].strip()
        current = nxt
    pieces.append([current, buffer.strip()])
    return pieces


class Collector:
    """Accumulates chapters and verses, preserving Charles's own numbering."""

    def __init__(self) -> None:
        self.prologue: list[str] = []
        self.colophon: str | None = None
        self.chapters: dict[int, list[list]] = {}
        self.anomalies: list[str] = []
        self._chapter: int | None = None
        self._verses: list[list] | None = None
        self._pending_gloss: str | None = None

    # -- gloss handling -------------------------------------------------
    def hold_gloss(self, text: str) -> None:
        # Charles's marginal Anno Mundi dates are kept; the modern transcriber's
        # one-off expansion of the abbreviation is a note, so it is dropped.
        text = ABBREV_GLOSS_RE.sub("", text).strip()
        if not text:
            return
        self._pending_gloss = (
            text if not self._pending_gloss else f"{self._pending_gloss} {text}"
        )

    def _take_gloss(self, inline: str | None) -> str:
        parts = [p for p in (f"({inline})" if inline else None,
                             self._pending_gloss) if p]
        self._pending_gloss = None
        return " ".join(parts)

    # -- structure ------------------------------------------------------
    def open_chapter(self, number: int) -> None:
        self._chapter = number
        self._verses = self.chapters.setdefault(number, [])

    def add_verse_block(self, number: int, text: str, inline_gloss: str = None) -> None:
        if self._chapter is None:
            self.open_chapter(1)
        assert self._verses is not None
        expected = self._verses[-1][0] + 1 if self._verses else 1
        if number != expected:
            self.anomalies.append(
                f"chapter {self._chapter}: expected verse {expected}, "
                f"found {number} ({text[:60]!r})"
            )
        gloss = self._take_gloss(inline_gloss)
        for index, (num, body) in enumerate(split_run_on_verses(text, number)):
            if index == 0 and gloss:
                body = f"{gloss} {body}".strip()
            self._verses.append([num, body])

    def add_continuation(self, text: str) -> None:
        """A paragraph with no verse number: poetry or a continued sentence."""
        if self._chapter is None:
            self.prologue.append(text)
            self._pending_gloss = None
            return
        assert self._verses is not None and self._verses
        gloss = self._take_gloss(None)
        expected = self._verses[-1][0] + 1
        pieces = split_run_on_verses(text, expected - 1)
        tail = " ".join(p for p in (gloss, pieces[0][1]) if p)
        self._verses[-1][1] = f"{self._verses[-1][1]} {tail}".strip()
        for num, body in pieces[1:]:
            self._verses.append([num, body])

    def validate(self) -> list[str]:
        problems = list(self.anomalies)
        for chapter in range(1, N_CHAPTERS + 1):
            verses = self.chapters.get(chapter)
            if not verses:
                problems.append(f"chapter {chapter}: no verses recovered")
                continue
            numbers = [v[0] for v in verses]
            gaps = sorted(set(range(1, numbers[-1] + 1)) - set(numbers))
            if gaps:
                problems.append(
                    f"chapter {chapter}: verse numbers absent from source: "
                    + ", ".join(str(g) for g in gaps)
                )
        return problems


# --------------------------------------------------------------------------
# Primary parser: globalgreyebooks HTML
# --------------------------------------------------------------------------

def paragraph_text(tag) -> str:
    """Text of a <p>, with footnote references removed."""
    tag = copy.copy(tag)
    for junk in tag.find_all(["a", "sup"]):
        junk.decompose()
    return normalise(tag.get_text(" ", strip=True))


def parse_primary(markup: str) -> Collector:
    soup = BeautifulSoup(markup, "html.parser")

    article = soup.find("article", class_="reading-body")
    if article is None:
        article = soup.find(
            lambda t: t.name in ("article", "div", "section")
            and t.get("class")
            and "reading-body" in t.get("class")
        )
    if article is None:
        raise RuntimeError("primary source: could not locate the reading-body element")

    blocks = [child for child in article.children if getattr(child, "name", None)]

    # The body starts at the Prologue heading. Everything before it is the
    # publisher's front matter, Charles's Introduction, and his table of
    # abbreviations; everything from the trailing <hr> on is the footnote
    # apparatus and the indices.
    start = next(
        (i for i, b in enumerate(blocks)
         if b.name in ("h1", "h2", "h3") and "prologue" in b.get_text().lower()),
        None,
    )
    if start is None:
        raise RuntimeError("primary source: could not locate the Prologue heading")
    end = next((i for i, b in enumerate(blocks) if b.name in ("hr", "footer")),
               len(blocks))
    if end <= start:
        raise RuntimeError("primary source: body delimiters are out of order")
    print(f"  body spans blocks {start + 1}..{end - 1} of {len(blocks)}")

    collector = Collector()
    for block in blocks[start + 1:end]:
        if block.name != "p":
            continue  # in-chapter section headings are Charles's editor's, not text
        text = paragraph_text(block)
        if not text:
            continue

        if BACK_MATTER_RE.match(text):
            continue
        if COLOPHON_RE.match(text):
            collector.colophon = text
            continue

        if CHRON_ONLY_RE.match(text):
            collector.hold_gloss(text)
            continue

        chapter_match = CHAPTER_RE.match(text)
        if chapter_match:
            collector.open_chapter(ROMAN_TO_INT[chapter_match.group("roman")])
            remainder = text[chapter_match.end():]
            # A chapter opener may or may not restate "1."
            verse_match = VERSE_RE.match(remainder)
            if verse_match:
                num = verse_match.group("num") or verse_match.group("num2")
                if num == "1":
                    remainder = remainder[verse_match.end():]
            collector.add_verse_block(1, remainder, chapter_match.group("gloss"))
            continue

        verse_match = VERSE_RE.match(text)
        if verse_match:
            num = int(verse_match.group("num") or verse_match.group("num2"))
            collector.add_verse_block(
                num, text[verse_match.end():], verse_match.group("gloss")
            )
        else:
            collector.add_continuation(text)

    return collector


# --------------------------------------------------------------------------
# Fallback parser: archive.org djvu OCR
# --------------------------------------------------------------------------

def _dehyphenate(text: str) -> str:
    """Rejoin words the scan broke across lines ("command- \\nment")."""
    return re.sub(r"(\w)-\s*\n\s*(\w)", r"\1\2", text)


def parse_fallback(markup: str) -> Collector:
    """Best-effort recovery from the OCR scan.

    The scan interleaves body text with Charles's commentary, so segmentation is
    driven purely by the next expected marker: a chapter's Roman numeral, then
    that chapter's verse numbers in order. Anything the scanner mixed in between
    is swept into the verse it interrupts, and chapters whose opener is never
    found are reported so the caller can emit a MISSING marker. This path is a
    safety net for an unreachable primary, not an equal-quality source.
    """
    soup = BeautifulSoup(markup, "html.parser")
    pre = soup.find("pre")
    text = _dehyphenate(html.unescape(pre.get_text() if pre else markup))
    text = unicodedata.normalize("NFC", text)

    anchor = text.find("history of the division of the days")
    if anchor == -1:
        raise RuntimeError("fallback source: could not locate the Prologue")
    body = text[anchor:]

    collector = Collector()

    # Locate each chapter opener in order: "I." ... "L." at a line or sentence
    # start, each one appearing after the previous.
    offsets: dict[int, int] = {}
    cursor = 0
    for chapter in range(1, N_CHAPTERS + 1):
        pattern = re.compile(
            r"(?:^|\n)\s*(?:CHAPTER\s+)?" + _roman(chapter) + r"\.\s+(?=[A-Z“])"
        )
        match = pattern.search(body, cursor)
        if not match:
            continue
        offsets[chapter] = match.end()
        cursor = match.end()

    prologue = normalise(body[: min(offsets.values())]) if offsets else ""
    if prologue:
        collector.prologue.append(prologue)

    found = sorted(offsets)
    for index, chapter in enumerate(found):
        stop = offsets[found[index + 1]] if index + 1 < len(found) else len(body)
        chunk = normalise(body[offsets[chapter]:stop])
        collector.open_chapter(chapter)
        # Verse 1 runs to the first "2.", and so on.
        for num, verse in split_run_on_verses(chunk, 1):
            collector.chapters[chapter].append([num, verse])

    missing = [c for c in range(1, N_CHAPTERS + 1) if c not in offsets]
    for chapter in missing:
        collector.anomalies.append(
            f"chapter {chapter}: opener not found in OCR scan"
        )
    return collector


# --------------------------------------------------------------------------
# Rendering
# --------------------------------------------------------------------------

def render_text_section(collector: Collector) -> str:
    """Everything that follows the "## Text" marker."""
    lines: list[str] = []

    if collector.prologue:
        lines += ["", "### Prologue", ""]
        for paragraph in collector.prologue:
            lines += [paragraph, ""]

    for chapter in range(1, N_CHAPTERS + 1):
        lines += ["", f"## Chapter {chapter}", ""]
        verses = collector.chapters.get(chapter)
        if not verses:
            lines += [
                f"> **MISSING:** chapter {chapter} could not be retrieved from source",
                "",
            ]
            continue
        for number, body in verses:
            lines += [f"**{number}** {body}".strip(), ""]

    if collector.colophon:
        lines += ["", collector.colophon, ""]

    # Collapse the blank line that "" + "## Chapter" pairs introduce.
    out = "\n".join(lines)
    return re.sub(r"\n{3,}", "\n\n", out).rstrip() + "\n"


def rebuild_document(existing: str, collector: Collector) -> str:
    """Preserve the front matter, heading, metadata table and notes verbatim."""
    marker = re.search(r"^" + re.escape(TEXT_MARKER) + r"\s*$", existing, re.MULTILINE)
    if not marker:
        raise RuntimeError(f"{TARGET}: '{TEXT_MARKER}' marker not found")
    head = existing[: marker.end()]
    return head + "\n" + render_text_section(collector)


# --------------------------------------------------------------------------
# Reporting
# --------------------------------------------------------------------------

def report(collector: Collector) -> int:
    """Print per-chapter statistics. Returns the number of flagged chapters."""
    print()
    print("Chapter word / verse counts")
    print("---------------------------")
    print(f"{'Ch':>3}  {'Verses':>6}  {'Words':>7}  Flag")

    total_words = total_verses = 0
    thin: list[tuple[int, int]] = []
    missing: list[int] = []

    for chapter in range(1, N_CHAPTERS + 1):
        verses = collector.chapters.get(chapter, [])
        words = sum(len(v[1].split()) for v in verses)
        total_words += words
        total_verses += len(verses)
        flag = ""
        if not verses:
            flag = "*** MISSING ***"
            missing.append(chapter)
        elif words < MIN_CHAPTER_WORDS:
            flag = f"*** UNDER {MIN_CHAPTER_WORDS} WORDS ***"
            thin.append((chapter, words))
        print(f"{chapter:>3}  {len(verses):>6}  {words:>7}  {flag}")

    print("---------------------------")
    print(f"Total chapters : {sum(1 for c in range(1, N_CHAPTERS + 1) if collector.chapters.get(c))}/{N_CHAPTERS}")
    print(f"Total verses   : {total_verses}")
    print(f"Total words    : {total_words:,}")
    if total_verses:
        print(f"Mean words/ch  : {total_words / N_CHAPTERS:.0f}")

    problems = collector.validate()
    if problems:
        print()
        print("Source notes (verse numbers are reproduced as Charles has them):")
        for problem in problems:
            print(f"  - {problem}")

    if thin or missing:
        print()
        print("FLAGGED — the summary-scrape bug may have recurred:")
        for chapter, words in thin:
            print(f"  - chapter {chapter}: {words} words (< {MIN_CHAPTER_WORDS})")
        for chapter in missing:
            print(f"  - chapter {chapter}: missing entirely")
    else:
        print()
        print(f"OK: all {N_CHAPTERS} chapters present, none under {MIN_CHAPTER_WORDS} words.")

    return len(thin) + len(missing)


# --------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--dry-run", action="store_true",
                        help="parse and report without writing anything")
    parser.add_argument("--cache", type=Path, default=None,
                        help="directory used to cache downloaded pages")
    parser.add_argument("--source", choices=("auto", "primary", "fallback"),
                        default="auto", help="which source to use (default: auto)")
    args = parser.parse_args()

    if not TARGET.exists():
        print(f"error: {TARGET} does not exist", file=sys.stderr)
        return 1
    existing = TARGET.read_text(encoding="utf-8")

    collector: Collector | None = None
    used = ""

    if args.source in ("auto", "primary"):
        print("Primary source: globalgreyebooks.com")
        try:
            collector = parse_primary(fetch(PRIMARY_URL, args.cache))
            used = PRIMARY_URL
            recovered = sum(1 for c in collector.chapters.values() if c)
            print(f"  recovered {recovered}/{N_CHAPTERS} chapters")
            if recovered == 0:
                raise RuntimeError("primary source yielded no chapters")
        except Exception as exc:
            print(f"  primary source failed: {exc}", file=sys.stderr)
            collector = None
            if args.source == "primary":
                return 1

    if collector is None and args.source in ("auto", "fallback"):
        print("Fallback source: archive.org OCR scan")
        try:
            collector = parse_fallback(fetch(FALLBACK_URL, args.cache))
            used = FALLBACK_URL
            recovered = sum(1 for c in collector.chapters.values() if c)
            print(f"  recovered {recovered}/{N_CHAPTERS} chapters")
        except Exception as exc:
            print(f"  fallback source failed: {exc}", file=sys.stderr)
            return 1

    if collector is None:
        print("error: no source could be parsed", file=sys.stderr)
        return 1

    document = rebuild_document(existing, collector)
    flagged = report(collector)
    print(f"\nSource used: {used}")

    if args.dry_run:
        print("--dry-run: no files written")
        return 0

    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    BACKUP.write_text(existing, encoding="utf-8")
    print(f"Backed up  : {BACKUP.relative_to(REPO_ROOT)} "
          f"({len(existing.split())} words)")

    TARGET.write_text(document, encoding="utf-8")
    print(f"Rewrote    : {TARGET.relative_to(REPO_ROOT)} "
          f"({len(document.split())} words)")

    return 1 if flagged else 0


if __name__ == "__main__":
    sys.exit(main())
