# Book I reading editions

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
