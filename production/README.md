# PDF production

The editable source is [Book I: Paradise](../book-one/paradise.md), v7 working text. No v7 reading PDF has been rendered or verified. The original [frontispiece](../art/laniakea-tree.png) still has the recorded spoiler-bearing labels; V7-08 in [open items](../development/open-items.md) tracks its correction.

The single renderer is the preserved v6 implementation with current input, output, and artwork paths. It retains the six-by-nine-inch design, embedded STIXGeneral (DejaVu fallback), 11-point body type, bookmarks, running headers, and numbered body pages. Only the paths were changed during migration. Runtime compatibility, dependency installation, fonts, pagination, and PDF fidelity have not been tested for v7.

After the completed migration, from the project root:

```sh
python -m pip install -r production/requirements.txt
python production/render-book.py
```

Default outputs are `build/paradise-v7-working.pdf` and its `.qa.json` report. They are ignored by Git. The renderer also accepts `--source`, `--output`, `--frontispiece`, and `--qa`. Do not reuse v6 chapter-tightening settings without inspecting the v7 result. The dependencies are declared, not presented as a tested or locked environment.

For post-v7 changes, render before pushing; compare extracted text against the exact source and inspect layout and art for clipping, missing text, bad pagination, and spoilers. Apply the post-v7 review policy in [README](../README.md). A successful render is not editorial acceptance or a claim of publication readiness. Historical PDFs are recoverable from Git rather than retained beside the current manuscript.
