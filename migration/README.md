# Source preservation verification

All 292 supplied ZIP entries are accounted for: 291 non-cache entries represent 288 distinct file contents, all byte-verified against reachable pushed Git blobs. One generated Python cache is excluded. The original master document was already present at migration-start.

The ledger maps original ZIP paths and SHA-256 hashes to an actual commit and logical path. Recover with `git show COMMIT:PATH`. Source chronology is reconstructed; individual historical snapshots may be incomplete. The ledger is retained in this commit and can be removed from the final working tree.

No PDF was rendered and no editorial review was run.
