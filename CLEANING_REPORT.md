# Cleaning Report — OCR pass 1 (`clean/ocr-pass1`)

Produced by `scripts/clean_ocr.py`. Six files in scope, no others:

- `en/03-broader-canon/80-serata-seyon.md`
- `en/03-broader-canon/81-teezaz.md`
- `en/03-broader-canon/82-gessew.md`
- `en/03-broader-canon/84-mashafa-kidan-1.md`
- `en/03-broader-canon/86-qalementos.md`
- `en/03-broader-canon/87-didascalia.md`

Backups of all six, taken before any modification, are in `backups/`.

Step 1 (line-number deletion) applied: **NO — awaiting approval**.
Mode: **apply (files written)**.

## Summary

| File | Trailing-space lines stripped | Line numbers deleted | Line numbers pending | De-hyphen joins | Blank lines collapsed | Lines before → after |
|---|---:|---:|---:|---:|---:|---:|
| `80-serata-seyon.md` | 662 | 0 | 49 | 0 | 0 | 969 → 969 |
| `81-teezaz.md` | 2469 | 0 | 179 | 0 | 0 | 3272 → 3272 |
| `82-gessew.md` | 336 | 0 | 4 | 0 | 0 | 620 → 620 |
| `84-mashafa-kidan-1.md` | 0 | 0 | 87 | 89 | 0 | 4574 → 4485 |
| `86-qalementos.md` | 8628 | 0 | 161 | 662 | 0 | 11658 → 10996 |
| `87-didascalia.md` | 0 | 0 | 126 | 230 | 0 | 9463 → 9233 |

**Totals:** 12095 lines rstripped · 0 line numbers deleted · 606 pending approval · 981 joins · 0 blank lines collapsed.

## Step 0 — trailing whitespace

Runs first, because Steps 1 and 2 both key off the end-of-line character
and a trailing space hides it.

In `86-qalementos.md` 8,628 of 11,658 lines carried trailing whitespace. Before stripping it the file appeared to have zero hyphen line-breaks; afterwards it has 662. That is the whole reason for the ordering — run Step 2 first and this file silently cleans nothing.

| File | Lines with trailing whitespace | Total lines |
|---|---:|---:|
| `80-serata-seyon.md` | 662 | 969 |
| `81-teezaz.md` | 2,469 | 3,272 |
| `82-gessew.md` | 336 | 620 |
| `84-mashafa-kidan-1.md` | 0 | 4,574 |
| `86-qalementos.md` | 8,628 | 11,658 |
| `87-didascalia.md` | 0 | 9,463 |

## Step 1 — absorbed printer line numbers

Horner (1904) and Harden (1920) print marginal line numbers every 5 lines;
the scraper absorbed them at end of line. Detection requires all of:

1. the file contains no `**N**` verse markers — all six qualify;
2. a 1-3 digit number at end of line, preceded by whitespace;
3. the number is within 2 of a multiple of 5.

Condition 3 is **vacuous**: every integer is within 2 of a multiple of 5
(`n % 5` is 0, 1 or 2 — within 2 below — or 3 or 4 — within 2 above). It is
implemented as stated and it excludes nothing. The counts below are
therefore the counts of "any 1-3 digit number at end of line".

Two structural guards were added, without which this pass destroys the
chapter structure of all six files:

- **front matter and metadata** (everything up to `## Text`): `number: 82`
  and `chapters: 56` are indistinguishable from a marginal number;
- **headings**: `## Canon 1`, `## Statute 31`, `## Chapter 12` all end in a
  1-3 digit number preceded by whitespace. In `82-gessew.md` 55 of the 61
  matches are headings and only 4 are prose.

| File | Total matches | Headings | Front matter / metadata | Remaining |
|---|---:|---:|---:|---:|
| `80-serata-seyon.md` | 79 | 28 | 2 | 49 |
| `81-teezaz.md` | 221 | 40 | 2 | 179 |
| `82-gessew.md` | 61 | 55 | 2 | 4 |
| `84-mashafa-kidan-1.md` | 157 | 68 | 2 | 87 |
| `86-qalementos.md` | 163 | 0 | 2 | 161 |
| `87-didascalia.md` | 172 | 44 | 2 | 126 |

### Tiering of the remainder

A number at end of line is not automatically a marginal line number. Three
other things in these files match the rule exactly, so the remainder is
tiered and only tier A is recommended for deletion:

- **Tier A — prose.** A marginal number absorbed mid-sentence. This is the
  pass-1 target. `80-serata-seyon.md` line 48: *All hail, our sons and our*
  *daughters, in the name of* `5`. The 5/10/15/20 cadence is visible in the
  line numbers themselves.
- **Tier B — running page head.** The number is the page number on a running
  head that the scraper left inline: `THE ETHIOPIC DIDASCALIA 3`,
  `MANUSCRITS COPTES. 91`. Deleting just the number leaves the head text
  behind and removes the very evidence that identifies it, making the later
  whole-line fix harder. Recommended: leave for a running-head pass; they
  are indexed in `MANUAL_REVIEW.md`.
- **Tier C — risky.** The number is real content. Three sub-cases, all in
  `86-qalementos.md`: a folio citation `(F. 4` broken across lines (Grébaut
  cites `(F. 4 r° a)` throughout); a referring noun, *commence au feuillet*
  `151`; and an enumeration of manuscript pages, *244 à 246,* `259`.
  Recommended: never delete.

| File | Tier A prose | Tier B running head | Tier C risky | Tier A that is an exact multiple of 5 |
|---|---:|---:|---:|---:|
| `80-serata-seyon.md` | 44 | 5 | 0 | 44 |
| `81-teezaz.md` | 149 | 30 | 0 | 149 |
| `82-gessew.md` | 0 | 4 | 0 | 0 |
| `84-mashafa-kidan-1.md` | 9 | 64 | 14 | 1 |
| `86-qalementos.md` | 62 | 74 | 25 | 16 |
| `87-didascalia.md` | 39 | 83 | 4 | 4 |

### `80-serata-seyon.md` — 49 candidates

**Tier A — PROSE — absorbed marginal line number (the pass-1 target) (44)**

| Line | Number | Kind | 60 chars of preceding context |
|---:|---:|---|---|
| 48 | `5` | prose | `…All hail, our sons and our daughters, in the name of` |
| 57 | `10` | prose | `…Tomas and K^fas and Endreyas and Bartalomewos and` |
| 67 | `15` | prose | `…that every one of you may take his place according to` |
| 129 | `5` | prose | `…Said Petros : Thou shalt not kill life, and` |
| 133 | `10` | prose | `…shalt not cause abortion, nor after the child is born shalt` |
| 137 | `15` | prose | `…about doing evil, and thou shalt not be of double heart` |
| 154 | `30` | prose | `…or a lover of fighting, because this depraves and causes` |
| 231 | `30` | prose | `…Said Tom§s : O my son, him who spoke` |
| 299 | `10` | prose | `…which was commanded us. And said all of them :` |
| 306 | `15` | prose | `…if not many people that they may form an assembly` |
| 311 | `20` | prose | `…And they shall try them carefully concerning that which` |
| 316 | `35` | prose | `…for himself, nor a railer, not unfair, nor the like of that.` |
| 361 | `35` | prose | `…y to the church, who rememTRANSLATION OF THE ETHIOPIC TEXT 1` |
| 367 | `5` | prose | `…ought he not to do it himself? Will it not be written` |
| 374 | `10` | prose | `…every word shall be established. And they shall be tried` |
| 379 | `15` | prose | `…are not double-tongued, nor wrathful, because wrath` |
| 384 | `90` | prose | `…they shall bid those of the brethren who have somewhat` |
| 388 | `35` | prose | `…and some of them they shall question, and some of them` |
| 444 | `5` | prose | `…work), according as it has been given him from God;` |
| 451 | `10` | prose | `…Concerning the reminder that the Obla-` |
| 456 | `15` | prose | `…with certainty. And said Yuhanes : Have ye forgotten,` |
| 461 | `20` | prose | `…concerning Maryam : See her laughing. And said` |
| 470 | `25` | prose | `…Said Kefa : It is not fitting for women to` |
| 475 | `50` | prose | `…should help the needy ? Said Filepos : O brethren,` |
| 525 | `5` | prose | `…us the holy Apostles, thy helpers in thy Church (work-` |
| 530 | `10` | prose | `…chosen for the pontificate, that he may feed thy flock` |
| 535 | `15` | prose | `…authority to forgive sin according to thy commandment,` |
| 546 | `35` | prose | `…them shall salute him with the mouth, kissing him who` |
| 550 | `30` | prose | `…gfiving thanks : The Lord (be) with you all. And the` |
| 599 | `5` | prose | `…— to them who take of it, that it may be to them for holi-` |
| 604 | `10` | prose | `…Church now and always and for ever and ever. Am€n.` |
| 610 | `15` | prose | `…various meaning of each one, but also with the other words,` |
| 615 | `20` | prose | `…receive it.` |
| 622 | `25` | prose | `…Jesus Christ, to grant us to receive with blessing this` |
| 684 | `5` | prose | `…And the presbyter shall say (the prayer of) laying on` |
| 689 | `10` | prose | `…Keep and confirm in them thy fear by thy greatness;` |
| 712 | `25` | prose | `…we said before he shall pray, saying : My God, the` |
| 787 | `15` | prose | `…the Father of our Lord and our Saviour Jesus Christ,` |
| 792 | `20` | prose | `…thy holy of holies * that which is offered to thee by thine` |
| 880 | `35` | prose | `…Concerning new persons who wish to be` |
| 943 | `15` | prose | `…adulteress, or a man without pity, or a man who does` |
| 947 | `20` | prose | `…by the sun, or soothsayer, or interpreter of dreams, or` |
| 954 | `25` | prose | `…Concerning Concubines. If there is any-` |
| 959 | `30` | prose | `…shall receive her, but if she had been near another man,` |

**Tier B — RUNNING PAGE HEAD — number sits on page furniture (5)**

| Line | Number | Kind | 60 chars of preceding context |
|---:|---:|---|---|
| 121 | `29` | running_head | `…TRANSLATION OF THE ETHIOPIC TEXT 1` |
| 288 | `33` | running_head | `…TRANSLATION OF THE ETHIOPIC TEXT 1` |
| 439 | `37` | running_head | `…TRANSLATION OF THE ETHIOPIC TEXT 1` |
| 519 | `39` | running_head | `…TRANSLATION OF THE ETHIOPIC TEXT 1` |
| 677 | `43` | running_head | `…TRANSLATION OF THE ETHIOPIC TEXT 1` |

### `81-teezaz.md` — 179 candidates

**Tier A — PROSE — absorbed marginal line number (the pass-1 target) (149)**

| Line | Number | Kind | 60 chars of preceding context |
|---:|---:|---|---|
| 97 | `5` | prose | `…him and kill him before he receives baptism for the for-` |
| 107 | `15` | prose | `…them ; and if they have done thus they shall hear the` |
| 117 | `25` | prose | `…instruct those who shall be baptised that they should` |
| 122 | `30` | prose | `…be baptised shall fast on Friday, and the bishop shall` |
| 170 | `5` | prose | `…Satan in it, and it is named oil which has been exorcised` |
| 175 | `10` | prose | `…right And let the presbyter, having taken every one of` |
| 180 | `15` | prose | `…saying : All unclean spirits shall depart from him. Thus` |
| 190 | `25` | prose | `…Amen. And he who shall be baptised shall also say` |
| 254 | `15` | prose | `…Christ, and the cup, the wine mixed, that it may become` |
| 259 | `20` | prose | `…the promise which he promised to our fathers, saying : I` |
| 316 | `5` | prose | `…people while the deacons break the bread. And the` |
| 321 | `10` | prose | `…other days they shall give (it) according to the com-` |
| 328 | `15` | prose | `…we have often said. The widows and virgins shall fast,` |
| 333 | `20` | prose | `…they bring that which is proper to bring into the church,` |
| 338 | `25` | prose | `…before they partake. It is Eulogia (awlogiya) — everyone` |
| 403 | `5` | prose | `…bishop again asks them at the supper. If the believers` |
| 423 | `15` | prose | `…should be zealots among the peoples, all of us equal and` |
| 443 | `25` | prose | `…and give the Eulogia. If there is any who takes it away,` |
| 453 | `30` | prose | `…and standing in the midst of all the Faithful, being about` |
| 497 | `5` | prose | `…of their own bread, for it is Eulogia and not Eucharist` |
| 504 | `10` | prose | `…shall receive the bread of blessing from the presbyter or` |
| 509 | `15` | prose | `…take the Eulogia from the hand of the presbyter if he` |
| 514 | `10` | prose | `…the laymen it is not proper that they should make the` |
| 521 | `25` | prose | `…widows and those who are aged, he shall satisfy them` |
| 526 | `30` | prose | `…immediately, and each of them shall do as they wish` |
| 576 | `5` | prose | `…each one ^ which was made thou gavest size and place :` |
| 581 | `10` | prose | `…longer be one born of flesh, but may abide truly in thine` |
| 587 | `15` | prose | `…again we beseech God the almighty, the Father of the` |
| 598 | `25` | prose | `…m darkness into light, and from ignorance into the knowledge` |
| 675 | `50` | prose | `…potions, both those which are drunk, and those which are` |
| 733 | `15` | prose | `…and at each of the names of the Holy Trinity, he` |
| 743 | `25` | prose | `…the Father and the Son and the Holy Sfnrit, and at` |
| 799 | `5` | prose | `…them) with the Lord our God. And the bishop shall` |
| 809 | `5` | prose | `…thy benefit : when the world was gone astray thou savedst J` |
| 819 | `25` | prose | `…holiness and seal of the Holy Spirit upon every person` |
| 824 | `30` | prose | `…Spirit ; and cause that they may be named (his) temple,` |
| 875 | `5` | prose | `…and our Saviour Jesus Christ, to thee have humbled` |
| 880 | `10` | prose | `…hear their prayer. Give them to know the power of the` |
| 885 | `15` | prose | `…for to thee is glory and power and might, now, etc` |
| 891 | `30` | prose | `…shall celebrate, saying : The Lord (be) with you alL` |
| 896 | `25` | prose | `…thanks to the Lord. And they who are present shall` |
| 901 | `30` | prose | `…and say the invocation of the coming of the Holy` |
| 950 | `5` | prose | `…stretching out his hands, he confesses God, saying : I` |
| 970 | `25` | prose | `…saying each of their names. And after the confession of` |
| 976 | `30` | prose | `…humbled themselves ; and to thee they have subdued` |
| 1035 | `15` | prose | `…Christ, who hast regenerated us thy servants and thy` |
| 1045 | `25` | prose | `…And breathe thrice, and then anoint them with the` |
| 1050 | `30` | prose | `…him take the chrism from the bishop and anoint them,` |
| 1101 | `5` | prose | `…say : There is not here a catechumen who is not one` |
| 1123 | `25` | prose | `…creation we offer to thee this milk and honey which` |
| 1175 | `5` | prose | `…the Holy Spirit for ever and ever. Amen.` |
| 1191 | `90` | prose | `…the pregnant or the sick. They who cannot fast the` |
| 1196 | `35` | prose | `…Pentakoste he shall fast in compensation. It is not the` |
| 1253 | `5` | prose | `…But ye shall therefore take the greatest care that none of` |
| 1258 | `10` | prose | `…mercy towards thee : and thou shalt be as having denied` |
| 1265 | `15` | prose | `…Concerning the Deacons and Presbyters.` |
| 1269 | `20` | prose | `…every day, unless sickness of body prevents them. And` |
| 1276 | `25` | prose | `…Concerning the grave. No man shall` |
| 1281 | `30` | prose | `…bishop shall sustain him with what they offer to the` |
| 1334 | `5` | prose | `…the ancient law commanded to give the bread which` |
| 1339 | `10` | prose | `…the heavens. And again pray at the sixth hour ; for` |
| 1345 | `15` | prose | `…Christ prayed, and made all the world darkness : and` |
| 1351 | `20` | prose | `…God who faileth not, who remembered his righteous` |
| 1356 | `25` | prose | `…And therefore thou also as thou makest beginning of` |
| 1362 | `30` | prose | `…a wife, both of you pray. And if she has not yet` |
| 1410 | `5` | prose | `…signifies that thou makest it in faith. Not for` |
| 1415 | `10` | prose | `…outwardly with the seal of the Word. He trembles` |
| 1420 | `15` | prose | `…slain, and he commanded to smear the blood on the` |
| 1424 | `30` | prose | `…foreheads thus sealed with the hand, then we shall` |
| 1429 | `35` | prose | `…may keep it, ye who have sense, if ye heard and kept` |
| 1494 | `15` | prose | `…Since the power is his, and ours the faith and diligence,` |
| 1510 | `30` | prose | `…Lord Christ for the Jews like Moses healed all infirmity` |
| 1559 | `5` | prose | `…Let not therefore any who do a sign and miracle` |
| 1564 | `10` | prose | `…or knowledge, or discerning of spirits, or the word of` |
| 1570 | `15` | prose | `…magnify himself nor boasted over his prophet Aaron.` |
| 1575 | `20` | prose | `…of Ailon, because the day was not sufficient for the` |
| 1580 | `25` | prose | `…And the seven thousand who were in Esrael, the holy ones` |
| 1584 | `30` | prose | `…Elesewon did not neglect his assistant when he was` |
| 1652 | `15` | prose | `…impious if they prophesy do not reveal their wickedness` |
| 1725 | `5` | prose | `…from gods, and from dead things keep, and from blood and` |
| 1731 | `10` | prose | `…the next ; and if he has need, the third also ; and if he` |
| 1737 | `15` | prose | `…is a prophet : if he lives the life of God, he is a true` |
| 1750 | `25` | prose | `…the ancient prophets.` |
| 1816 | `15` | prose | `…(of the church) and the (other) widows shall sit by` |
| 1822 | `30` | prose | `…enter and make them sit in separate places.` |
| 1829 | `25` | prose | `…And if any other man or woman comes in lay dress,` |
| 1834 | `30` | prose | `…ministering to command places for them, but remain` |
| 1902 | `15` | prose | `…him) all the people shall assemble ; the presbyters, and` |
| 1912 | `25` | prose | `…the men of his own house well, and has he conducted his` |
| 1976 | `15` | prose | `…they may wash their hands as a likeness of those who` |
| 1985 | `25` | prose | `…any bear malice in his heart against another, nor any` |
| 2058 | `25` | prose | `…And thou, bishop, ordain the presbyter, and lay hand` |
| 2064 | `30` | prose | `…Concerning the Deaconesses and Subdeaconesses and` |
| 2129 | `15` | prose | `…who is with you should be ordained by bishops.` |
| 2140 | `35` | prose | `…commandment, and he shall not be deposed, nor he who` |
| 2147 | `30` | prose | `…himself. And he shall ordain men. And he shall offer` |
| 2197 | `5` | prose | `…are the servants of the deacons.` |
| 2207 | `15` | prose | `…Statute 6i. Concerning that which is left of the` |
| 2212 | `20` | prose | `…the bishop, and three shall be given to the presbyter,` |
| 2217 | `25` | prose | `…veryone shall perform his ordinance. And there is not in the` |
| 2278 | `5` | prose | `…that he should be cured, and that he should not come into` |
| 2284 | `10` | prose | `…and the adulterers and drinks with them, let him leave` |
| 2291 | `15` | prose | `…If there is a man who makes idols, if he wishes` |
| 2297 | `20` | prose | `…shall leave their former work or be rejected.` |
| 2303 | `25` | prose | `…shall not do it. Or he who plays the harp, or he who` |
| 2310 | `30` | prose | `…manner if there is a witch, or woman who guides to` |
| 2367 | `5` | prose | `…left (the occupations) they shall be accepted, otherwise` |
| 2374 | `10` | prose | `…if she took another she shall be repudiated.` |
| 2380 | `15` | prose | `…we have commanded. If he loves her he shall first` |
| 2386 | `20` | prose | `…And if there is a man among us, and he did wickedly,` |
| 2392 | `25` | prose | `…he may be in the number of those who do virtuously,` |
| 2397 | `30` | prose | `…quickly (or slowly) in its time, but it shall be (a matter)` |
| 2476 | `30` | prose | `…his glory and his work, that he might be known that he` |
| 2527 | `5` | prose | `…the week (sabu'a) of the Pascha (Fasika). The first` |
| 2532 | `10` | prose | `…the first week (samun) because our Lord and our God` |
| 2537 | `15` | prose | `…not do work on the day of the feast of the fortieth,` |
| 2542 | `20` | prose | `…manifested, he who came down upon the believers in our` |
| 2547 | `25` | prose | `…Jesus Christ, of our Lady Mary, the Saviour of the` |
| 2552 | `30` | prose | `…the Holy Spirit descended upon him like the form of a` |
| 2606 | `5` | prose | `…because of unbelievers, thou, bishop, make prayer in` |
| 2611 | `10` | prose | `…pollute it As the pure man sanctifies the church, so it` |
| 2617 | `15` | prose | `…and three they shall pray, because our Lord said : Where` |
| 2623 | `20` | prose | `…partakes of the holy Mystery should be defiled.` |
| 2630 | `25` | prose | `…be excommunicated and go out of the church.` |
| 2700 | `15` | prose | `…Concerning those who are persecuted for` |
| 2770 | `15` | prose | `…as was right for his service ; that which the chief priests` |
| 2781 | `25` | prose | `…to Saol, when he thought to offer sacrifice of his own` |
| 2787 | `30` | prose | `…And God has made known to us by the declaration of` |
| 2847 | `15` | prose | `…as he is the Chief Priest for us, so he offered spiritual` |
| 2852 | `20` | prose | `…Order of ordination of priesthood like us. And after his` |
| 2911 | `5` | prose | `…to us thine angel the good guide. And have mercy upon` |
| 2914 | `10` | prose | `…was named over us. Be forgiving to us and forsake us` |
| 2925 | `20` | prose | `…healing give to them life, the Lord our God.` |
| 2932 | `35` | prose | `…away from them all disease and all suffering. Speedily` |
| 2941 | `50` | prose | `…art the overseer of all flesh, and of those who are troubled` |
| 2992 | `5` | prose | `…water its furrows. Bring the sowing and the harvest,` |
| 3000 | `10` | prose | `…For the poor of thy people, and for all those who hope` |
| 3010 | `20` | prose | `…the sowing and the harvest. May he grant rich favour,` |
| 3017 | `25` | prose | `…pleased (and) bring the sowing and the harvest, which` |
| 3025 | `30` | prose | `…For the poor of thy people and for all who call upon` |
| 3073 | `5` | prose | `…Speedily let thy mercy find us, O Lord.` |
| 3104 | `50` | prose | `…for those who offer an offering to the holy, one, catholic` |
| 3155 | `5` | prose | `…etc., Lord of the living, Life of the dead, and Hope` |
| 3160 | `10` | prose | `…for ever and ever, with whom is the treasure of life, for` |
| 3165 | `15` | prose | `…orphans {lit. offspring of the dead) ; and for the soul of` |
| 3170 | `20` | prose | `…in the bosom of Abreham, Yeshak, and Ya'ekob, in the` |
| 3174 | `25` | prose | `…kingdom ; for there is no death to thy servants, but` |
| 3179 | `30` | prose | `…lived one hour upon the earth. Do thou grant passings` |
| 3252 | `25` | prose | `…beseech thee for the blessed Papas N. In keeping keep` |

**Tier B — RUNNING PAGE HEAD — number sits on page furniture (30)**

| Line | Number | Kind | 60 chars of preceding context |
|---:|---:|---|---|
| 164 | `153` | running_head | `…TRANSLATION OF THE ETHIOPIC TEXT` |
| 238 | `55` | running_head | `…TRANSLATION OF THE ETHIOPIC TEXT 1` |
| 310 | `57` | running_head | `…TRANSLATION OF THE ETHIOPIC TEXT 1` |
| 393 | `159` | running_head | `…TRANSLATION OF THE ETHIOPIC TEXT` |
| 570 | `163` | running_head | `…TRANSLATION OF THE ETHIOPIC TEXT` |
| 644 | `65` | running_head | `…TRANSLATION OF THE ETHIOPIC TEXT 1` |
| 717 | `167` | running_head | `…TRANSLATIOH OF THE ETHIOPIC TEXT` |
| 793 | `169` | running_head | `…TRANSLATION OF THE ETHIOPIC TEXT` |
| 868 | `171` | running_head | `…TRANSLATION OF THE ETHIOPIC TEXT` |
| 944 | `73` | running_head | `…TRANSLATION OF THE ETHIOPIC TEXT 1` |
| 1018 | `75` | running_head | `…TRANSLATION OF THE ETHIOPIC TEXT 1` |
| 1095 | `177` | running_head | `…TRANSLATION OF THE ETHIOPIC TEXT` |
| 1169 | `79` | running_head | `…TRANSLATION OF THE ETHIOPIC TEXT 1` |
| 1328 | `83` | running_head | `…TRANSLATION OF THE ETHIOPIC TEXT 1` |
| 1478 | `87` | running_head | `…TRANSLATION OF THE ETHIOPIC TEXT 1` |
| 1552 | `89` | running_head | `…TRANSLATION OF THE ETHIOPIC TEXT 1` |
| 1882 | `97` | running_head | `…TRANSLATION OF THE ETHIOPIC TEXT 1` |
| 2110 | `203` | running_head | `…TRANSLATION OF THE ETHIOPIC TEXT` |
| 2271 | `207` | running_head | `…TRANSLATION OF THE ETHIOPIC TEXT` |
| 2361 | `209` | running_head | `…TRANSLATION OF THE ETHIOPIC TEXT` |
| 2442 | `211` | running_head | `…TRANSLATION OF THE ETHIOPIC TEXT` |
| 2519 | `213` | running_head | `…TRANSLATION OF THE ETHIOPIC TEXT` |
| 2683 | `217` | running_head | `…TRANSLATION OF THE ETHIOPIC TEXT` |
| 2756 | `219` | running_head | `…TRANSLATION OF THE ETHIOPIC TEXT` |
| 2831 | `221` | running_head | `…TRANSLATION OF THE ETHIOPIC TEXT` |
| 2904 | `223` | running_head | `…TRANSLATION OF THE ETHIOPIC TEXT` |
| 2985 | `225` | running_head | `…TRANSLATION OF THE ETHIOPIC TEXT` |
| 3005 | `15` | running_head | `…PRAYER FOR THE FRUIT OF THE EARTH` |
| 3148 | `229` | running_head | `…TRANSLATION OF THE ETHIOPIC TEXT` |
| 3223 | `1` | running_head | `…TRANSLATION OF THE ETHIOPIC TEXT 23` |

### `82-gessew.md` — 4 candidates

**Tier B — RUNNING PAGE HEAD — number sits on page furniture (4)**

| Line | Number | Kind | 60 chars of preceding context |
|---:|---:|---|---|
| 162 | `65` | running_head | `…THE APOSTOLIC CANONS, TRANSLATED FROM THE ETHIOPIC.` |
| 284 | `67` | running_head | `…THE APOSTOLIC CANONS, TRANSLATED FROM THE ETHIOPIC.` |
| 399 | `69` | running_head | `…THE APOSTOLIC CANONS, TRANSLATED FROM THE ETHIOPIC.` |
| 522 | `1` | running_head | `…THE APOSTOLIC CANONS, TRANSLATED FROM THE ETHIOPIC. 7` |

### `84-mashafa-kidan-1.md` — 87 candidates

**Tier A — PROSE — absorbed marginal line number (the pass-1 target) (9)**

| Line | Number | Kind | 60 chars of preceding context |
|---:|---:|---|---|
| 155 | `18` | prose | `…days, out of the latest generation,” there should be vessels` |
| 202 | `57` | prose | `…CHaprer` |
| 1924 | `1` | prose | `…been cut, so that we may attain? immortality instead of` |
| 2974 | `8` | prose | `…13 Masc. (phials is fem.). Cf. Rev. v.` |
| 3038 | `5` | prose | `…the night [and] at dawn. If she be menstruous let her abide` |
| 3107 | `7` | prose | `…who sent Thee, turn, help, O Lord, set upright our thoughts` |
| 3189 | `2` | prose | `…A male or female virgin is not instituted" or appointed` |
| 3266 | `1` | prose | `…Cuarrer 47` |
| 4191 | `17` | prose | `…CHarTer` |

**Tier B — RUNNING PAGE HEAD — number sits on page furniture (64)**

| Line | Number | Kind | 60 chars of preceding context |
|---:|---:|---|---|
| 133 | `51` | running_head | `…L 2, 3] PROLOGUE` |
| 244 | `53` | running_head | `…I. 6-8] PROLOGUE` |
| 308 | `8` | running_head | `…54 TESTAMENT OF OUR LORD [1.` |
| 359 | `55` | running_head | `…1. 8] PROLOGUE` |
| 473 | `57` | running_head | `…I. 10, 11] PROLOGUE` |
| 576 | `59` | running_head | `…I. 13-15] PROLOGUE` |
| 676 | `61` | running_head | `…I. 17, 18] PROLOGUE` |
| 775 | `63` | running_head | `…1. 19] THE CHURCH BUILDINGS` |
| 888 | `65` | running_head | `…I. 20, 21] THE BISHOP` |
| 937 | `21` | running_head | `…66 TESTAMENT OF OUR LORD [1` |
| 986 | `67` | running_head | `…I. 21] THE BISHOP` |
| 1035 | `22` | running_head | `…68 TESTAMENT OF OUR LORD [L.2i,` |
| 1082 | `69` | running_head | `…I. 22, 23] THE EUCHARIST` |
| 1129 | `23` | running_head | `…70 TESTAMENT OF OUR LORD [1.` |
| 1185 | `71` | running_head | `…I. 23] THE EUCHARIST` |
| 1246 | `23` | running_head | `…72 TESTAMENT OF OUR LORD [1.` |
| 1295 | `73` | running_head | `…1. 23] THE EUCHARIST` |
| 1345 | `23` | running_head | `…74 TESTAMENT OF OUR LORD [I.` |
| 1395 | `75` | running_head | `…I, 23] THE EUCHARIST` |
| 1436 | `23` | running_head | `…76 TESTAMENT OF OUR LORD [I.` |
| 1486 | `77` | running_head | `…I. 23, 24] THE EUCHARIST` |
| 1577 | `79` | running_head | `…I. 26] THE EUCHARIST` |
| 1621 | `26` | running_head | `…80 TESTAMENT OF OUR LORD {I.` |
| 1663 | `81` | running_head | `…1. 26] THE EUCHARIST` |
| 1705 | `26` | running_head | `…82 _ TESTAMENT OF OUR LORD [1.` |
| 1752 | `83` | running_head | `…I. 26] THE EUCHARIST` |
| 1847 | `85` | running_head | `…1, 28] MYSTAGOGIA` |
| 1895 | `238` | running_head | `…86 TESTAMENT OF OUR LORD [1` |
| 1942 | `87` | running_head | `…I. 28] MYSTAGOGIA` |
| 1992 | `28` | running_head | `…88 TESTAMENT OF OUR LORD [I.` |
| 2040 | `89` | running_head | `…1. 28] MYSTAGOGIA :` |
| 2137 | `91` | running_head | `…I. 30] PRESBYTERS` |
| 2227 | `93` | running_head | `…L 31] PRESBYTERS` |
| 2277 | `31` | running_head | `…94 TESTAMENT OF OUR LORD (1.` |
| 2332 | `95` | running_head | `…1. 31, 32] PRESBYTERS` |
| 2386 | `32` | running_head | `…96 TESTAMENT OF OUR LORD [1.` |
| 2432 | `97` | running_head | `…I. 32-34] DEACONS` |
| 2482 | `34` | running_head | `…98 TESTAMENT OF OUR LORD [I.` |
| 2533 | `99` | running_head | `…I. 34, 35] DEACONS` |
| 2583 | `35` | running_head | `…100 TESTAMENT OF OUR LORD [I.` |
| 2643 | `101` | running_head | `…I. 35] DEACONS` |
| 2841 | `105` | running_head | `…I. 38-40] CONFESSORS, WIDOWS` |
| 2884 | `40` | running_head | `…106 TESTAMENT OF OUR LORD [I.` |
| 2931 | `107` | running_head | `…1. 40] WIDOWS` |
| 2976 | `41` | running_head | `…108 TESTAMENT OF OUR LORD [I.` |
| 3024 | `109` | running_head | `…I. 41, 42] WIDOWS` |
| 3117 | `111` | running_head | `…I. 43, 44] WIDOWS, SUBDEACONS` |
| 3146 | `4` | running_head | `…OF SUBDEACONS` |
| 3211 | `113` | running_head | `…I. 46] VIRGINS` |
| 3322 | `1` | running_head | `…116 TESTAMENT OF OUR LORD [IL` |
| 3373 | `117` | running_head | `…II. 1, 2] CATECHUMENS` |
| 3432 | `2` | running_head | `…118 TESTAMENT OF OUR LORD (11.` |
| 3488 | `119` | running_head | `…II. 3, 4] CATECHUMENS` |
| 3583 | `121` | running_head | `…II. 6, 7] CATECHUMENS` |
| 3632 | `7` | running_head | `…122 TESTAMENT OF OUR LORD [II.` |
| 3683 | `123` | running_head | `…1. 7] CATECHUMENS` |
| 3775 | `125` | running_head | `…11. 8] BAPTISM` |
| 3829 | `8` | running_head | `…126 TESTAMENT OF OUR LORD (I.` |
| 3874 | `127` | running_head | `…IL. 8, 9] CONFIRMATION` |
| 3975 | `129` | running_head | `…II. 10, 11] MAUNDY THURSDAY, ETC.` |
| 4081 | `131` | running_head | `…II. 13-15] FIRST FRUITS, PROPERTY` |
| 4186 | `133` | running_head | `…1. 16-19] PASCHAL SOLEMNITIES, ETC.` |
| 4286 | `135` | running_head | `…IL. 20-23] THE SICK, PSALMS, BURIALS` |
| 4385 | `137` | running_head | `…II. 24-26] CONCLUSION` |

**Tier C — RISKY — folio citation, referring noun, or enumeration (14)**

| Line | Number | Kind | 60 chars of preceding context |
|---:|---:|---|---|
| 80 | `2` | enumeration | `…50 TESTAMENT OF OUR LORD [I. 1,` |
| 727 | `19` | enumeration | `…62 TESTAMENT OF OUR LORD [I. 18,` |
| 832 | `20` | enumeration | `…64 TESTAMENT OF OUR LORD [1. 19,` |
| 2182 | `31` | enumeration | `…92 TESTAMENT OF OUR LORD [I. 30,` |
| 2698 | `36` | enumeration | `…102 TESTAMENT OF OUR LORD [I. 35,` |
| 2795 | `38` | enumeration | `…104 TESTAMENT OF OUR LORD [I. 37,` |
| 3073 | `43` | enumeration | `…110 TESTAMENT OF OUR LORD [1. 42,` |
| 3261 | `47` | enumeration | `…114 TESTAMENT OF OUR LORD [1. 46,` |
| 3728 | `8` | enumeration | `…124 TESTAMENT OF OUR LORD [II. 7,` |
| 3922 | `10` | enumeration | `…128 TESTAMENT OF OUR LORD {r1. 9,` |
| 4139 | `16` | enumeration | `…132 TESTAMENT OF OUR LORD [IT. 15,` |
| 4229 | `20` | enumeration | `…134 TESTAMENT OF OUR LORD [11 19,` |
| 4335 | `24` | enumeration | `…136 TESTAMENT OF OUR LORD [II 23,` |
| 4434 | `27` | enumeration | `…138 TESTAMENT OF OUR LORD [iI. 26,` |

### `86-qalementos.md` — 161 candidates

**Tier A — PROSE — absorbed marginal line number (the pass-1 target) (62)**

| Line | Number | Kind | 60 chars of preceding context |
|---:|---:|---|---|
| 242 | `2` | prose | `…Desinit : (F. 206 r° b) AGAar : Gage à h92% 2: 09%` |
| 760 | `65` | prose | `…KA4OG .… (90 r.) ne se trouve que dans les manuscrits` |
| 2441 | `1` | prose | `…,` |
| 2631 | `31` | prose | `…Lirrérarune À ÉTHIOPIENNE PSEUDO-CLÉMENTIN E.` |
| 2690 | `33` | prose | `…;` |
| 2974 | `4` | prose | `…Ni > ni 4 4 s .` |
| 3107 | `6` | prose | `…"Apy. : ‘Env tv xepahv Eu6dkn` |
| 3138 | `6` | prose | `…"Apy. : Kéxpuyé mic moopñrns Or` |
| 3808 | `17` | prose | `…"AY. Edv un vis ôTAiontat` |
| 4006 | `6` | prose | `…"Apy. : "Ex tivoy cnueluv voñoac` |
| 4031 | `1` | prose | `…Guspoper…` |
| 4064 | `4` | prose | `…LA À L] ’ ei L` |
| 4298 | `2` | prose | `…(og. 710) Maëiuou Toù ‘Ouohoynrod, Tà verpaxooix xepdlata ta` |
| 4484 | `42` | prose | `…“` |
| 4723 | `35` | prose | `…;` |
| 4764 | `2` | prose | `…33 lignes) contenant un recueil de prières magiques. Fol.` |
| 5032 | `27` | prose | `…— Fol. 3 (18 lign.), Prière de la Vierge au Golgotha. — Fol.` |
| 5034 | `62` | prose | `… Fol.43 (2 col., 18-20 lign.), Anaphore de la Vierge. — Fol.` |
| 5035 | `97` | prose | `…col., 18-20 lign.), Récit de N.-$. aux douze apôtres. — Fol.` |
| 5283 | `67` | prose | `…TABLE.` |
| 5309 | `3` | prose | `…Q. 992.` |
| 5713 | `251` | prose | `…Ls at lots mei@l 5e` |
| 5751 | `2` | prose | `…SI a Roll is sas, Lusac hs` |
| 5781 | `9` | prose | `….123005` |
| 6106 | `100` | prose | `…LS JRassafs Jlosinskso we .J + YO` |
| 6203 | `230` | prose | `…POS MJradas 40010 aauro aausfo ,JRaueds Jloiatl os CRC` |
| 6212 | `45` | prose | `…] MR Fsoaus fsa Jpe «9! Loos HKiois Iio So por .Lpas fro Ne)` |
| 6213 | `550` | prose | `… EN Jade CE Mise Luis) Euois JR user pul .Rcoo Ho pulr Etuis` |
| 6294 | `2` | prose | `…CSS` |
| 6525 | `58` | prose | `…2 X 40 et 3 A La M \ , = et N ê U è` |
| 6574 | `4` | prose | `…ar& oùpavolëv, ds abroi phuapobot, xat à ouyy@pnos rod "Ada.` |
| 6575 | `72` | prose | `…La / - 1 ’ Pn` |
| 6737 | `10` | prose | `…Notons aussi qu'Abou-Taleb mourut au mois de Schewal de l’an` |
| 6835 | `430` | prose | `…Îl 2 S à` |
| 7721 | `57` | prose | `…MORTS ET SECOND AVÈNEMENT DU CuHrist (fol. 56 r° à à fol.` |
| 7726 | `9` | prose | `…28 3 NN : Tag à NA à Né à. (4) AAC] :` |
| 7785 | `7` | prose | `…QC: : AhPCLTE : A0-h3 : Néhfo: : ne7 : AA :` |
| 7786 | `24` | prose | `…NC: : .… A: ht OH : ove.b : [RAT :]` |
| 7818 | `60` | prose | `…5. — Lévitique, xx, 1-3. — Le sABBAT (fol. 59 v° b à fol.` |
| 7881 | `6` | prose | `…Incipit : (F. 62 v° a suite) HAU-£: : ADR : PCI 2` |
| 7918 | `71` | prose | `…Incipit : (F. 64 r° a suite) né : hPC£t : DA9°N :` |
| 8021 | `6` | prose | `…Éphrem le Syrien… Gloire à toi, 6 Patient! Gloire à toi,` |
| 8036 | `0` | prose | `…(tirées) à nouveau d'un sermon de Saint Mar Éphrem.` |
| 9111 | `7` | prose | `…CAEN` |
| 9182 | `255` | prose | `…LE TROPAIRE O Movoyevñc.` |
| 9277 | `257` | prose | `…LE TROPAIRE ‘O Movoyevhc.` |
| 9353 | `259` | prose | `…LE TROPAIRE O Mevoyevns.` |
| 9426 | `261` | prose | `…LE TROPAIRE O Moveyevñc.` |
| 9505 | `1` | prose | `…e vin : Ju sacs so, co] Su: Lio, CE qui la rapproche encore:` |
| 9513 | `263` | prose | `…LE TROPAIRE O Movoyeync.` |
| 9593 | `20` | prose | `…LE TROPAIRE ‘O Movoyevñc.` |
| 9678 | `267` | prose | `…LE TROPAIRE ‘© Moyoyevhs.` |
| 9928 | `4` | prose | `…Téy. Il, o. 466.` |
| 10018 | `150` | prose | `…‘O xaréhoyoc obroc avreyoton mors &x roù ür” dpbuèv` |
| 10033 | `6` | prose | `…‘Ayiou ’Abavaclou Toi Marsopirou œepomévnv mao docuv ùTApÉEV` |
| 10116 | `6` | prose | `…‘H Gvoyoaph abTn cxevdiv za Bélov éye4pn LaTa TV LE` |
| 10222 | `160` | prose | `…GNAYPAPR ÉTÉPOV creudiv, xeîrat ëv p. 113% ro5 dr œprôuov` |
| 10238 | `5` | prose | `…rpiroy dé pot Bapivos pabwotvos` |
| 10246 | `10` | prose | `…Evværov dé cor oÙXe 6 AUTax®` |
| 10250 | `7` | prose | `…ln` |
| 10291 | `32` | prose | `…I. — Traité théologique, par Ibn el-Assal, xiv° siècle,` |
| 10943 | `6` | prose | `…se réjouiront d’une joie qui ne finira pas. Comiprends donc,` |

**Tier B — RUNNING PAGE HEAD — number sits on page furniture (74)**

| Line | Number | Kind | 60 chars of preceding context |
|---:|---:|---|---|
| 108 | `9` | running_head | `…Fû : OÙ : A0 2 FAN? ACER : AÛN : AAGE. :` |
| 460 | `6` | running_head | `…ORIENT CHRÉTIEN.` |
| 511 | `83` | running_head | `…LITTÉRATURE ÉTIHIOPIENNE PSEUDO-CLÉMENTINE.` |
| 669 | `87` | running_head | `…MANUSCRITS COPTES.` |
| 758 | `99` | running_head | `…MANUSCRITS COPTES.` |
| 842 | `91` | running_head | `…MANUSCRITS COPTES,` |
| 931 | `93` | running_head | `…MANUSCRITS COPTES.` |
| 1002 | `95` | running_head | `…MANUSCRITS COPTES.` |
| 1087 | `97` | running_head | `…MANUSCRITS COPTES.` |
| 1171 | `99` | running_head | `…MANUSCRITS COPTES.` |
| 2005 | `2` | running_head | `…ORIENT CHRÉTIEN. -` |
| 2443 | `27` | running_head | `…. LITTÉRATURE ÉTHIOPIENNE PSEUDO-CLÉMENTINE.` |
| 3312 | `91` | running_head | `…DES MÉTÉORES.` |
| 3544 | `39` | running_head | `…UN: MANUSCRIT DES MÉTÉORES.` |
| 4229 | `43` | running_head | `…DES MÉTÉORES.` |
| 4264 | `4` | running_head | `…* 72 = FE) \| \` |
| 4286 | `72` | running_head | `…+ SAN NA 21 #` |
| 4482 | `49` | running_head | `…MANUSCRITS ÉTHIOPIENS.` |
| 4521 | `4` | running_head | `…ORIENT CHRÉTIEN.` |
| 4649 | `53` | running_head | `…* MANUSCRITS ÉTHIOPIENS.` |
| 4730 | `99` | running_head | `…MANUSCRITS ÉTHIOPIENS.` |
| 4769 | `5` | running_head | `…NN PR 7 NS` |
| 4805 | `97` | running_head | `…MANUSCRITS ÉTHIOPIENS.` |
| 4884 | `99` | running_head | `…. MANUSCRITS ÉTHIOPIENS.` |
| 4960 | `61` | running_head | `…MANUSCRITS ÉTHIOPIENS.` |
| 5040 | `63` | running_head | `…MANUSCORITS ÉTHIOPIENS. ;` |
| 5120 | `65` | running_head | `…MANUSCRITS ÉTHIOPIENS.` |
| 5151 | `4` | running_head | `…XVIII S. \|` |
| 5156 | `5` | running_head | `…ORIENT CNRÉTIEN,` |
| 5577 | `73` | running_head | `…FRAGMENTS DE MAR ABA, DISCIPLE DE SAINT EPHREM.` |
| 5725 | `7` | running_head | `…DEUX NOTICES RELATIVES AU MALABAR.` |
| 5787 | `79` | running_head | `…DEUX NOTICES RELATIVES AU MALABAR.` |
| 5878 | `81` | running_head | `…DEUX NOTICES RELATIVES AU MALABAR.` |
| 5929 | `6` | running_head | `…ORIENT CHRÉTIEN.` |
| 5975 | `83` | running_head | `…DEUX NOTICES RELATIVES AU MALABAR.` |
| 6067 | `85` | running_head | `…DEUX NOTICES RELATIVES AU MALABAR.` |
| 6145 | `87` | running_head | `…DEUX NOTICES RELATIVES AU MALABAR.` |
| 6228 | `89` | running_head | `…DEUX NOTICES RELATIVES AU MALABAR. .` |
| 6307 | `91` | running_head | `…DEUX NOTICES RELATIVES AU MALABAR.` |
| 6402 | `93` | running_head | `…DEUX NOTICES RELATIVES AU MALABAR.` |
| 6504 | `95` | running_head | `…DEUX NOTICES RELATIVES AU MALABAR.` |
| 6589 | `97` | running_head | `…DEUX NOTICES RELATIVES. AU MALABAR. .` |
| 6649 | `7` | running_head | `…ORIENT CHRÉTIEN.` |
| 6704 | `99` | running_head | `…DEUX NOTICES RELATIVES AU MALABAR.` |
| 6798 | `101` | running_head | `…MÉLANGES,` |
| 6925 | `103` | running_head | `…MÉLANGES.` |
| 7076 | `107` | running_head | `…BIBLIOGRAPHIE.` |
| 7173 | `109` | running_head | `…BIBLIOGRAPHIE.` |
| 7378 | `4` | running_head | `…EN EST \| PP PER C2 Se PP DE Lt he NET : = Ra` |
| 7402 | `3` | running_head | `…dA : AA : ANNÉE CR : 077 : Onr : AL : AE :` |
| 7413 | `8` | running_head | `…ORIENT CHRÉTIEN. 5` |
| 7418 | `20` | running_head | `…ADUP : AAA à ICT : DAPRAAP : I :` |
| 7440 | `2` | running_head | `…DETINA : NA TEA 2 IN 5 ADNLANRE F2: HAE` |
| 7616 | `119` | running_head | `…“LES MSS. ÉTHIOPIENS DE M. DELORME.` |
| 7686 | `93` | running_head | `…PAT : APNAU: : ACER :` |
| 7700 | `121` | running_head | `… LES.MSS. ÉTHIOPIENS DE M. DELORME.` |
| 7776 | `123` | running_head | `…LES MSS. ÉTHIOPIENS DE M. DELORME.` |
| 7822 | `5` | running_head | `…LANCE : Aov-ÿ, : DR : 772000: : ABT : AH A` |
| 7910 | `1` | running_head | `…(F. 64 7° à) Mb C ? NCTY : DA : AA : AAN :` |
| 7937 | `127` | running_head | `…LES MSS. ÉTHIOPIENS DE M. DELORME.` |
| 8086 | `131` | running_head | `…LES MSS. ÉTHIOPIENS DE M. DELORME.` |
| 8110 | `02` | running_head | `…DAASIL TE : NNHRC : DAPALT : AGO : GAP :` |
| 8556 | `2` | running_head | `…DORÉ RP ROUEN CR COLE GR Lo,` |
| 8618 | `143` | running_head | `…LITTÉRATURE ÉTHIOPIRNNE PSEUDO-CLÉMENTINE.` |
| 9078 | `1` | running_head | `…: Ê PATES = L ‘#` |
| 9317 | `17` | running_head | `…/  ORIENT CHRÉTIEN. ;` |
| 9750 | `269` | running_head | `…IIAAAIOT KATAAOTOI.` |
| 9988 | `18` | running_head | `…ORIENT CHRÉTIEN,` |
| 10044 | `275` | running_head | `…HAAAÏJOI KATAAOTOI.` |
| 10242 | `279` | running_head | `…HAAAIOI KATAAOTOT.` |
| 10415 | `283` | running_head | `…CATALOGUE SOMMAIRE DES MANUSCRITS DU P. P. A. SBATH.` |
| 10517 | `285` | running_head | `…CATALOGUE SOMMAIRE DES MANUSCRITS DU P. P. A. SBATH.` |
| 10615 | `71` | running_head | `…1 LITTÉRATURE ÉTHIOPIENNE PSEUDO-CLÉMENTINE.` |
| 10814 | `19` | running_head | `…LITTÉRATURE ÉTHIOPIENNE PSEUDO-OLÉMENTINE.` |

**Tier C — RISKY — folio citation, referring noun, or enumeration (25)**

| Line | Number | Kind | 60 chars of preceding context |
|---:|---:|---|---|
| 464 | `4` | folio | `…cinquième jour, le Seigneur ordonna aux eaux de produire (F.` |
| 640 | `259` | enumeration | `…240, 247 à 251, 254 à 298, 241 à 243, 252, 253, 244 à 246,` |
| 1179 | `151` | referent | `…rouges. La liturgie de saint Grégoire commence au feuillet` |
| 1434 | `11` | folio | `…de la nuit, (et sache) comment il faut que tu intercèdes (F.` |
| 1687 | `16` | folio | `…t, Lamech, en allant dans la campagne, entendit le bruit (F.` |
| 1753 | `17` | folio | `…instruments de musique. Lorsque les enfants de Seth, que (F.` |
| 1840 | `19` | folio | `…culte devant le Seigneur, avec droiture et avec justice, (F.` |
| 2542 | `31` | folio | `… Le fils (4) fit la statue de son père en or et la plaça (F.` |
| 2611 | `32` | folio | `…de VNämroud, et (sut) comment il avait appris la science (F.` |
| 5656 | `23` | enumeration | `…pouvons que rapprocher son récit, qui occupe les folios 21 à` |
| 7119 | `877` | referent | `…hèse théologique ou pour un sermon. L’index alphabétique, p.` |
| 7474 | `148` | referent | `…Ce Martyre existe en arabe dans le ms. Fonds arabe, n°` |
| 7871 | `61` | folio | `… Evangile de Jean : Ensuite, eut lieu la fête des Juifs. (F.` |
| 7878 | `62` | folio | `…9. — I Corinthiens, xv, 91-xvI, 2. — LA RÉSURRECTION (fol.` |
| 7882 | `62` | folio | `…U< : 409 : 4 : Fr léNo: : Ah à NAT : Hz : (F.` |
| 7928 | `64` | folio | `…12. — LA BÉNÉDICTION DES PROPHÈTES ET DES APÔTRES (fol.` |
| 8014 | `15` | folio | `…2. — PRIÈRE POUR LE MARDI, tirée de Saint Éphrem (fol.` |
| 8094 | `68` | folio | `…6. — PRIÈRE POUR LE SAMEDI, tirée de Saint Athanase (fol.` |
| 8117 | `76` | folio | `…7. — PRIÈRÉ POUR LE DIMANCHE, tirée de Saint Cyrille (fol.` |
| 9045 | `49` | folio | `…nouveau, mon Seigneur me dit : « Tourne-toi. » Je le vis (F.` |
| 9254 | `161` | enumeration | `…Dans les hymnes de Sévère, Patr. Or., tome VI, p. 157, 160,` |
| 10555 | `58` | folio | `…TERVENTION DE DIEU EN FAVEUR DES CHRÉTIENS PERSÉCUTÉS. — (F.` |
| 10592 | `59` | folio | `…le 10m ?Andnäs; le 11e la secte qui s'appelle El-Bânyou; (F.` |
| 10675 | `61` | folio | `…e. Les jeunes gens s’assoiront au-dessus des vieillards, (F.` |
| 10955 | `68` | folio | `…e (2), qui est le plus grand et le plus glorieux de tous (F.` |

### `87-didascalia.md` — 126 candidates

**Tier A — PROSE — absorbed marginal line number (the pass-1 target) (39)**

| Line | Number | Kind | 60 chars of preceding context |
|---:|---:|---|---|
| 433 | `28` | prose | `…unto a multitude of words, but may be strong in` |
| 533 | `7` | prose | `…sorrow. In like manner a wicked woman bringeth` |
| 1167 | `7` | prose | `…ree .` |
| 1265 | `23` | prose | `…in all his iniquity which he hath done, the sinner shall` |
| 1312 | `1` | prose | `…compassionate to those who turn` |
| 1613 | `12` | prose | `…out a good shepherd, and a meek and patient teacher` |
| 1869 | `18` | prose | `…with 8vos.` |
| 1948 | `37` | prose | `…anger.’”` |
| 2436 | `2` | prose | `…E` |
| 2551 | `1` | prose | `…to-day have begotten you.’’` |
| 2710 | `44` | prose | `…them) ‘Judge in righteousness and uprightness ”’;` |
| 2715 | `47` | prose | `…for your judgment shall not be acceptable.”` |
| 2752 | `3` | prose | `…the way of life. The bishop ought to walk in this` |
| 3654 | `48` | prose | `…and have mercy upon thee,*? and give thee peace.”` |
| 3685 | `5` | prose | `…prophet is not had in honour in his own city.’` |
| 4174 | `4` | prose | `…may pray for him,‘? and entreat on his behalf. Ye` |
| 4232 | `1` | prose | `…“4 and make offerings to the Church. And` |
| 4280 | `76` | prose | `…neither is it right for other women to teach. For` |
| 4546 | `1` | prose | `…o hath given alms to their sj` |
| 4818 | `2` | prose | `…H` |
| 4880 | `7` | prose | `…ye not an offering of the reward of fornication.”` |
| 5263 | `4` | prose | `…eternal life.”` |
| 5353 | `36` | prose | `…and body in Gehenna.”` |
| 6306 | `4` | prose | `…me. oe` |
| 6366 | `5` | prose | `…they fast.’` |
| 6381 | `2` | prose | `…K` |
| 6421 | `73` | prose | `…" Lit. save this man alive. te: stat` |
| 6429 | `18` | prose | `…said, “Thus do ye in remembrance of me.” 17 Finish` |
| 6519 | `10` | prose | `…3° The translator seems` |
| 7307 | `7` | prose | `…them."` |
| 7412 | `38` | prose | `…children 8 (and) forbid them not to come unto me.”` |
| 7540 | `5` | prose | `…signs in heaven and seduce many of the elect.’` |
| 7750 | `1` | prose | `…the whole world is mine, with the fulness thereof.` |
| 7826 | `7` | prose | `…walk in his ways, and seek him with all their heart.”` |
| 7931 | `2` | prose | `…M` |
| 8055 | `2` | prose | `…in the sight of the Lord is the death of the righteous.”` |
| 8129 | `1` | prose | `…people, even unto the people of Israel, ‘And behold` |
| 8227 | `18` | prose | `…anger.”` |
| 8884 | `4` | prose | `…(he that cometh thereto) may be worthy. to keep Thy` |

**Tier B — RUNNING PAGE HEAD — number sits on page furniture (83)**

| Line | Number | Kind | 60 chars of preceding context |
|---:|---:|---|---|
| 122 | `3` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 217 | `5` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 308 | `7` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 411 | `9` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 592 | `13` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 689 | `15` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 783 | `17` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 880 | `19` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 978 | `21` | running_head | `…THE ETEHIOPIC DIDASCALIA` |
| 1077 | `23` | running_head | `…THE EVTIIOPIC DIDASCALIA` |
| 1170 | `25` | running_head | `…THE ETHLOPIC DIDASCALIA` |
| 1263 | `27` | running_head | `…THE EVIIOPIC DIDASCALIA` |
| 1344 | `29` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 1441 | `31` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 1535 | `33` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 1627 | `35` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 1738 | `37` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 1826 | `39` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 2020 | `43` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 2114 | `45` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 2212 | `47` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 2300 | `49` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 2493 | `53` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 2593 | `55` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 2687 | `57` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 2783 | `59` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 2877 | `61` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 2984 | `63` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 3082 | `65` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 3177 | `67` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 3283 | `69` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 3366 | `71` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 3486 | `73` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 3581 | `75` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 3662 | `77` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 3798 | `79` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 3894 | `81` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 3984 | `83` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 4104 | `85` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 4198 | `87` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 4295 | `89` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 4483 | `93` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 4585 | `95` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 4678 | `97` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 4854 | `101` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 4983 | `103` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 5076 | `105` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 5157 | `107` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 5242 | `109` | running_head | `…THE EYTHIOPIC DIDASCALIA` |
| 5424 | `113` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 5514 | `115` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 5621 | `117` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 5709 | `119` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 5797 | `121` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 5943 | `123` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 6056 | `125` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 6248 | `129` | running_head | `…THE ETINOPIC DIDASCALIA` |
| 6336 | `131` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 6427 | `133` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 6523 | `135` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 6620 | `137` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 6726 | `139` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 6825 | `141` | running_head | `…THE ‘ETHIOPIC DIDASCALIA` |
| 6918 | `143` | running_head | `…THE ETHIOPIC DIDASCALIA,` |
| 7023 | `145` | running_head | `…THE ETIHOPIC DIDASCALIA` |
| 7114 | `147` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 7201 | `149` | running_head | `…THE ETHIOPIC: DIDASCALIA` |
| 7388 | `153` | running_head | `…THLE EQYHLOPIC DIDASCALIA` |
| 7482 | `155` | running_head | `…THE EVHIOPIC DIDASCALIA` |
| 7778 | `161` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 7870 | `163` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 7977 | `165` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 8066 | `167` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 8153 | `169` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 8253 | `171` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 8357 | `173` | running_head | `…HE ETHIOPIC DIDASCALIA` |
| 8451 | `175` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 8532 | `177` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 8616 | `179` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 8719 | `181` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 8806 | `183` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 8898 | `185` | running_head | `…THE ETHIOPIC DIDASCALIA` |
| 8992 | `187` | running_head | `…THE ETHIOPIC DIDASCALIA` |

**Tier C — RISKY — folio citation, referring noun, or enumeration (4)**

| Line | Number | Kind | 60 chars of preceding context |
|---:|---:|---|---|
| 3080 | `264` | enumeration | `…*° P and when ye do thus, “Ps 17,` |
| 6425 | `4` | enumeration | `…" Cf. Isa 14, 19. Ts 27,` |
| 8012 | `10` | enumeration | `…°° The Eth. word is not given °¢ Lev 20,` |
| 9163 | `1` | enumeration | `…three of these words are found in the Eth. N.T. in Mt 28,` |

## Step 2 — de-hyphenation

`word-` at end of line is joined to a continuation beginning with a
lowercase letter, unless the resulting compound is attested hyphenated
mid-line elsewhere in the same file. That attestation set is built
per-file from the original text before any joining.

### `80-serata-seyon.md` — 0 joins

None — this file has no hyphen line-breaks.

### `81-teezaz.md` — 0 joins

None — this file has no hyphen line-breaks.

### `82-gessew.md` — 0 joins

None — this file has no hyphen line-breaks.

### `84-mashafa-kidan-1.md` — 89 joins

| Line | Before → After |
|---:|---|
| 65 | `varia- / tions` → `variations` |
| 195 | `approach- / ing` → `approaching` |
| 202 | `blood- / shed` → `bloodshed` |
| 315 | `vain- / glorious` → `vainglorious` |
| 318 | `reject- / ing` → `rejecting` |
| 381 | `up- / right` → `upright` |
| 392 | `prob- / ably` → `probably` |
| 443 | `over- / come` → `overcome` |
| 490 | `over- / thrown` → `overthrown` |
| 501 | `blas- / pheme` → `blaspheme` |
| 508 | `blue- / black` → `blueblack` |
| 721 | `habita- / tion` → `habitation` |
| 742 | `com- / mandments` → `commandments` |
| 748 | `command- / ments` → `commandments` |
| 798 | `de- / tached` → `detached` |
| 849 | `this- / type` → `thistype` |
| 878 | `accord- / ing` → `according` |
| 929 | `de- / livering` → `delivering` |
| 985 | `reason- / ing` → `reasoning` |
| 1020 | `offer- / ings` → `offerings` |
| 1024 | `under- / standing` → `understanding` |
| 1068 | `with- / out` → `without` |
| 1161 | `sub- / deacons` → `subdeacons` |
| 1288 | `know- / ledge` → `knowledge` |
| 1323 | `suffer- / ing` → `suffering` |
| 1331 | `dark- / ness` → `darkness` |
| 1379 | `dis- / pleasing` → `displeasing` |
| 1385 | `sub- / dued` → `subdued` |
| 1617 | `Con- / firmer` → `Confirmer` |
| 1682 | `peace- / fulness` → `peacefulness` |
| 1698 | `them- / selves` → `themselves` |
| 1748 | `dis- / obedience` → `disobedience` |
| 1893 | `dark- / ness` → `darkness` |
| 1902 | `Intelli- / gence` → `Intelligence` |
| 1907 | `Salva- / tion` → `Salvation` |
| 1928 | `con- / fess` → `confess` |
| 1935 | `com- / prehensible` → `comprehensible` |
| 1948 | `deter- / mining` → `determining` |
| 1987 | `insepar- / able` → `inseparable` |
| 1994 | `glori- / fied` → `glorified` |
| 2097 | `par- / taking` → `partaking` |
| 2182 | `In- / effable` → `Ineffable` |
| 2202 | `laud- / ing` → `lauding` |
| 2241 | `wander- / ing` → `wandering` |
| 2379 | `utter- / ances` → `utterances` |
| 2464 | `ministra- / tions` → `ministrations` |
| 2497 | `ab- / stinence` → `abstinence` |
| 2499 | `en- / tangled` → `entangled` |
| 2505 | `per- / severe` → `persevere` |
| 2555 | `con- / demued` → `condemued` |
| 2595 | `four- / teen` → `fourteen` |
| 2711 | `forgive- / ness` → `forgiveness` |
| 2814 | `earnest- / ness` → `earnestness` |
| 2826 | `com- / munion` → `communion` |
| 2868 | `en- / lighten` → `enlighten` |
| 2902 | `con- / science` → `conscience` |
| 2950 | `re- / vealed` → `revealed` |
| 2957 | `crucify- / ing` → `crucifying` |
| 3052 | `accom- / plish` → `accomplish` |
| 3054 | `meek- / ness` → `meekness` |
| 3100 | `After- / wards` → `Afterwards` |
| 3194 | `know- / ledge` → `knowledge` |
| 3196 | `con- / tention` → `contention` |
| 3200 | `doubt- / fulness` → `doubtfulness` |
| 3202 | `enlight- / ened` → `enlightened` |
| 3225 | `pure- / ness` → `pureness` |
| 3246 | `habita- / tions` → `habitations` |
| 3287 | `distrac- / tion` → `distraction` |
| 3289 | `comeli- / ness` → `comeliness` |
| 3300 | `ex- / amples` → `examples` |
| 3370 | `dili- / gently` → `diligently` |
| 3408 | `fornica- / tion` → `fornication` |
| 3416 | `faith- / ful` → `faithful` |
| 3633 | `intelli- / gence` → `intelligence` |
| 3722 | `corrup- / tion` → `corruption` |
| 3766 | `command- / ment` → `commandment` |
| 3783 | `un- / belief` → `unbelief` |
| 3791 | `necro- / mancy` → `necromancy` |
| 3922 | `pres- / byter` → `presbyter` |
| 3942 | `pres- / byter` → `presbyter` |
| 3980 | `holi- / ness` → `holiness` |
| 4118 | `mid- / night` → `midnight` |
| 4124 | `them- / selves` → `themselves` |
| 4227 | `be- / hind` → `behind` |
| 4234 | `thanks- / givings` → `thanksgivings` |
| 4299 | `sub- / deacons` → `subdeacons` |
| 4385 | `re- / membereth` → `remembereth` |
| 4493 | `pro- / gress` → `progress` |
| 4498 | `receiv- / ing` → `receiving` |

### `86-qalementos.md` — 662 joins

| Line | Before → After |
|---:|---|
| 70 | `parti- / culières` → `particulières` |
| 82 | `docu- / ments` → `documents` |
| 93 | `Ab- / badie` → `Abbadie` |
| 145 | `mois- / sonnaïit` → `moissonnaïit` |
| 184 | `litté- / ralement` → `littéralement` |
| 193 | `con- / viennent` → `conviennent` |
| 214 | `mon- / tagne` → `montagne` |
| 245 | `Ex- / plication` → `Explication` |
| 288 | `bien- / heureux` → `bienheureux` |
| 321 | `Apô- / tres` → `Apôtres` |
| 336 | `nou- / velle` → `nouvelle` |
| 336 | `connais- / sance` → `connaissance` |
| 336 | `nais- / sance` → `naissance` |
| 343 | `Sau- / veur` → `Sauveur` |
| 349 | `mys- / tères` → `mystères` |
| 354 | `persécu- / tion` → `persécution` |
| 362 | `sou- / doiement` → `soudoiement` |
| 362 | `ex- / termination` → `extermination` |
| 371 | `connaïis- / sait` → `connaïissait` |
| 373 | `mys- / tères` → `mystères` |
| 404 | `Sei- / gneur` → `Seigneur` |
| 408 | `exté- / rieure` → `extérieure` |
| 413 | `lu- / mières` → `lumières` |
| 417 | `manifes- / tées` → `manifestées` |
| 434 | `glorifica- / tion` → `glorification` |
| 444 | `om- / bre` → `ombre` |
| 467 | `médi- / cinales` → `médicinales` |
| 474 | `con- / sidérés` → `considérés` |
| 534 | `engen- / drée` → `engendrée` |
| 548 | `trem- / blèrent` → `tremblèrent` |
| 548 | `cou- / ronné` → `couronné` |
| 553 | `Gol- / gotha` → `Golgotha` |
| 557 | `cou- / ronne` → `couronne` |
| 567 | `pro- / phète` → `prophète` |
| 592 | `exécu- / tant` → `exécutant` |
| 592 | `Chéru- / bins` → `Chérubins` |
| 596 | `com- / mandements` → `commandements` |
| 600 | `som- / meil` → `sommeil` |
| 646 | `pré- / paratoires` → `préparatoires` |
| 650 | `ar- / ménien` → `arménien` |
| 666 | `la- / quelle` → `laquelle` |
| 687 | `beau- / coup` → `beaucoup` |
| 713 | `nom- / més` → `nommés` |
| 719 | `eulo- / gie` → `eulogie` |
| 741 | `bou- / cle` → `boucle` |
| 778 | `com- / mençant` → `commençant` |
| 810 | `feuil- / let` → `feuillet` |
| 825 | `por- / tent` → `portent` |
| 856 | `In- / troduction` → `Introduction` |
| 859 | `Cons- / tantinople` → `Constantinople` |
| 865 | `o- / raison` → `oraison` |
| 871 | `Mer- / cure` → `Mercure` |
| 896 | `Ammo- / nius` → `Ammonius` |
| 905 | `Divi- / sion` → `Division` |
| 980 | `Im- / primés` → `Imprimés` |
| 993 | `Priè- / res` → `Prières` |
| 998 | `Orai- / son` → `Oraison` |
| 998 | `men- / tionnés` → `mentionnés` |
| 998 | `Dios- / core` → `Dioscore` |
| 1003 | `Théo- / dore` → `Théodore` |
| 1007 | `béné- / diction` → `bénédiction` |
| 1011 | `Sou- / riel` → `Souriel` |
| 1011 | `vieil- / lards` → `vieillards` |
| 1014 | `Geor- / ges` → `Georges` |
| 1019 | `Bar- / soma` → `Barsoma` |
| 1029 | `fa- / rann` → `farann` |
| 1032 | `Atha- / nase` → `Athanase` |
| 1047 | `Rubri- / ques` → `Rubriques` |
| 1052 | `natio- / nale` → `nationale` |
| 1075 | `incor- / porels` → `incorporels` |
| 1084 | `Dios- / core` → `Dioscore` |
| 1096 | `seule- / ment` → `seulement` |
| 1104 | `com- / mencent` → `commencent` |
| 1162 | `grà- / ces` → `gràces` |
| 1171 | `Me- / mento` → `Memento` |
| 1220 | `Me- / mento` → `Memento` |
| 1229 | `peqe- / porn` → `peqeporn` |
| 1229 | `in- / corporels` → `incorporels` |
| 1237 | `men- / tionnés` → `mentionnés` |
| 1294 | `extré- / mement` → `extrémement` |
| 1296 | `cer- / tainement` → `certainement` |
| 1304 | `hom- / mes` → `hommes` |
| 1350 | `trans- / gressé` → `transgressé` |
| 1393 | `vien- / draient` → `viendraient` |
| 1410 | `ense- / velissement` → `ensevelissement` |
| 1410 | `témoi- / gnage` → `témoignage` |
| 1422 | `pa- / radis` → `paradis` |
| 1424 | `mon- / tagne` → `montagne` |
| 1457 | `appor- / terez` → `apporterez` |
| 1515 | `em- / porter` → `emporter` |
| 1543 | `troi- / sième` → `troisième` |
| 1554 | `corrom- / prait` → `corromprait` |
| 1573 | `Sei- / gneur` → `Seigneur` |
| 1577 | `souf- / france` → `souffrance` |
| 1591 | `Séra- / phins` → `Séraphins` |
| 1594 | `extré- / mités` → `extrémités` |
| 1601 | `des- / cendra` → `descendra` |
| 1612 | `en- / tendre` → `entendre` |
| 1619 | `com- / mandement` → `commandement` |
| 1637 | `appar- / tiennent` → `appartiennent` |
| 1680 | `nai- / tra` → `naitra` |
| 1682 | `ven- / dredi` → `vendredi` |
| 1705 | `demeurè- / rent` → `demeurèrent` |
| 1705 | `peu- / ple` → `peuple` |
| 1724 | `Sei- / gneur` → `Seigneur` |
| 1733 | `tou- / chaient` → `touchaient` |
| 1862 | `persévé- / raient` → `persévéraient` |
| 1864 | `cou- / raient` → `couraient` |
| 1879 | `ac- / complissement` → `accomplissement` |
| 1891 | `beau- / coup` → `beaucoup` |
| 1896 | `extrème- / ment` → `extrèmement` |
| 1898 | `hennis- / sement` → `hennissement` |
| 1898 | `cla- / meurs` → `clameurs` |
| 1930 | `vou- / lurent` → `voulurent` |
| 1945 | `commande- / ments` → `commandements` |
| 1960 | `res- / taient` → `restaient` |
| 1965 | `Sei- / gneur` → `Seigneur` |
| 1995 | `miséricor- / dieux` → `miséricordieux` |
| 1999 | `Sei- / gneur` → `Seigneur` |
| 2021 | `retour- / nât` → `retournât` |
| 2047 | `La- / mech` → `Lamech` |
| 2049 | `Md- / tousâlà` → `Mdtousâlà` |
| 2058 | `ac- / corde` → `accorde` |
| 2119 | `ani- / maux` → `animaux` |
| 2122 | `in- / humation` → `inhumation` |
| 2122 | `vête- / ments` → `vêtements` |
| 2135 | `prescrip- / tion` → `prescription` |
| 2137 | `Magä- / bit` → `Magäbit` |
| 2149 | `Tré- / sors` → `Trésors` |
| 2163 | `des- / cendus` → `descendus` |
| 2166 | `Mon- / tagne` → `Montagne` |
| 2168 | `tom- / berez` → `tomberez` |
| 2186 | `dé- / posa` → `déposa` |
| 2198 | `af- / fliction` → `affliction` |
| 2200 | `bénissez- / nous` → `bénisseznous` |
| 2218 | `cor- / beau` → `corbeau` |
| 2235 | `demeu- / rèrent` → `demeurèrent` |
| 2251 | `Bahäy- / nos` → `Bahäynos` |
| 2271 | `sur- / face` → `surface` |
| 2273 | `monta- / gnes` → `montagnes` |
| 2273 | `portè- / rent` → `portèrent` |
| 2288 | `arrêtè- / rent` → `arrêtèrent` |
| 2298 | `cor- / beau` → `corbeau` |
| 2301 | `cou- / chait` → `couchait` |
| 2306 | `mani- / festés` → `manifestés` |
| 2309 | `commanüe- / ment` → `commanüement` |
| 2317 | `demeu- / raient` → `demeuraient` |
| 2339 | `nom- / bre` → `nombre` |
| 2339 | `person- / nes` → `personnes` |
| 2346 | `châti- / ment` → `châtiment` |
| 2357 | `dé- / couvrirent` → `découvrirent` |
| 2360 | `Lors- / que` → `Lorsque` |
| 2370 | `tom- / bés` → `tombés` |
| 2372 | `Mosi- / réwiens` → `Mosiréwiens` |
| 2378 | `som- / meil` → `sommeil` |
| 2419 | `en- / droit` → `endroit` |
| 2428 | `a- / vaient` → `avaient` |
| 2442 | `per- / sonne` → `personne` |
| 2466 | `soigneuse- / ment` → `soigneusement` |
| 2499 | `rede- / vint` → `redevint` |
| 2523 | `éprouve- / rent` → `éprouverent` |
| 2548 | `ense- / velit` → `ensevelit` |
| 2552 | `ense- / velit` → `ensevelit` |
| 2556 | `ense- / velit` → `ensevelit` |
| 2609 | `jus- / qu` → `jusqu` |
| 2618 | `éme- / raude` → `émeraude` |
| 2634 | `jus- / qu` → `jusqu` |
| 2668 | `Trem- / blement` → `Tremblement` |
| 2674 | `adorè- / rent` → `adorèrent` |
| 2690 | `con- / traire` → `contraire` |
| 2728 | `sorcel- / lerie` → `sorcellerie` |
| 2732 | `Sei- / gneur` → `Seigneur` |
| 2732 | `com- / ment` → `comment` |
| 2741 | `monta- / gnes` → `montagnes` |
| 2745 | `col- / lines` → `collines` |
| 2745 | `mon- / tagnes` → `montagnes` |
| 2748 | `ado- / raient` → `adoraient` |
| 2774 | `che- / val` → `cheval` |
| 2777 | `lors- / que` → `lorsque` |
| 2783 | `philoso- / phie` → `philosophie` |
| 2794 | `en- / seigne` → `enseigne` |
| 2817 | `astrono- / ne` → `astronone` |
| 2847 | `yeypauué- / vov` → `yeypauuévov` |
| 2885 | `xutohryo- / pe` → `xutohryope` |
| 2931 | `évhowra- / péox` → `évhowrapéox` |
| 2989 | `Ümo- / rlbevrar` → `Ümorlbevrar` |
| 3081 | `auvdtæ- / rpléev` → `auvdtærpléev` |
| 3175 | `TAt- / deuer` → `TAtdeuer` |
| 3210 | `pn- / déve` → `pndéve` |
| 3229 | `ed- / gp` → `edgp` |
| 3288 | `u- / mnpov` → `umnpov` |
| 3334 | `oma- / v` → `omav` |
| 3471 | `mpocye- / po` → `mpocyepo` |
| 3585 | `drro- / c` → `drroc` |
| 3602 | `Ta- / paresovrt` → `Taparesovrt` |
| 3667 | `aouu- / popouc` → `aouupopouc` |
| 3803 | `xara- / ppovouvrwv` → `xarappovouvrwv` |
| 3821 | `eù- / voiae` → `eùvoiae` |
| 3904 | `avri- / doctc` → `avridoctc` |
| 3945 | `pyiuay- / pirn` → `pyiuaypirn` |
| 4031 | `éco- / mel` → `écomel` |
| 4104 | `Ékenuo- / cuvny` → `Ékenuocuvny` |
| 4107 | `a- / pl` → `apl` |
| 4129 | `xaXEt- / rat` → `xaXEtrat` |
| 4181 | `Evi- / dp` → `Evidp` |
| 4253 | `Kü- / puov` → `Küpuov` |
| 4316 | `maxpu- / vert` → `maxpuvert` |
| 4374 | `tpoc- / ayopeubvar` → `tpocayopeubvar` |
| 4419 | `yevo- / p` → `yevop` |
| 4548 | `cata- / logue` → `catalogue` |
| 4553 | `pagi- / nation` → `pagination` |
| 4582 | `Paralipo- / mènes` → `Paralipomènes` |
| 4589 | `li- / gnes` → `lignes` |
| 4592 | `apo- / cryphe` → `apocryphe` |
| 4620 | `e- / raf` → `eraf` |
| 4675 | `aveugle- / né` → `aveuglené` |
| 4677 | `pas- / sion` → `passion` |
| 4686 | `apô- / tre` → `apôtre` |
| 4724 | `Thessaloni- / ciens` → `Thessaloniciens` |
| 4754 | `li- / gnes` → `lignes` |
| 4762 | `apo- / cryphe` → `apocryphe` |
| 4767 | `Ag- / gée` → `Aggée` |
| 4777 | `li- / gnes` → `lignes` |
| 4791 | `Haÿmaä- / not` → `Haÿmaänot` |
| 4826 | `Ro- / mains` → `Romains` |
| 4834 | `Apô- / tres` → `Apôtres` |
| 4906 | `cérémo- / nies` → `cérémonies` |
| 4914 | `li- / gnes` → `lignes` |
| 4943 | `com- / position` → `composition` |
| 4962 | `appe- / lées` → `appelées` |
| 5008 | `Ra- / phaël` → `Raphaël` |
| 5013 | `Lamenta- / tions` → `Lamentations` |
| 5025 | `li- / gnes` → `lignes` |
| 5033 | `li- / gnes` → `lignes` |
| 5066 | `li- / gnes` → `lignes` |
| 5085 | `di- / vers` → `divers` |
| 5085 | `Sé- / vère` → `Sévère` |
| 5100 | `con- / tenant` → `contenant` |
| 5102 | `for- / mules` → `formules` |
| 5102 | `cer- / taines` → `certaines` |
| 5159 | `Com- / plies` → `Complies` |
| 5179 | `mys- / tères` → `mystères` |
| 5208 | `Sau- / veur` → `Sauveur` |
| 5229 | `mo- / gasa` → `mogasa` |
| 5231 | `za- / nagh` → `zanagh` |
| 5239 | `pla- / cés` → `placés` |
| 5283 | `saber- / hänaät` → `saberhänaät` |
| 5283 | `amha- / rique` → `amharique` |
| 5283 | `priè- / res` → `prières` |
| 5299 | `Lamen- / tations` → `Lamentations` |
| 5306 | `li- / gnes` → `lignes` |
| 5326 | `zaga- / barka` → `zagabarka` |
| 5336 | `Man- / fas` → `Manfas` |
| 5341 | `li- / gnes` → `lignes` |
| 5350 | `li- / gnes` → `lignes` |
| 5556 | `Pro- / phétie` → `Prophétie` |
| 5556 | `Lamen- / tations` → `Lamentations` |
| 5559 | `Pa- / ralipomènes` → `Paralipomènes` |
| 5630 | `ma- / riage` → `mariage` |
| 5668 | `Sa- / fäm` → `Safäm` |
| 5689 | `frag- / ments` → `fragments` |
| 5699 | `con- / tenus` → `contenus` |
| 5779 | `ex- / plication` → `explication` |
| 5790 | `jan- / vier` → `janvier` |
| 5808 | `ce- / lui` → `celui` |
| 5833 | `sem- / ble` → `semble` |
| 5857 | `posses- / sion` → `possession` |
| 5869 | `en- / flamimés` → `enflamimés` |
| 5871 | `bien- / heureux` → `bienheureux` |
| 5904 | `édite- / rons` → `éditerons` |
| 5909 | `ménolo- / ges` → `ménologes` |
| 5920 | `Codi- / ces` → `Codices` |
| 5939 | `écri- / ture` → `écriture` |
| 6095 | `archi- / diaconat` → `archidiaconat` |
| 6109 | `imposi- / tion` → `imposition` |
| 6115 | `cou- / tumes` → `coutumes` |
| 6118 | `beau- / coup` → `beaucoup` |
| 6118 | `ar- / chidiacre` → `archidiacre` |
| 6122 | `Sy- / riens` → `Syriens` |
| 6126 | `An- / tioche` → `Antioche` |
| 6131 | `en- / suite` → `ensuite` |
| 6131 | `syria- / que` → `syriaque` |
| 6135 | `Anga- / male` → `Angamale` |
| 6147 | `évé- / que` → `évéque` |
| 6153 | `com- / mencça` → `commencça` |
| 6175 | `Ma- / labar` → `Malabar` |
| 6185 | `mo- / ment` → `moment` |
| 6189 | `Es- / prit` → `Esprit` |
| 6191 | `sy- / riens` → `syriens` |
| 6208 | `sub- / stances` → `substances` |
| 6225 | `évé- / que` → `évéque` |
| 6225 | `habi- / tudes` → `habitudes` |
| 6235 | `mon- / tagnards` → `montagnards` |
| 6252 | `Sal- / vator` → `Salvator` |
| 6259 | `piè- / ces` → `pièces` |
| 6261 | `Mala- / bar` → `Malabar` |
| 6293 | `arri- / vés` → `arrivés` |
| 6299 | `Catho- / lique` → `Catholique` |
| 6306 | `évé- / ques` → `évéques` |
| 6319 | `résurrec- / tion` → `résurrection` |
| 6330 | `vête- / ments` → `vêtements` |
| 6343 | `Théo- / dore` → `Théodore` |
| 6350 | `Sep- / tembre` → `Septembre` |
| 6357 | `Sei- / gneur` → `Seigneur` |
| 6374 | `compo- / ser` → `composer` |
| 6424 | `Sei- / gneur` → `Seigneur` |
| 6453 | `As- / somption` → `Assomption` |
| 6465 | `bienheu- / reuse` → `bienheureuse` |
| 6485 | `manus- / crit` → `manuscrit` |
| 6485 | `con- / verti` → `converti` |
| 6485 | `ma- / nuscrit` → `manuscrit` |
| 6498 | `déli- / ces` → `délices` |
| 6509 | `manus- / crit` → `manuscrit` |
| 6509 | `dis- / ciple` → `disciple` |
| 6509 | `ail- / leurs` → `ailleurs` |
| 6540 | `com- / prime` → `comprime` |
| 6566 | `occa- / sion` → `occasion` |
| 6576 | `vo- / hume` → `vohume` |
| 6585 | `seule- / ment` → `seulement` |
| 6595 | `de- / voir` → `devoir` |
| 6649 | `Décapita- / tion` → `Décapitation` |
| 6692 | `reprodui- / sons` → `reproduisons` |
| 6695 | `vain- / queurs` → `vainqueurs` |
| 6714 | `Jérusa- / lem` → `Jérusalem` |
| 6724 | `Qal- / qasandi` → `Qalqasandi` |
| 6737 | `con- / damnés` → `condamnés` |
| 6747 | `Pto- / lémée` → `Ptolémée` |
| 6775 | `Êde- / pévrwv` → `Êdepévrwv` |
| 6809 | `ac- / compagnaient` → `accompagnaient` |
| 6811 | `rache- / ter` → `racheter` |
| 6827 | `décom- / position` → `décomposition` |
| 6829 | `occu- / pait` → `occupait` |
| 6887 | `Aroxx- / réoraoic` → `Aroxxréoraoic` |
| 6972 | `len- / tille` → `lentille` |
| 6972 | `traver- / saient` → `traversaient` |
| 6975 | `reti- / rèrent` → `retirèrent` |
| 7000 | `pro- / phète` → `prophète` |
| 7006 | `im- / pure` → `impure` |
| 7014 | `rappor- / tent` → `rapportent` |
| 7083 | `lende- / main` → `lendemain` |
| 7276 | `com- / pulsera` → `compulsera` |
| 7289 | `sous- / cripteurs` → `souscripteurs` |
| 7297 | `pou- / vaient` → `pouvaient` |
| 7301 | `ar- / gent` → `argent` |
| 7319 | `si- / cles` → `sicles` |
| 7350 | `par- / ties` → `parties` |
| 7350 | `ar- / chitrave` → `architrave` |
| 7350 | `ins- / cription` → `inscription` |
| 7383 | `con- / fusion` → `confusion` |
| 7393 | `tra- / duction` → `traduction` |
| 7397 | `anec- / dotes` → `anecdotes` |
| 7403 | `succes- / sivement` → `successivement` |
| 7408 | `prépa- / ration` → `préparation` |
| 7420 | `tra- / duction` → `traduction` |
| 7439 | `Pléro- / phories` → `Plérophories` |
| 7450 | `scho- / larum` → `scholarum` |
| 7457 | `Damas- / cène` → `Damascène` |
| 7469 | `Sophro- / nius` → `Sophronius` |
| 7475 | `Écri- / ture` → `Écriture` |
| 7487 | `théo- / logique` → `théologique` |
| 7493 | `indis- / pensable` → `indispensable` |
| 7498 | `nom- / breuses` → `nombreuses` |
| 7498 | `héré- / sies` → `hérésies` |
| 7498 | `orien- / taux` → `orientaux` |
| 7513 | `Impri- / meries` → `Imprimeries` |
| 7518 | `tra- / duire` → `traduire` |
| 7527 | `Jona- / than` → `Jonathan` |
| 7527 | `ter- / restre` → `terrestre` |
| 7561 | `inté- / ressant` → `intéressant` |
| 7563 | `Ahas- / xeros` → `Ahasxeros` |
| 7607 | `des- / criptions` → `descriptions` |
| 7617 | `byzan- / tiologique` → `byzantiologique` |
| 7630 | `heureuse- / ment` → `heureusement` |
| 7640 | `para- / phrasés` → `paraphrasés` |
| 7667 | `con- / naissances` → `connaissances` |
| 7670 | `contri- / buera` → `contribuera` |
| 7674 | `im- / portante` → `importante` |
| 7676 | `De- / lehaye` → `Delehaye` |
| 7679 | `orien- / taux` → `orientaux` |
| 7679 | `Aréopa- / gite` → `Aréopagite` |
| 7685 | `Eu- / graphus` → `Eugraphus` |
| 7689 | `Mu- / seum` → `Museum` |
| 7691 | `prin- / cipaux` → `principaux` |
| 7705 | `ora- / toire` → `oratoire` |
| 7717 | `Bar- / berini` → `Barberini` |
| 7722 | `tra- / duction` → `traduction` |
| 7737 | `con- / servée` → `conservée` |
| 7744 | `iden- / tifie` → `identifie` |
| 7755 | `a- / près` → `après` |
| 7755 | `prédé- / cesseurs` → `prédécesseurs` |
| 7815 | `des- / truction` → `destruction` |
| 7858 | `mar- / tyr` → `martyr` |
| 7878 | `Geor- / gius` → `Georgius` |
| 7903 | `mar- / tyrisés` → `martyrisés` |
| 7922 | `Lipo- / manus` → `Lipomanus` |
| 7940 | `briè- / yement` → `brièyement` |
| 7976 | `répon- / dirent` → `répondirent` |
| 8139 | `recom- / mandations` → `recommandations` |
| 8147 | `descen- / dra` → `descendra` |
| 8158 | `ten- / tation` → `tentation` |
| 8160 | `rédemp- / lion` → `rédemplion` |
| 8168 | `Pas- / sage` → `Passage` |
| 8180 | `servi- / teur` → `serviteur` |
| 8199 | `geo- / lier` → `geolier` |
| 8210 | `Mat- / thieu` → `Matthieu` |
| 8212 | `par- / tirent` → `partirent` |
| 8246 | `servi- / teur` → `serviteur` |
| 8372 | `accom- / plit` → `accomplit` |
| 8394 | `Césa- / rée` → `Césarée` |
| 8421 | `main- / tenant` → `maintenant` |
| 8436 | `asso- / cié` → `associé` |
| 8448 | `Sei- / gneur` → `Seigneur` |
| 8470 | `mys- / tère` → `mystère` |
| 8497 | `par- / donner` → `pardonner` |
| 8566 | `Abra- / ham` → `Abraham` |
| 8592 | `Melchisé- / dec` → `Melchisédec` |
| 8608 | `en- / gendra` → `engendra` |
| 8620 | `Sei- / gneur` → `Seigneur` |
| 8620 | `Lors- / qu` → `Lorsqu` |
| 8644 | `ap- / pelle` → `appelle` |
| 8647 | `Welchi- / sédec` → `Welchisédec` |
| 8653 | `ré- / jour` → `réjour` |
| 8656 | `A- / braham` → `Abraham` |
| 8660 | `Melchi- / séclec` → `Melchiséclec` |
| 8671 | `deman- / dèrent` → `demandèrent` |
| 8696 | `men- / tionné` → `mentionné` |
| 8744 | `Construc- / tion` → `Construction` |
| 8755 | `Sei- / gneur` → `Seigneur` |
| 8768 | `au- / tour` → `autour` |
| 8852 | `Sei- / gneuwr` → `Seigneuwr` |
| 8877 | `supplica- / tion` → `supplication` |
| 8913 | `a- / son` → `ason` |
| 8913 | `gé- / nérations` → `générations` |
| 8956 | `Sei- / gneur` → `Seigneur` |
| 8966 | `pen- / dant` → `pendant` |
| 9005 | `Abi- / mélec` → `Abimélec` |
| 9015 | `Philis- / tins` → `Philistins` |
| 9074 | `précé- / demment` → `précédemment` |
| 9129 | `fu- / rent` → `furent` |
| 9159 | `au- / guste` → `auguste` |
| 9180 | `sou- / viendrez` → `souviendrez` |
| 9194 | `révéle- / rai` → `révélerai` |
| 9201 | `mys- / tères` → `mystères` |
| 9207 | `bou- / che` → `bouche` |
| 9207 | `épou- / vante` → `épouvante` |
| 9212 | `au- / rais` → `aurais` |
| 9217 | `vien- / dront` → `viendront` |
| 9233 | `antérieure- / ment` → `antérieurement` |
| 9233 | `conte- / nait` → `contenait` |
| 9246 | `Es- / prit` → `Esprit` |
| 9250 | `in- / termédiaire` → `intermédiaire` |
| 9254 | `con- / naît` → `connaît` |
| 9254 | `des- / sus` → `dessus` |
| 9263 | `miséri- / corde` → `miséricorde` |
| 9269 | `bienveil- / lance` → `bienveillance` |
| 9277 | `Es- / prit` → `Esprit` |
| 9320 | `trou- / vions` → `trouvions` |
| 9332 | `ap- / pelé` → `appelé` |
| 9335 | `va- / riées` → `variées` |
| 9350 | `om- / brage` → `ombrage` |
| 9350 | `cons- / truction` → `construction` |
| 9354 | `cou- / ronnée` → `couronnée` |
| 9357 | `ef- / fet` → `effet` |
| 9357 | `éta- / blie` → `établie` |
| 9382 | `tou- / tes` → `toutes` |
| 9387 | `é- / galent` → `égalent` |
| 9393 | `or- / donné` → `ordonné` |
| 9396 | `glori- / fient` → `glorifient` |
| 9400 | `de- / meure` → `demeure` |
| 9403 | `prin- / ces` → `princes` |
| 9413 | `seule- / ment` → `seulement` |
| 9439 | `Sei- / gneur` → `Seigneur` |
| 9463 | `corrup- / tible` → `corruptible` |
| 9463 | `Per- / sonne` → `Personne` |
| 9481 | `ap- / paru` → `apparu` |
| 9498 | `Clé- / ment` → `Clément` |
| 9500 | `fu- / rent` → `furent` |
| 9615 | `ré- / pons` → `répons` |
| 9618 | `his- / torien` → `historien` |
| 9629 | `cons- / titution` → `constitution` |
| 9632 | `hiéro- / solymitaine` → `hiérosolymitaine` |
| 9635 | `Bour- / de` → `Bourde` |
| 9635 | `impé- / riale` → `impériale` |
| 9641 | `allu- / sion` → `allusion` |
| 9649 | `attribu- / tion` → `attribution` |
| 9649 | `Théo- / phane` → `Théophane` |
| 9653 | `mono- / physite` → `monophysite` |
| 9653 | `bio- / graphe` → `biographe` |
| 9660 | `con- / server` → `conserver` |
| 9666 | `considé- / rable` → `considérable` |
| 9690 | `hono- / rée` → `honorée` |
| 9693 | `change- / ment` → `changement` |
| 9734 | `monophy- / sites` → `monophysites` |
| 9738 | `Sé- / vère` → `Sévère` |
| 9741 | `In- / carnation` → `Incarnation` |
| 9754 | `hypos- / tatique` → `hypostatique` |
| 9778 | `monophy- / site` → `monophysite` |
| 9780 | `inca- / pables` → `incapables` |
| 9798 | `dis- / persé` → `dispersé` |
| 9811 | `Ma- / cedonius` → `Macedonius` |
| 9822 | `Ma- / rie` → `Marie` |
| 9831 | `consubs- / tantiel` → `consubstantiel` |
| 9834 | `se- / rait` → `serait` |
| 9834 | `u- / nité` → `unité` |
| 9838 | `nom- / bre` → `nombre` |
| 9842 | `intro- / duisant` → `introduisant` |
| 9842 | `plu- / sieurs` → `plusieurs` |
| 9845 | `incon- / vénient` → `inconvénient` |
| 9847 | `recon- / naître` → `reconnaître` |
| 9850 | `Constantino- / ple` → `Constantinople` |
| 9853 | `or- / thodoxie` → `orthodoxie` |
| 9867 | `provo- / qué` → `provoqué` |
| 9869 | `cor- / rections` → `corrections` |
| 9876 | `catho- / liqués` → `catholiqués` |
| 9880 | `sur- / tout` → `surtout` |
| 9894 | `Lors- / que` → `Lorsque` |
| 9900 | `sui- / vant` → `suivant` |
| 9904 | `Ca- / brol` → `Cabrol` |
| 9911 | `tradi- / tionnelle` → `traditionnelle` |
| 9915 | `ana- / phore` → `anaphore` |
| 9918 | `rap- / porter` → `rapporter` |
| 9920 | `paral- / lèle` → `parallèle` |
| 9926 | `obser- / ver` → `observer` |
| 9931 | `Re- / naudot` → `Renaudot` |
| 9933 | `pres- / que` → `presque` |
| 9947 | `habille- / ment` → `habillement` |
| 9956 | `compre- / nant` → `comprenant` |
| 9958 | `se- / conde` → `seconde` |
| 9958 | `compre- / nait` → `comprenait` |
| 9967 | `prouvent- / elles` → `prouventelles` |
| 9984 | `par- / faite` → `parfaite` |
| 9986 | `cor- / rections` → `corrections` |
| 9991 | `canonia- / les` → `canoniales` |
| 9993 | `Do- / mini` → `Domini` |
| 10022 | `ana- / logue` → `analogue` |
| 10025 | `ana- / phore` → `anaphore` |
| 10027 | `re- / lever` → `relever` |
| 10027 | `ap- / préciable` → `appréciable` |
| 10034 | `Cté- / siphon` → `Ctésiphon` |
| 10040 | `néces- / saire` → `nécessaire` |
| 10058 | `for- / mules` → `formules` |
| 10072 | `consécra- / tion` → `consécration` |
| 10072 | `ra- / conte` → `raconte` |
| 10077 | `mys- / tère` → `mystère` |
| 10086 | `sin- / gulière` → `singulière` |
| 10101 | `géné- / rale` → `générale` |
| 10104 | `attri- / buée` → `attribuée` |
| 10106 | `u- / sage` → `usage` |
| 10114 | `bor- / nes` → `bornes` |
| 10121 | `ap- / pela` → `appela` |
| 10140 | `der- / niers` → `derniers` |
| 10146 | `supers- / titieux` → `superstitieux` |
| 10153 | `parcou- / rir` → `parcourir` |
| 10158 | `néces- / saire` → `nécessaire` |
| 10164 | `nou- / velle` → `nouvelle` |
| 10177 | `pre- / mière` → `première` |
| 10187 | `accom- / plir` → `accomplir` |
| 10200 | `accom- / plie` → `accomplie` |
| 10200 | `Eucha- / ristie` → `Eucharistie` |
| 10207 | `dénon- / cée` → `dénoncée` |
| 10247 | `rele- / ver` → `relever` |
| 10258 | `a- / bolition` → `abolition` |
| 10260 | `sain- / tes` → `saintes` |
| 10260 | `com- / munion` → `communion` |
| 10264 | `préa- / lablement` → `préalablement` |
| 10272 | `litur- / gie` → `liturgie` |
| 10275 | `auto- / rité` → `autorité` |
| 10296 | `TpOEpn- / uéva` → `TpOEpnuéva` |
| 10316 | `Bubav- / riohoyuxñs` → `Bubavriohoyuxñs` |
| 10330 | `ieco- / uovéyou` → `iecouovéyou` |
| 10354 | `Histo- / rische` → `Historische` |
| 10354 | `droonuetw- / get` → `droonuetwget` |
| 10384 | `dio- / bien` → `diobien` |
| 10384 | `To- / créhwv` → `Tocréhwv` |
| 10384 | `POVONG- / varos` → `POVONGvaros` |
| 10389 | `Mont- / faucon` → `Montfaucon` |
| 10396 | `pLeyxko- / ppruooç` → `pLeyxkoppruooç` |
| 10402 | `Ypovolo- / yiav` → `Ypovoloyiav` |
| 10405 | `Eevopé- / vous` → `Eevopévous` |
| 10415 | `Ei- / var` → `Eivar` |
| 10428 | `Khau- / diov` → `Khaudiov` |
| 10428 | `Bouév- / os` → `Bouévos` |
| 10444 | `Auo- / vustou` → `Auovustou` |
| 10459 | `Apxao- / doyixñc` → `Apxaodoyixñc` |
| 10468 | `Auovu- / ciou` → `Auovuciou` |
| 10473 | `xepi- / mou` → `xepimou` |
| 10551 | `uépri- / viavoü` → `uépriviavoü` |
| 10615 | `ava- / oi` → `avaoi` |
| 10664 | `Aaux- / cxnvôv` → `Aauxcxnvôv` |
| 10708 | `o- / perdrara` → `operdrara` |
| 10855 | `Favo- / rinus` → `Favorinus` |
| 10861 | `Aoya- / practice` → `Aoyapractice` |
| 10887 | `Évan- / gile` → `Évangile` |
| 10896 | `re- / ligieux` → `religieux` |
| 10901 | `An- / tioche` → `Antioche` |
| 10934 | `His- / toire` → `Histoire` |
| 10959 | `con- / fessé` → `confessé` |
| 10978 | `His- / toire` → `Histoire` |
| 10985 | `Phi- / lippe` → `Philippe` |
| 10995 | `Logi- / que` → `Logique` |
| 10998 | `correspon- / dance` → `correspondance` |
| 10998 | `Ham- / bali` → `Hambali` |
| 11002 | `ano- / nyme` → `anonyme` |
| 11029 | `mé- / dicale` → `médicale` |
| 11057 | `Kuri- / kos` → `Kurikos` |
| 11060 | `direc- / tion` → `direction` |
| 11060 | `ar- / ticles` → `articles` |
| 11067 | `in- / tellectuel` → `intellectuel` |
| 11084 | `Jac- / ques` → `Jacques` |
| 11098 | `Mous- / tafa` → `Moustafa` |
| 11114 | `au- / dience` → `audience` |
| 11137 | `mo- / rale` → `morale` |
| 11137 | `Has- / sih` → `Hassih` |
| 11144 | `ma- / nuscrits` → `manuscrits` |
| 11161 | `survien- / dront` → `surviendront` |
| 11164 | `ca- / lamités` → `calamités` |
| 11166 | `héré- / sies` → `hérésies` |
| 11173 | `Ascen- / sion` → `Ascension` |
| 11180 | `se- / maines` → `semaines` |
| 11196 | `jus- / qu` → `jusqu` |
| 11201 | `cru- / cifié` → `crucifié` |
| 11206 | `fidè- / les` → `fidèles` |
| 11206 | `Com- / prends` → `Comprends` |
| 11212 | `divul- / gué` → `divulgué` |
| 11216 | `Badri- / non` → `Badrinon` |
| 11218 | `ap- / pelle` → `appelle` |
| 11224 | `Mesel- / mâniens` → `Meselmâniens` |
| 11224 | `Berdhi- / tiens` → `Berdhitiens` |
| 11224 | `Fatsiligä- / niens` → `Fatsiligäniens` |
| 11258 | `sup- / plié` → `supplié` |
| 11258 | `pa- / radis` → `paradis` |
| 11280 | `pen- / dant` → `pendant` |
| 11283 | `ma- / lice` → `malice` |
| 11283 | `ar- / bres` → `arbres` |
| 11287 | `ar- / gent` → `argent` |
| 11314 | `livre- / rai` → `livrerai` |
| 11317 | `se- / ront` → `seront` |
| 11319 | `lut- / tera` → `luttera` |
| 11330 | `rassasie- / ront` → `rassasieront` |
| 11335 | `pro- / chain` → `prochain` |
| 11335 | `fidè- / les` → `fidèles` |
| 11350 | `perdi- / tion` → `perdition` |
| 11364 | `saC- / cagé` → `saCcagé` |
| 11364 | `mira- / cles` → `miracles` |
| 11371 | `se- / ront` → `seront` |
| 11389 | `pleu- / reront` → `pleureront` |
| 11398 | `croi- / ront` → `croiront` |
| 11404 | `som- / meil` → `sommeil` |
| 11417 | `Sanälä- / niens` → `Sanäläniens` |
| 11427 | `Tersi- / tiens` → `Tersitiens` |
| 11434 | `renie- / ront` → `renieront` |
| 11456 | `puis- / sance` → `puissance` |
| 11481 | `héré- / tique` → `hérétique` |
| 11495 | `vipè- / res` → `vipères` |
| 11528 | `de- / puis` → `depuis` |
| 11528 | `ré- / gions` → `régions` |
| 11590 | `fi- / dèles` → `fidèles` |
| 11602 | `évé- / nements` → `événements` |
| 11609 | `pre- / mier` → `premier` |
| 11634 | `par- / viendra` → `parviendra` |
| 11650 | `pratique- / ront` → `pratiqueront` |
| 11655 | `jus- / tice` → `justice` |

### `87-didascalia.md` — 230 joins

| Line | Before → After |
|---:|---|
| 106 | `joint- / partakers` → `jointpartakers` |
| 112 | `com- / mandments` → `commandments` |
| 181 | `neigh- / bour` → `neighbour` |
| 188 | `like- / wise` → `likewise` |
| 247 | `thy- / self` → `thyself` |
| 284 | `compas- / sion` → `compassion` |
| 317 | `interpre- / tation` → `interpretation` |
| 367 | `command- / ments` → `commandments` |
| 404 | `counten- / ance` → `countenance` |
| 427 | `two- / edged` → `twoedged` |
| 445 | `unclean- / ness` → `uncleanness` |
| 531 | `com- / passion` → `compassion` |
| 535 | `thy- / self` → `thyself` |
| 611 | `further- / more` → `furthermore` |
| 719 | `modera- / tion` → `moderation` |
| 765 | `com- / mandment` → `commandment` |
| 817 | `condemna- / tion` → `condemnation` |
| 912 | `command- / ment` → `commandment` |
| 962 | `What- / soever` → `Whatsoever` |
| 1016 | `repent- / ance` → `repentance` |
| 1029 | `our- / selves` → `ourselves` |
| 1118 | `con- / demneth` → `condemneth` |
| 1180 | `him- / self` → `himself` |
| 1480 | `trans- / grressors` → `transgrressors` |
| 1530 | `he- / goats` → `hegoats` |
| 1632 | `understand- / ing` → `understanding` |
| 1640 | `peace- / maker` → `peacemaker` |
| 1789 | `con- / verted` → `converted` |
| 1889 | `trans- / children` → `transchildren` |
| 1920 | `com- / passion` → `compassion` |
| 1936 | `supplica- / tion` → `supplication` |
| 1990 | `com- / mitteth` → `committeth` |
| 2006 | `forgive- / ness` → `forgiveness` |
| 2059 | `afflic- / tion` → `affliction` |
| 2123 | `them- / selves` → `themselves` |
| 2131 | `com- / manded` → `commanded` |
| 2225 | `whatso- / ever` → `whatsoever` |
| 2286 | `punctua- / lows` → `punctualows` |
| 2441 | `appoint- / ment` → `appointment` |
| 2452 | `them- / selves` → `themselves` |
| 2543 | `concern- / ing` → `concerning` |
| 2693 | `King- / dom` → `Kingdom` |
| 2698 | `up- / rightness` → `uprightness` |
| 2705 | `any- / thing` → `anything` |
| 2735 | `com- / manded` → `commanded` |
| 2753 | `con- / straining` → `constraining` |
| 2903 | `Where- / fore` → `Wherefore` |
| 2963 | `un- / certain` → `uncertain` |
| 2980 | `re- / ceive` → `receive` |
| 2996 | `trans- / gression` → `transgression` |
| 3062 | `condemna- / tion` → `condemnation` |
| 3093 | `super- / fluous` → `superfluous` |
| 3214 | `judg- / ment` → `judgment` |
| 3233 | `pro- / ceedeth` → `proceedeth` |
| 3236 | `upright- / ness` → `uprightness` |
| 3253 | `testi- / mony` → `testimony` |
| 3264 | `cor- / right` → `corright` |
| 3275 | `Jeru- / salem` → `Jerusalem` |
| 3326 | `con- / demnation` → `condemnation` |
| 3328 | `upright- / ness` → `uprightness` |
| 3461 | `trans- / lates` → `translates` |
| 3476 | `neigh- / bour` → `neighbour` |
| 3508 | `teach- / ing` → `teaching` |
| 3510 | `accord- / ing` → `according` |
| 3517 | `command- / ments` → `commandments` |
| 3575 | `persecu- / tions` → `persecutions` |
| 3633 | `fellow- / labourer` → `fellowlabourer` |
| 3690 | `sen- / following` → `senfollowing` |
| 3768 | `im- / plics` → `implics` |
| 3770 | `re- / main` → `remain` |
| 3792 | `pur- / chased` → `purchased` |
| 3792 | `re- / deemed` → `redeemed` |
| 3850 | `command- / ments` → `commandments` |
| 3900 | `them- / selves` → `themselves` |
| 3926 | `my- / voice` → `myvoice` |
| 4099 | `re- / ferring` → `referring` |
| 4113 | `dif- / ferent` → `different` |
| 4129 | `trans- / lates` → `translates` |
| 4187 | `con- / tinually` → `continually` |
| 4213 | `mani- / fested` → `manifested` |
| 4231 | `con- / demnation` → `condemnation` |
| 4234 | `righteous- / ness` → `righteousness` |
| 4234 | `concern- / ing` → `concerning` |
| 4360 | `Magde- / lene` → `Magdelene` |
| 4453 | `com- / mand` → `command` |
| 4469 | `money- / its` → `moneyits` |
| 4499 | `know- / ledge` → `knowledge` |
| 4508 | `com- / mand` → `command` |
| 4535 | `con- / demnation` → `condemnation` |
| 4626 | `in- / somuch` → `insomuch` |
| 4638 | `under- / stand` → `understand` |
| 4669 | `accord- / itp` → `accorditp` |
| 4750 | `congre- / gation` → `congregation` |
| 4859 | `Phari- / the` → `Pharithe` |
| 4887 | `Where- / fore` → `Wherefore` |
| 4974 | `drunken- / ness` → `drunkenness` |
| 5007 | `understand- / ing` → `understanding` |
| 5055 | `com- / manded` → `commanded` |
| 5108 | `pol- / luted` → `polluted` |
| 5115 | `sus- / tenance` → `sustenance` |
| 5142 | `concern- / ing` → `concerning` |
| 5157 | `accord- / ing` → `according` |
| 5185 | `handi- / craft` → `handicraft` |
| 5189 | `condemna- / tion` → `condemnation` |
| 5283 | `imprison- / ment` → `imprisonment` |
| 5319 | `Who- / soever` → `Whosoever` |
| 5381 | `un- / godly` → `ungodly` |
| 5415 | `testi- / mony` → `testimony` |
| 5424 | `tor- / mented` → `tormented` |
| 5468 | `haughti- / ness` → `haughtiness` |
| 5468 | `covetous- / ness` → `covetousness` |
| 5477 | `suffer- / ings` → `sufferings` |
| 5477 | `suffer- / ings` → `sufferings` |
| 5499 | `command- / ment` → `commandment` |
| 5550 | `accom- / plished` → `accomplished` |
| 5575 | `resur- / rection` → `resurrection` |
| 5591 | `con- / tempt` → `contempt` |
| 5593 | `fore- / told` → `foretold` |
| 5597 | `resur- / rection` → `resurrection` |
| 5597 | `con- / cerning` → `concerning` |
| 5659 | `Scrip- / tures` → `Scriptures` |
| 5706 | `resur- / rection` → `resurrection` |
| 5723 | `trans- / lation` → `translation` |
| 5723 | `para- / phrase` → `paraphrase` |
| 5730 | `Dill- / mann` → `Dillmann` |
| 5763 | `founda- / tions` → `foundations` |
| 5837 | `con- / cerning` → `concerning` |
| 5863 | `command- / ment` → `commandment` |
| 6004 | `awk- / wardly` → `awkwardly` |
| 6004 | `pre- / vious` → `previous` |
| 6051 | `what- / soever` → `whatsoever` |
| 6064 | `reckon- / ing` → `reckoning` |
| 6081 | `reckon- / ing` → `reckoning` |
| 6107 | `Xan- / month` → `Xanmonth` |
| 6237 | `taker- / away` → `takeraway` |
| 6316 | `com- / manded` → `commanded` |
| 6318 | `com- / pleted` → `completed` |
| 6396 | `wicked- / ness` → `wickedness` |
| 6412 | `dark- / ness` → `darkness` |
| 6434 | `righteous- / ness` → `righteousness` |
| 6436 | `vine- / yard` → `vineyard` |
| 6495 | `Pass- / over` → `Passover` |
| 6553 | `inherit- / ance` → `inheritance` |
| 6558 | `more- / over` → `moreover` |
| 6576 | `ordi- / nance` → `ordinance` |
| 6580 | `resur- / rection` → `resurrection` |
| 6624 | `pretend- / ing` → `pretending` |
| 6632 | `con- / cerning` → `concerning` |
| 6654 | `come- / liness` → `comeliness` |
| 6701 | `more- / over` → `moreover` |
| 6756 | `con- / suming` → `consuming` |
| 6767 | `Pente- / intelligible` → `Penteintelligible` |
| 6780 | `trans- / gressed` → `transgressed` |
| 6791 | `trans- / gress` → `transgress` |
| 6825 | `men- / tioned` → `mentioned` |
| 6827 | `appar- / ently` → `apparently` |
| 6888 | `judg- / ment` → `judgment` |
| 7078 | `exceed- / ingly` → `exceedingly` |
| 7107 | `faith- / ful` → `faithful` |
| 7115 | `re- / moved` → `removed` |
| 7129 | `re- / presents` → `represents` |
| 7163 | `command- / ments` → `commandments` |
| 7210 | `them- / selves` → `themselves` |
| 7286 | `under- / stand` → `understand` |
| 7296 | `recon- / ciled` → `reconciled` |
| 7298 | `circum- / cision` → `circumcision` |
| 7318 | `fol- / correct` → `folcorrect` |
| 7417 | `tem- / maker` → `temmaker` |
| 7443 | `com- / manded` → `commanded` |
| 7452 | `Pos- / maker` → `Posmaker` |
| 7483 | `num- / bered` → `numbered` |
| 7532 | `circum- / cision` → `circumcision` |
| 7539 | `unbeliev- / ing` → `unbelieving` |
| 7572 | `trans- / gressors` → `transgressors` |
| 7589 | `un- / yodly` → `unyodly` |
| 7643 | `char- / sentence` → `charsentence` |
| 7643 | `per- / you` → `peryou` |
| 7663 | `any- / thing` → `anything` |
| 7669 | `condemna- / tion` → `condemnation` |
| 7673 | `forgive- / ness` → `forgiveness` |
| 7748 | `righteous- / ness` → `righteousness` |
| 7783 | `there- / forevas` → `thereforevas` |
| 7783 | `upright- / ness` → `uprightness` |
| 7795 | `them- / selves` → `themselves` |
| 7822 | `over- / whelmed` → `overwhelmed` |
| 7839 | `sacri- / fices` → `sacrifices` |
| 7901 | `More- / over` → `Moreover` |
| 7956 | `trans- / lation` → `translation` |
| 7972 | `com- / manded` → `commanded` |
| 7988 | `any- / thing` → `anything` |
| 7990 | `sacri- / fices` → `sacrifices` |
| 8006 | `priest- / text` → `priesttext` |
| 8065 | `suffer- / ings` → `sufferings` |
| 8105 | `sen- / tence` → `sentence` |
| 8105 | `interroga- / tive` → `interrogative` |
| 8105 | `neces- / sary` → `necessary` |
| 8112 | `Any- / thing` → `Anything` |
| 8124 | `quota- / tion` → `quotation` |
| 8138 | `trans- / gressed` → `transgressed` |
| 8145 | `bap- / tized` → `baptized` |
| 8151 | `grati- / tude` → `gratitude` |
| 8181 | `trans- / gression` → `transgression` |
| 8271 | `remem- / brance` → `remembrance` |
| 8274 | `Saddu- / cees` → `Sadducees` |
| 8309 | `cor- / respond` → `correspond` |
| 8439 | `con- / demned` → `condemned` |
| 8499 | `command- / ments` → `commandments` |
| 8543 | `thanks- / giving` → `thanksgiving` |
| 8581 | `pres- / byters` → `presbyters` |
| 8609 | `fol- / would` → `folwould` |
| 8638 | `thanks- / giving` → `thanksgiving` |
| 8666 | `exceed- / ingly` → `exceedingly` |
| 8678 | `trans- / gressed` → `transgressed` |
| 8687 | `com- / passion` → `compassion` |
| 8772 | `false- / hood` → `falsehood` |
| 8794 | `com- / mandments` → `commandments` |
| 8846 | `resurrec- / tion` → `resurrection` |
| 8914 | `ap- / parently` → `apparently` |
| 8925 | `men- / tioned` → `mentioned` |
| 9014 | `man- / kind` → `mankind` |
| 9020 | `under- / stand` → `understand` |
| 9033 | `up- / rightness` → `uprightness` |
| 9036 | `know- / ledge` → `knowledge` |
| 9136 | `trans- / gressed` → `transgressed` |
| 9285 | `com- / prises` → `comprises` |
| 9339 | `Trans- / literated` → `Transliterated` |
| 9349 | `trans- / literation` → `transliteration` |
| 9370 | `Con- / cerning` → `Concerning` |
| 9383 | `trans- / lation` → `translation` |
| 9455 | `Edin- / burgh` → `Edinburgh` |

## Step 3 — blank lines

| File | Runs of 3+ blank lines collapsed to 2 |
|---|---:|
| `80-serata-seyon.md` | 0 |
| `81-teezaz.md` | 0 |
| `82-gessew.md` | 0 |
| `84-mashafa-kidan-1.md` | 0 |
| `86-qalementos.md` | 0 |
| `87-didascalia.md` | 0 |

## Not done in this pass

Footnotes were not moved, translator introductions were not moved, and OCR
misspellings were not corrected. All three are catalogued in
`MANUAL_REVIEW.md` with line numbers.

