# The Final Decision

A science-fiction trilogy about a family, a search, and competing answers to survival.

**Current baseline: Book I, Paradise — v7 working text.** The manuscript has 17 chapters and 15,558 chapter-body words. Books II and III have outlines and pilot passages, not complete manuscripts. V7 has no rendered reading PDF. The existing frontispiece still needs its recorded correction before a new illustrated edition.

## Writing files

- [Read or edit Book I](book-one/paradise.md).
- [Series bible and Book II/III pilots](reference/bible.md).
- [Characters](reference/characters.md) and [Books I/II synopsis](reference/synopsis.md).
- [Current decisions and labelled proposals](development/decisions.md).
- [Open work and implementation status](development/open-items.md).
- [Philosophy, selected wording, and proposed scenes](development/philosophy.md).
- [Original artwork](art/laniakea-tree.png) and [production instructions](production/README.md).

The manuscript governs the present Book I text. Explicit latest author decisions govern future work; proposed scenes and private explanations remain labelled as proposals. Updating a reference does not silently rewrite the prose. Historical documents can contain superseded positions.

## History instead of duplicate files

Keep one current file per purpose. Commit a small coherent change and push it before starting the next commit. Do not create dated backup files, version-numbered manuscripts, archive folders, or tracked ZIP/PDF exports. Generated work belongs in ignored `build/` output.

The supplied ZIP has been reconstructed as forward commits on the existing history. All **288 distinct non-cache source contents**, covering **291 ZIP entries**, are preserved exactly; the single generated Python cache was excluded. The final working tree has 14 files. The v7 manuscript and original artwork remain byte-for-byte unchanged.

The [preservation ledger](https://github.com/Calix17/Trilogy/blob/94d7cd121a037537faf49cf011e35e2e2e5d84ce/migration/preservation-ledger.csv) maps every original ZIP path and hash to a commit and historical path. It lives in Git history, not in the current writing folder. Recover old PDFs, alternate exports, notes, reviews, and workshop material through that ledger.

| Tag | What it preserves |
| --- | --- |
| `migration-start` | Original repository and combined `series.md`. |
| `book-one-v1` through `book-one-v6` | Exact recovered manuscript and its main packaged reading PDF at each checkpoint. |
| `book-one-v7-working` | Exact v7 working manuscript import. |
| `zip-history-preserved` | Verified original-source coverage before consolidation and cleanup. |
| `v7-clean` | Completed v7 migration with only current files. |

The earlier checkpoints are reconstructed from surviving sources; their companion files are partial states, not certified original project releases. Commit dates are import dates. Distinct recovered variants and uncertain source chronology are explicitly identified in commit messages.

```sh
git log --follow -- book-one/paradise.md
git show book-one-v1:book-one/paradise.md
git show book-one-v6:book-one/paradise.md
git show migration-start:series.md
```

To retrieve binary PDFs or exact original bytes safely on Windows, use `git archive` for the chosen commit/path rather than text-mode shell redirection. For example, `git archive --format=zip --output=../book-one-v6-export.zip book-one-v6 book-one/paradise.pdf`. For a variant or intermediate note, use the commit/path from the ledger.

## Verification boundary and future work

The migration checks preservation, source hashes, task/status coverage, current links, the live-file list, and remote commits. **No PDF rendering, art inspection, plot-hole review, or other editorial assessment was performed for this migration.** The `v7-clean` tag is the boundary.

For subsequent work after that boundary, add the planned verification entry point and current review record at stable paths. Before pushing, render a fresh review PDF, compare its text to the source, inspect layout/art, and review affected project rules, chronology, causality, character knowledge and development, rhythm, story arcs, symbols, chapter endings, artistic coherence, and reader risks. Establish a full current-manuscript assessment in that later phase. Track unanswered questions as answered, intentionally open, deferred, privately undecided, or accidentally dropped. Give significant findings evidence, confidence, reader impact, and a proportionate mitigation.

Details should serve the storytelling. Quiet endings, deliberate ambiguity, uneven emphasis, and asymmetric arcs are allowed. Do not require every character to transform or every chapter to end on a cliffhanger. Do not invent audience-success probabilities. New technical or material continuity failures block a post-v7 push; intentional ambiguity and existing development risks receive explicit dispositions. Proposed changes to selected outcomes or mystery boundaries remain author decisions. Keep one backlog in [open items](development/open-items.md); preserve previous assessments in commits.
