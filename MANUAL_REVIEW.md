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
| `80-serata-seyon.md` | 633 | `g^n` | `(letter unknown)` | — | caret substituted for a letter |
| `80-serata-seyon.md` | 759 | `g^i` | `(letter unknown)` | — | caret substituted for a letter |
| `80-serata-seyon.md` | 789 | `g^r` | `(letter unknown)` | — | caret substituted for a letter |
| `80-serata-seyon.md` | 890 | `i^t` | `(letter unknown)` | — | caret substituted for a letter |
| `80-serata-seyon.md` | 891 | `i^t` | `(letter unknown)` | — | caret substituted for a letter |
| `81-teezaz.md` | 65 | `pnayer` | `prayer` | yes | 'r' read as 'n' |
| `81-teezaz.md` | 207 | `t^n` | `(letter unknown)` | — | caret substituted for a letter |
| `81-teezaz.md` | 250 | `g^v` | `(letter unknown)` | — | caret substituted for a letter |
| `81-teezaz.md` | 407 | `g^a` | `(letter unknown)` | — | caret substituted for a letter |
| `81-teezaz.md` | 736 | `b^y` | `(letter unknown)` | — | caret substituted for a letter |
| `81-teezaz.md` | 741 | `b^i` | `(letter unknown)` | — | caret substituted for a letter |
| `81-teezaz.md` | 815 | `g^v` | `(letter unknown)` | — | caret substituted for a letter |
| `81-teezaz.md` | 1072 | `g^v` | `(letter unknown)` | — | caret substituted for a letter |
| `81-teezaz.md` | 1163 | `g^v` | `(letter unknown)` | — | caret substituted for a letter |
| `81-teezaz.md` | 1309 | `g^v` | `(letter unknown)` | — | caret substituted for a letter |
| `81-teezaz.md` | 1499 | `g^c` | `(letter unknown)` | — | caret substituted for a letter |
| `81-teezaz.md` | 1715 | `g^a` | `(letter unknown)` | — | caret substituted for a letter |
| `81-teezaz.md` | 3130 | `r^e` | `(letter unknown)` | — | caret substituted for a letter |
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
| `87-didascalia.md` | 5242 | `EYTHIOPIC` | `ETHIOPIC` | — | running-head title corrupted |
| `87-didascalia.md` | 6248 | `ETINOPIC` | `ETHIOPIC` | — | running-head title corrupted |
| `87-didascalia.md` | 7023 | `ETIHOPIC` | `ETHIOPIC` | — | running-head title corrupted |
| `87-didascalia.md` | 7342 | `ETIHOPIC` | `ETHIOPIC` | — | running-head title corrupted |
| `87-didascalia.md` | 7388 | `EQYHLOPIC` | `ETHIOPIC` | — | running-head title corrupted |
| `87-didascalia.md` | 7482 | `EVHIOPIC` | `ETHIOPIC` | — | running-head title corrupted |

### Full occurrence index

| File | Pattern | Count | Lines |
|---|---|---:|---|
| `80-serata-seyon.md` | `K^fas` | 1 | 57 |
| `80-serata-seyon.md` | `ao` | 6 | 142, 420, 540, 657, 832, 873 |
| `80-serata-seyon.md` | `caret-for-letter` | 7 | 57, 296, 633, 759, 789, 890-891 |
| `80-serata-seyon.md` | `lo` | 7 | 220, 258, 337, 567, 645, 781, 938 |
| `81-teezaz.md` | `ao` | 21 | 67, 185, 433, 592, 628, 664, 703, 738, 853, 1118, 1388, 1614, 1704, 1981, 2095, 2465, 2583, 3052, 3135, 3209, 3245 |
| `81-teezaz.md` | `caret-for-letter` | 12 | 207, 250, 407, 736, 741, 815, 1072, 1163, 1309, 1499, 1715, 3130 |
| `81-teezaz.md` | `lo` | 46 | 49, 102, 137, 249, 362, 413, 618, 656, 691, 766, 916, 991, 1030, 1181, 1377, 1449, 1489, 1526, 1600, 1647, 1688, 1811, 1896, 1970, 2005, 2040, 2081, 2122, 2163, 2202, 2333, 2454, 2568, 2654, 2661-2662, 2693, 2730, 2766, 2842, 2879, 3039, 3081, 3120, 3197, 3235 |
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
| `87-didascalia.md` | `DIDASCALIA-head` | 10 | 978, 1077, 1170, 1263, 5242, 6248, 7023, 7342, 7388, 7482 |
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

- **Footnote bodies** (5): 348, 403, 651, 716, 886
- **Running heads** (15): 79, 157, 244, 324, 395, 478, 553, 593, 630, 728, 770, 807, 850, 888, 926
- **Marker lines** (3): 209, 768, 816

### `81-teezaz.md`

- **Footnote bodies** (27): 284, 368, 544, 612, 760, 771, 910, 985, 1015, 1087, 1137, 1143, 1148, 1154, 1300, 1324, 1470, 1549, 1926, 1950, 2022, 2667, 2747, 2863, 2972, 3034, 3063
- **Running heads** (63): 91, 126, 164, 198, 272, 349, 393, 570, 717, 793, 868, 904, 979, 1055, 1095, 1130, 1587, 1676, 1718, 1760, 1800, 1837, 1920, 1959, 1993, 2067, 2110, 2150, 2228, 2271, 2316, 2361, 2442, 2479, 2519, 2555, 2683, 2756, 2790, 2831, 2866, 2890, 2904, 2918, 2947, 2956, 2979, 2985, 3005, 3028, 3030, 3056, 3083, 3085, 3107, 3122, 3148, 3150, 3182, 3188, 3217, 3260, 3272
- **Marker lines** (8): 726, 1062, 1598, 1624, 1935, 1990, 2901, 3089

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

- **Footnote bodies** (293): 68, 74, 76, 115, 120, 163, 171, 259-260, 264, 344, 346, 352, 354, 365, 408, 455, 497, 543, 547, 584-585, 587, 627, 639, 684, 731, 738, 776, 778, 829, 874, 877-878, 920, 923, 928, 970, 1024, 1027, 1125, 1207, 1210, 1218, 1253, 1255, 1257, 1259, 1261, 1296, 1305, 1308, 1310, 1337, 1342, 1394, 1478, 1480, 1488, 1521, 1580-1581, 1584, 1624, 1677, 1690, 1778, 1780, 1817-1818, 1821-1822, 1875, 1881, 1971, 2072, 2156, 2164, 2202, 2256 …
- **Running heads** (175): 46, 48, 76, 122, 171, 217, 264, 308, 365, 411, 455, 547, 592, 639, 689, 738, 783, 829, 880, 928, 978, 1027, 1077, 1125, 1170, 1263, 1310, 1344, 1394, 1441, 1488, 1535, 1584, 1627, 1690, 1738, 1780, 1826, 1881, 1971, 2020, 2072, 2114, 2164, 2212, 2300, 2345, 2493, 2544, 2593, 2641, 2687, 2739, 2783, 2831, 2877, 2984, 3037, 3082, 3131, 3177, 3237, 3283, 3333, 3366, 3443, 3486, 3535, 3581, 3625, 3662, 3753, 3798, 3847, 3894, 3941, 3984, 4059, 4104, 4149 …
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

