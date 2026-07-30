# Sources

Complete bibliographic references for all texts used in this project.

## 1. Public Domain Sources (pre-1930)

### Biblical Translations

| Source | Content | Date | Language | Access |
|--------|---------|------|----------|--------|
| American Standard Version (ASV) | OT & NT protocanonical (39 + 27 books) | 1901 | English | [Wikisource](https://en.wikisource.org/wiki/Bible_(American_Standard)) |
| L.C.L. Brenton, Septuagint Translation | Deuterocanonical books (Tobit, Judith, Wisdom, Sirach, Baruch, 1 Esdras) | 1851 | English | [Wikisource](https://en.wikisource.org/wiki/Brenton_Septuagint) |

### Ethiopian-Specific Texts

| Source | Content | Date | Language | Access |
|--------|---------|------|----------|--------|
| R.H. Charles, *The Book of Enoch* | 1 Enoch (108 chapters) | 1917 | English | [Sacred Texts](https://sacred-texts.com/bib/boe/index.htm) |
| R.H. Charles, *The Book of Jubilees* | Jubilees (50 chapters) | 1902 (Oesterley & Box 1917 reprint) | English | [Global Grey](https://www.globalgreyebooks.com/online-ebooks/r-h-charles_book-of-jubilees_complete-text.html) |
| R.H. Charles (ed.), *Apocrypha and Pseudepigrapha of the OT* (APOT), vol. 2 | 4 Ezra, 4 Baruch, and others | 1913 | English | [Archive.org](https://archive.org/details/apocryphaandpseu02charuoft) |
| François Martin, *Le Livre d'Hénoch* | 1 Enoch (French from Ge'ez) | 1906 | French | [Wikisource FR](https://fr.wikisource.org/wiki/Livre_d%E2%80%99H%C3%A9noch_(%C3%A9thiopien)/Livre_d%E2%80%99H%C3%A9noch) |

### Broader Canon Sources

| Source | Content | Date | Language | Access |
|--------|---------|------|----------|--------|
| G. Horner, *The Statutes of the Apostles* | Ser'ata Seyon, Te'ezaz (Sinodos parts 1-2) | 1904 | English | Archive.org |
| G.H. Schodde, *The Apostolic Canons* | Gessew (Sinodos part 3) | 1883 | English | Archive.org |
| James Cooper & A.J. Maclean | Mashafa Kidan I (Testamentum Domini) | 1902 | English | Archive.org |
| M.R. James | Mashafa Kidan II (Epistula Apostolorum) | 1924 | English | Archive.org |
| S. Grébaut, *Revue de l'Orient Chrétien* vol. 16-18 | Qalementos (French) | 1911-1913 | French | Gallica / Archive.org |
| J.M. Harden, *The Ethiopic Didascalia* | Didascalia (43 chapters) | 1920 | English | Google Books |

### ⚠️ Scraping warning: sacred-texts.com index pages are NOT text

**Do NOT use a sacred-texts.com `index.htm` page as a text source.** These pages
are tables of contents. For Charles's *Jubilees* the index page lists only his
per-chapter *summaries* (~46 words per chapter); the text itself lives on the
separate per-chapter pages. Scraping the index yielded a 2,311-word file that
looked plausible — 50 chapter headings, continuous prose — but contained none of
the actual book. Jubilees is now taken from the Global Grey transcription above,
which carries the whole text in one page. The same trap applies to
`https://sacred-texts.com/bib/boe/index.htm` for 1 Enoch: verify any
sacred-texts extraction against a known chapter's word count before trusting it.

## 2. Modern Academic Sources

| Source | Content | Date | Notes |
|--------|---------|------|-------|
| Daniel Flusser, *Sefer Yosippon* (critical edition) | Josippon | 1978-1980 | Hebrew critical edition |
| R.W. Cowley, "The Biblical Canon of the Ethiopian Orthodox Church Today" | Canon reference | 1974 | *Ostkirchliche Studien* 23 |
| D. Labadie, "Genèse du canon biblique éthiopien" | Canon history | 2024 | *Médiévales* 87 |

## 3. Paid Editions (post-2000)

| Source | Content | Date | Price | Notes |
|--------|---------|------|-------|-------|
| D.P. Curtin & Bekele Tesfaye, *1st Ethiopian Maccabees* | 1 Meqabyan | 2018 | ~$15 | Dalcassian Press. Ch.1 free on Wikisource EN |
| D.P. Curtin, *2nd Ethiopian Maccabees* | 2 Meqabyan | 2023 | ~$15 | Dalcassian Press |
| D.P. Curtin / Feqade Selassie | 3 Meqabyan | 2008/2023 | ~$15 | Multiple editions |
| Breandan Lumpkin | Qalementos (English) | 2024 | ~$25 | First modern English translation |
| Michael Mikhail | Sinodos, Dominos | 2025 | Paid | Includes Abtelis partial |

## 4. Reference Websites

- **Ethiopian Orthodox Bible Project**: https://ethiopianorthodoxbible.wordpress.com/
- **EOTC Official Canon**: https://www.ethiopianorthodox.org/english/canonical/books.html
- **Sacred Texts**: https://sacred-texts.com/ — ⚠️ never scrape an `index.htm` page as text; see the scraping warning above
- **Archive.org**: https://archive.org/
- **Wikisource EN**: https://en.wikisource.org/
- **Wikisource FR**: https://fr.wikisource.org/
