# PDF production

The editable source is [Book I: Paradise](../book-one/paradise.md), v7 working text. An internal review proof has been rendered and verified after the migration. The original [frontispiece](../art/laniakea-tree.png) still has the recorded spoiler-bearing labels; V7-08 in [open items](../development/open-items.md) tracks its correction before an approved illustrated reading edition.

The single renderer is the preserved v6 implementation with current input, output, and artwork paths. It retains the six-by-nine-inch design, embedded STIXGeneral (DejaVu fallback), 11-point body type, bookmarks, running headers, and numbered body pages. Only the paths were changed during migration. The post-v7 review has now verified runtime execution, fonts, pagination and chapter-text fidelity; see [the evidence](../development/verification.md#production-evidence-and-disposition).

After the completed migration, from the project root:

```sh
python -m pip install -r production/requirements.txt
python production/render-book.py
```

Default outputs are `build/paradise-v7-working.pdf` and its `.qa.json` report. They are ignored by Git. The renderer also accepts `--source`, `--output`, `--frontispiece`, and `--qa`. Do not reuse v6 chapter-tightening settings without inspecting the v7 result. The dependencies are declared, not presented as a tested or locked environment.

The inspected v7 proof uses `python production/render-book.py --compact-chapters 5,6,12,13,14`: 56 pages, no blank body pages or flagged sparse chapter endings, and all 17 chapter texts matching the source under the renderer's documented normalization. Review these spacing choices again after any prose or artwork change. This run used the bundled Python runtime and matplotlib 3.11.2 installed in ignored `build/review-deps`; set `PYTHONPATH` to that directory for this local setup, or install the declared requirements in a normal project environment. One-off checking code, JSON evidence and page images are ignored review output; the reusable verification entry point remains future tooling work.

For post-v7 changes, render before pushing; compare extracted text against the exact source and inspect layout and art for clipping, missing text, bad pagination, and spoilers. Apply the post-v7 review policy in [README](../README.md). A successful render is not editorial acceptance or a claim of publication readiness. Historical PDFs are recoverable from Git rather than retained beside the current manuscript.
