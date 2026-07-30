# Manual Review — OCR pass 1

Everything in this file was **deliberately left unchanged** by
`scripts/clean_ocr.py`. Line numbers refer to the files as they stand after
pass 1. Nothing here has been corrected, moved, or rewritten.

Three categories, per the pass-1 brief: suspected OCR misspellings,
footnote locations, and the introduction/sacred-text boundary.

## 1. Suspected OCR misspellings

### The `lo` / `ao` class — marginal line numbers absorbed at line *start*

This is the largest single class and it is the mirror image of Step 1. Where
Step 1 finds a marginal number absorbed at the **end** of a line, these are
marginal numbers absorbed at the **start** of a line and then misread as
letters: `lo` is the printed **10**, `ao` is the printed **20**. Two examples,
both from `80-serata-seyon.md`:

```
258  lo not accept the person of a rich man in case of his being
420  ao over the poor and needy, nor respect the person of the
```

Neither sentence begins with a word; the leading token is a page number.
Correcting these means **deleting** the token, not respelling it — but they
are out of scope for pass 1 because the rule would have to distinguish them
from the genuine English `lo` (*lo, they who are on the right take…*, line 337
of the same file) and from Greek/Latin fragments in `86-qalementos.md`.

### Single-occurrence cases, with exact locations

The `lo` / `ao` class is indexed separately below, being too numerous for
this table. Everything else, brief-named or not:

| File | Line | Reads | Should read | Named in brief | Why |
|---|---:|---|---|:-:|---|
| `80-serata-seyon.md` | 57 | `K^fas` | `Kefas` | yes | 'e' read as '^' |
| `80-serata-seyon.md` | 57 | `K^f` | `(letter unknown)` | — | caret substituted for a letter |
| `80-serata-seyon.md` | 296 | `P^t` | `(letter unknown)` | — | caret substituted for a letter |
| `80-serata-seyon.md` | 630 | `g^n` | `(letter unknown)` | — | caret substituted for a letter |
| `80-serata-seyon.md` | 756 | `g^i` | `(letter unknown)` | — | caret substituted for a letter |
| `80-serata-seyon.md` | 786 | `g^r` | `(letter unknown)` | — | caret substituted for a letter |
| `80-serata-seyon.md` | 887 | `i^t` | `(letter unknown)` | — | caret substituted for a letter |
| `80-serata-seyon.md` | 888 | `i^t` | `(letter unknown)` | — | caret substituted for a letter |
| `81-teezaz.md` | 65 | `pnayer` | `prayer` | yes | 'r' read as 'n' |
| `81-teezaz.md` | 206 | `t^n` | `(letter unknown)` | — | caret substituted for a letter |
| `81-teezaz.md` | 249 | `g^v` | `(letter unknown)` | — | caret substituted for a letter |
| `81-teezaz.md` | 405 | `g^a` | `(letter unknown)` | — | caret substituted for a letter |
| `81-teezaz.md` | 734 | `b^y` | `(letter unknown)` | — | caret substituted for a letter |
| `81-teezaz.md` | 739 | `b^i` | `(letter unknown)` | — | caret substituted for a letter |
| `81-teezaz.md` | 813 | `g^v` | `(letter unknown)` | — | caret substituted for a letter |
| `81-teezaz.md` | 1070 | `g^v` | `(letter unknown)` | — | caret substituted for a letter |
| `81-teezaz.md` | 1161 | `g^v` | `(letter unknown)` | — | caret substituted for a letter |
| `81-teezaz.md` | 1307 | `g^v` | `(letter unknown)` | — | caret substituted for a letter |
| `81-teezaz.md` | 1497 | `g^c` | `(letter unknown)` | — | caret substituted for a letter |
| `81-teezaz.md` | 1713 | `g^a` | `(letter unknown)` | — | caret substituted for a letter |
| `81-teezaz.md` | 3128 | `r^e` | `(letter unknown)` | — | caret substituted for a letter |
| `84-mashafa-kidan-1.md` | 47 | `Ir came` | `It came` | — | drop-capital 'It' read as 'Ir' |
| `86-qalementos.md` | 55 | `Buck` | `Buch` | yes | German 'Buch' misread |
| `86-qalementos.md` | 55 | `Schriflen` | `Schriften` | — | German 'Schriften', 't' read as 'l' |
| `86-qalementos.md` | 57 | `Güttingen` | `Göttingen` | yes | German 'Göttingen' misread |
| `86-qalementos.md` | 57 | `185$` | `1858` | yes | '$' for a final digit |
| `86-qalementos.md` | 91 | `Bush Museum` | `British Museum` | — | 'British' read as 'Bush' |
| `87-didascalia.md` | 48 | `WOLY` | `HOLY` | — | 'H' read as 'W' |
| `87-didascalia.md` | 61 | `shecp` | `sheep` | — | 'e' read as 'c' |
| `87-didascalia.md` | 978 | `ETEHIOPIC` | `ETHIOPIC` | — | running-head title corrupted |
| `87-didascalia.md` | 1077 | `EVTIIOPIC` | `ETHIOPIC` | — | running-head title corrupted |
| `87-didascalia.md` | 1170 | `ETHLOPIC` | `ETHIOPIC` | — | running-head title corrupted |
| `87-didascalia.md` | 1263 | `EVIIOPIC` | `ETHIOPIC` | — | running-head title corrupted |
| `87-didascalia.md` | 5245 | `EYTHIOPIC` | `ETHIOPIC` | — | running-head title corrupted |
| `87-didascalia.md` | 6252 | `ETINOPIC` | `ETHIOPIC` | — | running-head title corrupted |
| `87-didascalia.md` | 7027 | `ETIHOPIC` | `ETHIOPIC` | — | running-head title corrupted |
| `87-didascalia.md` | 7346 | `ETIHOPIC` | `ETHIOPIC` | — | running-head title corrupted |
| `87-didascalia.md` | 7392 | `EQYHLOPIC` | `ETHIOPIC` | — | running-head title corrupted |
| `87-didascalia.md` | 7487 | `EVHIOPIC` | `ETHIOPIC` | — | running-head title corrupted |

### Full occurrence index

| File | Pattern | Count | Lines |
|---|---|---:|---|
| `80-serata-seyon.md` | `K^fas` | 1 | 57 |
| `80-serata-seyon.md` | `ao` | 6 | 142, 420, 538, 654, 829, 870 |
| `80-serata-seyon.md` | `caret-for-letter` | 7 | 57, 296, 630, 756, 786, 887-888 |
| `80-serata-seyon.md` | `lo` | 7 | 220, 258, 337, 565, 642, 778, 935 |
| `81-teezaz.md` | `ao` | 21 | 67, 184, 431, 590, 626, 662, 701, 736, 851, 1116, 1386, 1612, 1702, 1979, 2093, 2463, 2581, 3050, 3133, 3207, 3243 |
| `81-teezaz.md` | `caret-for-letter` | 12 | 206, 249, 405, 734, 739, 813, 1070, 1161, 1307, 1497, 1713, 3128 |
| `81-teezaz.md` | `lo` | 46 | 49, 101, 136, 248, 360, 411, 616, 654, 689, 764, 914, 989, 1028, 1179, 1375, 1447, 1487, 1524, 1598, 1645, 1686, 1809, 1894, 1968, 2003, 2038, 2079, 2120, 2161, 2200, 2331, 2452, 2566, 2652, 2659-2660, 2691, 2728, 2764, 2840, 2877, 3037, 3079, 3118, 3195, 3233 |
| `81-teezaz.md` | `pnayer` | 1 | 65 |
| `84-mashafa-kidan-1.md` | `Ir came` | 1 | 47 |
| `84-mashafa-kidan-1.md` | `lo` | 1 | 1787 |
| `86-qalementos.md` | `185$` | 1 | 57 |
| `86-qalementos.md` | `Buck` | 1 | 55 |
| `86-qalementos.md` | `Bush Museum` | 1 | 91 |
| `86-qalementos.md` | `Göttingen` | 1 | 57 |
| `86-qalementos.md` | `Schriflen` | 1 | 55 |
| `86-qalementos.md` | `ao` | 7 | 2761, 2811, 5450, 5457, 5491, 6214, 8612 |
| `86-qalementos.md` | `lo` | 16 | 2831, 4218, 5674, 5677, 5686, 5689, 5729, 5789, 5982, 6287, 6290, 6300, 6303, 7505, 9103, 9739 |
| `87-didascalia.md` | `DIDASCALIA-head` | 10 | 978, 1077, 1170, 1263, 5245, 6252, 7027, 7346, 7392, 7487 |
| `87-didascalia.md` | `WOLY` | 1 | 48 |
| `87-didascalia.md` | `shecp` | 1 | 61 |

This index is a floor, not a census. It reports what the patterns above
match; the OCR of these six volumes is noisy throughout and misspellings
without a distinctive shape (a wrong letter that still forms a word) cannot
be found by rule at all.

## 2. Footnotes

Two things to relocate, and they are separate problems.

**Markers** are printed superscripts that the OCR flattened into stray
symbols glued to a word or to punctuation — `®`, `¢`, `’`, `°`, `*`. From
`87-didascalia.md` line 50: *We,? the Twelve Apostles, ministers of His*
*only-* — the `?` is footnote 2. From `84-mashafa-kidan-1.md` line 48:
*and was handled ® by Thomas*. Because the same characters are also
legitimate apostrophes and quotation marks, the counts below are heuristic
and will over-report.

**Bodies** are the printed apparatus at the foot of each page, which the
scraper left inline in the middle of the sacred text. In `87-didascalia.md`
they arrive as two interleaved columns, which is why they are unreadable:

```
68  1 A. adds: Their prayer and * P this one city.
69  their blessing, and the mercy of “P this right faith. We
70  their God be with their beloved hive appointed.
```

That is footnote 1 and footnote 3 printed side by side, read across instead
of down. Reassembling them needs column detection and is well outside a
noise-removal pass.

A third, related artifact: **running page heads**. `87-didascalia.md` carries
`2 THE ETHIOPIC DIDASCALIA` (line 76), `THE ETHIOPIC DIDASCALIA 3` (line 122) and so on every
few pages. `86-qalementos.md` carries the same thing in French:

- line 669: `MANUSCRITS COPTES. 87`
- line 123: `74 REVUE DE L'ORIENT CHRÉTIEN.`
- line 511: `LITTÉRATURE ÉTIHIOPIENNE PSEUDO-CLÉMENTINE. 83`

These sit on their own line and are pure page furniture. They are also the
reason tier B of Step 1 exists: the number on such a line is a page number,
and deleting it alone would leave the head text stranded in the text.

| File | Footnote markers (lines) | Footnote bodies (lines) | Running heads (lines) |
|---|---:|---:|---:|
| `80-serata-seyon.md` | 3 | 5 | 15 |
| `81-teezaz.md` | 8 | 27 | 63 |
| `82-gessew.md` | 0 | 5 | 8 |
| `84-mashafa-kidan-1.md` | 427 | 439 | 18 |
| `86-qalementos.md` | 585 | 85 | 191 |
| `87-didascalia.md` | 718 | 293 | 175 |

### `80-serata-seyon.md`

- **Footnote bodies** (5): 348, 403, 648, 713, 883
- **Running heads** (15): 79, 157, 244, 324, 395, 477, 551, 591, 627, 725, 767, 804, 847, 885, 923
- **Marker lines** (3): 209, 765, 813

### `81-teezaz.md`

- **Footnote bodies** (27): 283, 366, 542, 610, 758, 769, 908, 983, 1013, 1085, 1135, 1141, 1146, 1152, 1298, 1322, 1468, 1547, 1924, 1948, 2020, 2665, 2745, 2861, 2970, 3032, 3061
- **Running heads** (63): 91, 125, 163, 197, 271, 347, 391, 568, 715, 791, 866, 902, 977, 1053, 1093, 1128, 1585, 1674, 1716, 1758, 1798, 1835, 1918, 1957, 1991, 2065, 2108, 2148, 2226, 2269, 2314, 2359, 2440, 2477, 2517, 2553, 2681, 2754, 2788, 2829, 2864, 2888, 2902, 2916, 2945, 2954, 2977, 2983, 3003, 3026, 3028, 3054, 3081, 3083, 3105, 3120, 3146, 3148, 3180, 3186, 3215, 3258, 3270
- **Marker lines** (8): 724, 1060, 1596, 1622, 1933, 1988, 2899, 3087

### `82-gessew.md`

- **Footnote bodies** (5): 104, 226, 339, 464, 571
- **Running heads** (8): 104, 162, 226, 284, 339, 399, 464, 571

### `84-mashafa-kidan-1.md`

- **Footnote bodies** (439): 61, 63, 70, 75, 80, 114, 119, 129, 171, 176, 178, 184, 186, 190, 220-221, 241, 272, 274, 282, 284-285, 288, 290, 293, 296-297, 306, 308, 332-333, 335, 344-346, 348, 351-353, 356, 386, 393, 400, 402, 405, 410, 415, 452, 454, 458, 466, 468-469, 471, 503-506, 509-510, 512-513, 515, 542, 546, 550, 552, 555, 565, 568, 572, 574, 608, 610, 612, 618, 623, 626, 628-629 …
- **Running heads** (18): 1583, 1828, 2095, 2355, 2447, 2559, 2873, 3082, 3125, 3146, 3168, 3268, 3552, 3621, 3889, 4192, 4211, 4295
- **Marker lines** (427): 49, 52-53, 59, 88-89, 94-95, 100, 116, 147, 149, 151-152, 155, 159, 171, 198, 200, 206, 241-242, 246, 251, 253-254, 258, 261, 267, 280, 293, 310-315, 317-318, 322 …

### `86-qalementos.md`

- **Footnote bodies** (85): 111-112, 123, 204, 212, 266, 462, 624, 714, 803, 888, 961, 1041, 1130, 2007, 2096, 2189, 2282, 2379, 2381, 2495, 2591, 2732, 2754, 2823, 2864, 2888, 3024, 3052, 3096, 3394, 3636, 3675, 3687, 3805, 3939, 3992, 4270, 4279, 4298, 4303, 4361, 4523, 4607, 4649, 4689, 4699, 4771, 4848, 4922, 4998, 5077, 5452, 5520, 5693, 5747, 5755, 5931, 6100, 6189, 6271, 6356, 6455, 6525, 6550, 6651, 6700, 8009, 8473, 8641, 8667, 9014, 9125, 9202, 9613, 9666, 9759, 9796, 10142, 10568 …
- **Running heads** (191): 49, 123, 204, 301, 305, 308, 379, 460, 462, 552, 597-598, 600, 603, 605, 624, 655, 669, 714, 720, 758, 803, 842, 864, 888, 931, 933, 961, 988, 1002, 1041, 1087, 1128, 1130, 1171, 1220, 1307, 1399, 1495, 1585, 1587, 1684, 1864, 2007, 2189, 2381, 2591, 2642, 2644, 2685, 2821, 2850, 2948, 3006, 3012, 3055, 3076, 3139, 3198, 3310, 3312, 3315, 3335, 3394, 3444, 3468, 3687, 3840, 3924, 4002, 4106, 4149, 4229, 4330, 4334-4335, 4361, 4443, 4482, 4521 …
- **Marker lines** (585): 43, 67, 91, 100, 102, 109, 113, 131-132, 134-135, 140, 147-148, 150, 159-160, 171, 174, 184, 187, 196, 198, 211, 217, 226, 232, 234, 242, 246, 250, 256, 262, 268, 272, 291, 315, 327, 335, 344 …

### `87-didascalia.md`

- **Footnote bodies** (293): 68, 74, 76, 115, 120, 163, 171, 259-260, 264, 344, 346, 352, 354, 365, 408, 455, 497, 543, 547, 584-585, 587, 627, 639, 684, 731, 738, 776, 778, 829, 874, 877-878, 920, 923, 928, 970, 1024, 1027, 1125, 1207, 1210, 1218, 1253, 1255, 1257, 1259, 1261, 1296, 1305, 1308, 1310, 1337, 1342, 1394, 1478, 1480, 1488, 1521, 1580-1581, 1584, 1624, 1677, 1690, 1778, 1780, 1817-1818, 1821-1822, 1876, 1882, 1972, 2073, 2157, 2165, 2203, 2257 …
- **Running heads** (175): 46, 48, 76, 122, 171, 217, 264, 308, 365, 411, 455, 547, 592, 639, 689, 738, 783, 829, 880, 928, 978, 1027, 1077, 1125, 1170, 1263, 1310, 1344, 1394, 1441, 1488, 1535, 1584, 1627, 1690, 1738, 1780, 1826, 1882, 1972, 2021, 2073, 2115, 2165, 2213, 2301, 2346, 2494, 2545, 2594, 2642, 2688, 2740, 2784, 2832, 2878, 2985, 3038, 3083, 3132, 3178, 3239, 3285, 3335, 3368, 3445, 3488, 3537, 3583, 3627, 3664, 3755, 3800, 3849, 3896, 3943, 3986, 4061, 4106, 4151 …
- **Marker lines** (718): 57, 108, 112, 133, 148, 152, 155, 157, 161, 164, 174, 179, 189, 197, 220, 231-232, 240, 248, 251, 254, 274, 279, 294, 319, 321, 326, 341, 360, 380, 387, 414, 418, 424, 427, 429, 435, 440-441, 459 …

## 3. Introduction / sacred-text boundary

Only one of the six files actually has a translator's introduction inside
`## Text`. The other five begin with sacred text; what precedes it is the
repository's own front matter, Metadata table and Notes, which are correct
where they are.

| File | Sacred text begins | Detail |
|---|---:|---|
| `80-serata-seyon.md` | 43 | No translator introduction. `## Text` is followed immediately by the Sinodos incipit, *In the name of the Father…*. What precedes it is the repository's own Metadata table and Notes. |
| `81-teezaz.md` | 45 | No translator introduction. The file opens mid-work at `## Statute 31` — it is the continuation of the Sinodos begun in `80-serata-seyon.md`, whose statutes run 1-30. |
| `82-gessew.md` | 45 | No translator introduction. `## Preamble` is itself sacred text — the incipit *In the name of the Father…*. |
| `84-mashafa-kidan-1.md` | 47 | No translator introduction. Sacred text begins under `## Prologue` with *Ir came to pass, after our Lord rose from the dead…* (`Ir` is an OCR failure of the drop-capital `It`). Editorial matter does appear below, but as **footnotes**, not as a prefatory block — footnote 2, discussing Codex S. and the Copto-Arabic version, is at line 63. |
| `86-qalementos.md` | 97 | **The one file with a real translator introduction.** A blockquote note added by the repository's scraper sits just under `## Text`; Grébaut's own `INTRODUCTION` heading is at line 49 and his prefatory essay runs to line 96 — it cites Nau, Dillmann and the Tübingen manuscript and describes the seven Books. Sacred text begins at `# Livre Premier.`, with the incipit at line 102. Everything from 49 to 96 is Grébaut, not Qalementos, and should be moved out of `## Text` in a later pass. |
| `87-didascalia.md` | 46 | No translator introduction. `## Chapter 1` carries the work's own title as an `###` heading at line 44, and the sacred text begins with the invocation *IN THE NAME OF GOD THE FATHER ALMIGHTY…* (printed in small capitals, which the OCR preserved as literal capitals). |

## 4. Hyphens the de-hyphenation guard refused to join

`word-` at end of line is normally joined to the next line. The guard
refuses when the continuation fragment is a whole English word and the
joined form is not attested anywhere in the six files — see *Step 2a* in
`CLEANING_REPORT.md`. Refusing is not repairing: each line below still
carries a hyphen that an editor has to resolve, and most of them are
two-column footnote interleaving, where the true continuation is further
down the page in the other column.

| File | Line | Reads | Correct reading |
|---|---:|---|---|
| `87-didascalia.md` | 1861 | `trans-` / `children` | `translator` — continuation `lator` is in the next column |
| `87-didascalia.md` | 3209 | `cor-` / `right` | `correct` — continuation `rect` is in the next column |
| `87-didascalia.md` | 4386 | `money-` / `its` | `money-changers` — continuation `changers` is in the next column |
| `87-didascalia.md` | 5977 | `Xan-` / `month` | `Xanthicus` — continuation `thicus` is in the next column |
| `87-didascalia.md` | 7472 | `per-` / `you` | `pernicious` — continuation `nicious` is in the next column |

Three further joins the guard caught have already been resolved and are
no longer in this list, because `HELD_JOIN_REPAIRS` in the script now
performs the correct merge: `blue-black` (a colour compound, hyphen
kept), `this type` (two words) and `Phari the bishop` (a manuscript
variant inside a footnote).

## 5. Step 1 deletions to re-examine

Tier A means the classifier saw ordinary prose before the number. It has
no rule for `fol.`, for French `l'an`, or for Greek `ἀριθμόν`, so a few
numbers that are content rather than marginal furniture were sorted into
Tier A and deleted with the approved batch. They are listed here so the
next pass can restore them; all are in the French Qalementos.

| File | Line | Deleted | What it probably was | Confidence |
|---|---:|---:|---|---|
| `86-qalementos.md` | 7818 | `60` | the second half of a folio range, `fol. 59 v° b à fol. 60` | high |
| `86-qalementos.md` | 6737 | `10` | a year — *died in the month of Shawwal of the year 10* | high |
| `86-qalementos.md` | 10018 | `150` | Greek ὑπ’ ἀριθμὸν 150, *under catalogue number 150* | high |
| `86-qalementos.md` | 10222 | `160` | Greek ἀριθμόν 160, *number 160* | high |
| `86-qalementos.md` | 6213 | `550` | too large for a printer's margin, which runs 5–50 | medium |
| `86-qalementos.md` | 6203 | `230` | too large for a printer's margin | medium |
| `86-qalementos.md` | 6835 | `430` | too large for a printer's margin; the line is OCR wreckage | medium |
| `86-qalementos.md` | 9182 | `255` | too large for a printer's margin | medium |

