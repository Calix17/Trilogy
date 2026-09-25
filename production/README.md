# V4 reading edition

The active source is `../02-book-one/book-one-paradise-v4.md`. The adjacent PDF
is the reading edition: 17 chapters, 21,296 chapter-body words, 80 PDF pages.
The title/frontispiece is unnumbered; the narrative begins on printed page 1.

## Render

Requires Python 3.10 or later with `reportlab`, `Pillow`, and `pypdf`. Install
`matplotlib` for the bundled STIXGeneral fonts, or provide a complete DejaVu Serif
font family in the usual system font directory. No network access is used by
the renderer.

From the project root:

```bash
python3 08-production/render-book.py --tighten-chapters 13 --compact-chapters 5,15 --qa /tmp/paradise-v4-render-qa.json
```

The source and output default to the v4 files in `02-book-one/`. Use `--source`,
`--output`, and `--frontispiece` to specify alternatives. The default artwork is the
unchanged `05-art/laniakea-tree.png`. The renderer preserves emphasis and
normalizes Unicode dash characters to spaced or ordinary ASCII hyphens for the
PDF only. This does not change the Markdown source.

## Edition settings

- 6 × 9 inches; embedded STIXGeneral serif family.
- Body type: 11 pt, normally 14.8 pt leading.
- Chapter 13: 14.4 pt leading.
- Chapters 5 and 15: compact paragraph and heading spacing, 14.2 pt leading.
- Seventeen chapter bookmarks, running headers, and continuous page numbers.
- Existing frontispiece and visible v4 edition label.

The chapter-specific spacing prevents very short trailing pages without
cutting prose. Future text changes require another pagination and visual check.
The generated QA JSON includes extracted page text and is a working diagnostic;
the compact `v4-validation.json` records the checks for this delivered edition.

## Checks completed

All 80 pages were inspected in contact sheets, with full-size checks of the
cover and representative body/adjusted pages. No visible clipping, overlaps,
blank body pages, or very sparse chapter endings were found. An independent
comparison verified all 17 chapter bodies against extracted PDF text, in order,
using both word tokens and every non-whitespace character after the renderer's
punctuation normalization and Markdown emphasis removal.

Every manuscript and PDF supplied in the source project remains byte-for-byte
unchanged. Modified reference documents have exact prior copies under
`99-archive/pre-v4-reference/`. Screen materials and the original artwork have
not been rewritten. The new v4 archive contains the whole project.
