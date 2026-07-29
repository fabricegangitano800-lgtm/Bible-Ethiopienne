# Handoff — Book of Jubilees (45-jubilees.md) repair

> **Purpose of this file:** a bridge / handoff document between Claude sessions.
> It contains, verbatim and in full, the completion report produced when
> `scripts/fetch_jubilees.py` was written and run to repair
> `en/01-old-testament/06-ethiopian-ot/45-jubilees.md`.
> Branch: `fix/jubilees`. Date: 2026-07-29.
>
> Everything below the horizontal rule is the report reproduced word for word.

---

Done. `scripts/fetch_jubilees.py` fetched, parsed and rewrote the file from the primary source; the fallback was never needed.

## What was wrong and what fixed it

The primary source turned out to be well-structured: each verse is its own `<p>`, prefixed with Charles's verse number, and each chapter's first verse carries a Roman numeral. Body boundaries are clean — the Prologue heading starts it, the footnote `<hr>` ends it — so front matter, the Introduction, the abbreviations table, the notes and the indices are all excluded structurally rather than by guesswork.

Four things needed real handling:

- **Run-on verses.** The transcriber packs several verses into one `<p>` in places — Jubilees 5:27–28, and all of 27:1–13 as a single block. Splitting is driven strictly by the *next expected* verse number, so an incidental numeral in the prose can't trigger a false break. Without this, chapter 27 lost 12 verses.
- **Encoding.** Neither source sends a charset header, so `requests` falls back to ISO-8859-1 and mangles the curly quotes and Charles's transliterations (Lûbâr, Mastêmâ). Since verse splitting keys off `“`, that also silently broke chapter 27. Now decoded as UTF-8 explicitly.
- **Footnote refs.** `<a><sup>[n]</sup></a>` stripped by tag, not regex — Charles's own square brackets (`Sin[ai]`, `[(be) with thee, and]`) and his `†…†` critical marks are preserved.
- **Trailing matter.** The publisher's "THE END" is dropped; the book's closing colophon is set after chapter 50 rather than folded into 50:13.

Charles's marginal Anno Mundi dates are kept (they appear inline throughout anyway); the modern transcriber's one-off `(A.M. = Anno Mundi)` expansion is dropped as a note. The Prologue is rendered under `### Prologue` — it has no verse numbers, and this keeps all 50 `## Chapter N` headings intact.

## Report

All 50 chapters, verse numbers contiguous 1..N in every chapter, **no chapter under 150 words** — nearest is chapter 47 at 423. No MISSING markers.

| Ch | Verses | Words | | Ch | Verses | Words | | Ch | Verses | Words | | Ch | Verses | Words |
|---:|---:|---:|---|---:|---:|---:|---|---:|---:|---:|---|---:|---:|---:|
| 1 | 29 | 1449 | | 14 | 24 | 740 | | 27 | 27 | 1025 | | 40 | 13 | 561 |
| 2 | 33 | 1544 | | 15 | 34 | 1248 | | 28 | 30 | 1188 | | 41 | 28 | 951 |
| 3 | 35 | 1382 | | 16 | 31 | 1128 | | 29 | 20 | 741 | | 42 | 25 | 883 |
| 4 | 33 | 1516 | | 17 | 18 | 712 | | 30 | 26 | 1180 | | 43 | 24 | 898 |
| 5 | 32 | 1139 | | 18 | 19 | 680 | | 31 | 32 | 1358 | | 44 | 34 | 874 |
| 6 | 38 | 1605 | | 19 | 31 | 1008 | | 32 | 34 | 1298 | | 45 | 16 | 631 |
| 7 | 39 | 1487 | | 20 | 13 | 563 | | 33 | 23 | 878 | | 46 | 16 | 601 |
| 8 | 30 | 1431 | | 21 | 26 | 1069 | | 34 | 21 | 838 | | 47 | 12 | 423 |
| 9 | 15 | 607 | | 22 | 30 | 1302 | | 35 | 27 | 1235 | | 48 | 19 | 770 |
| 10 | 36 | 1381 | | 23 | 32 | 1364 | | 36 | 24 | 980 | | 49 | 23 | 1202 |
| 11 | 24 | 1048 | | 24 | 33 | 1200 | | 37 | 25 | 1028 | | 50 | 13 | 690 |
| 12 | 31 | 1194 | | 25 | 23 | 893 | | 38 | 24 | 636 | | | | |
| 13 | 29 | 1030 | | 26 | 35 | 1233 | | 39 | 18 | 629 | | | | |

- **Total verses: 1,307**
- **Total words: 51,447** (verse text; 53,136 for the whole file) — up from 2,311
- Mean 1,029 words/chapter, vs ~46 before

Per-chapter verse totals match Charles's standard counts on the ones worth checking (1→29, 5→32, 9→15, 27→27, 46→16, 50→13), which is independent confirmation the segmentation is right.

Verified: everything up to and including `## Text` is byte-identical to the previous version, and `backups/45-jubilees.md.bak` is a byte-exact copy of it.

Two things I did **not** do, since you said to keep the front matter exactly as-is — flagging them as your call:

- `source_url` still points at `https://sacred-texts.com/bib/jub/index.htm`, the TOC page that caused the bug. The text now comes from globalgreyebooks.
- `SOURCES.md` may want the same update.

Changes are on `fix/jubilees`, uncommitted (`45-jubilees.md` modified, `scripts/` and `backups/` untracked). Want me to commit?
