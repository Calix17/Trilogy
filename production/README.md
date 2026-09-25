# Book I reading editions

## V7 — working text

Source: `../02-book-one/book-one-paradise-v7-working.md`. Seventeen chapters; 15,558 chapter-body words using the same counting method as v6. No v7 PDF or new artwork has been generated. `v6-to-v7-working.diff` records all manuscript edits; `v7-working-validation.json` records preservation and targeted continuity checks. The original frontispiece still needs its revealing labels revised before a new illustrated edition.

## V6 — previous rendered edition

Source: `../02-book-one/book-one-paradise-v6.md`. Reading PDF: the adjacent `.pdf`. Seventeen chapters; 15,905 chapter-body words; 58 PDF pages including the original frontispiece. The first narrative page is printed page 1.

From the project root:

```bash
python3 08-production/render-book-v6.py --compact-chapters 5,12,14 --qa /tmp/paradise-v6-render-qa.json
```

The six-by-nine-inch design uses embedded STIXGeneral at 11 pt. Normal leading is 14.8 pt; chapters 5, 12, and 14 use the existing compact style at 14.2 pt with reduced paragraph and heading spacing to remove sparse spillovers. No prose is discarded. The original frontispiece, chapter bookmarks, running headers, and numbered narrative pages are retained.

All 58 pages were inspected in contact sheets, with enlarged checks of the cold room, Haven’s account, Daniel’s gift, the final decision, and the homecoming. Extracted chapter text matches the Markdown after punctuation and whitespace normalization. No blank body pages, sparse endings below the renderer’s threshold, off-page text, clipping, or overlap were found. `v6-validation.json` records source/PDF hashes, per-chapter comparisons, archive checks, and preservation of the two Book II reference sections.

The earlier renderer instructions below remain valid for their own editions. A future text change requires a fresh render and check.

---

## V5

Source: `../02-book-one/book-one-paradise-v5.md`. Reading PDF: the adjacent `.pdf`.
Seventeen chapters; 13,592 chapter-body words; 50 PDF pages including the frontispiece.
The first narrative page is printed page 1.

From the project root:

```bash
python3 08-production/render-book-v5.py --tighten-chapters 5,13 --compact-chapters 15,16 --qa /tmp/paradise-v5-render-qa.json
```

Requires Python 3.10+, ReportLab, Pillow, and pypdf. STIXGeneral is discovered through
matplotlib’s bundled fonts; DejaVu Serif is a fallback. No network is used. The source,
output, and frontispiece have project-relative defaults. Use `--source`, `--output`, and
`--frontispiece` for alternatives.

The reading page is 6 × 9 inches. Body text is embedded STIXGeneral, 11 pt, normally
14.8 pt leading. Chapters 5 and 13 use 14.4 pt leading. Chapters 15 and 16 use 14.2 pt
leading with compact paragraph/heading spacing to prevent very short spillover pages.
No prose is removed by the renderer. Dashes are normalized in the PDF only; emphasis
is preserved. Chapter bookmarks, running headers, and continuous page numbers are included.

All 50 pages were inspected in contact sheets, with full-size inspection of the final
three pages. No clipping, overlapping type, blank body pages, or very sparse chapter
endings were found. Each chapter’s extracted PDF text was compared to the Markdown
with emphasis removed and the renderer’s punctuation normalization applied. Every
non-whitespace character matched in order. `v5-validation.json` records these checks.

The previous manuscripts/PDFs are unchanged. Exact prior supporting documents are
under `99-archive/pre-v5-reference/`. The Book II bible outline is unchanged. The Book
III Window and universal new-body assumptions are explicitly marked for revision in
the current bible; no new Sami visit has been invented.

## Earlier editions

`render-book.py` retains the v4 defaults. Its v4 settings and verification record are
preserved in the pre-v5 production README and `v4-validation.json`. Use that version’s
command when reproducing v4. Future prose changes require another pagination and
visual check; the v5 page and word counts apply only to this delivered draft.
