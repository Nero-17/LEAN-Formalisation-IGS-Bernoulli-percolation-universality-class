# Building and checking the unified development

Requirements: Lean/Elan, Python 3.11 or later, Git, adequate disk and RAM for the
large exact certificate computations. Lean and mathlib are pinned by the repository.

## Restore generated literal data

The 44 large `Section5MassChunkData*.lean` files are deterministic data, not omitted
proofs. Their total size is 453,477,561 bytes. All proof files are tracked. Restore:

```sh
python scripts/restore_section5_chunk_data.py --output-dir ../restored-data
```

The destination must be empty. Copy its `Universality/Certificates/*.lean` files
into this repository's `Universality/Certificates/`. The restoration script verifies
every source JSON and all generated hashes. `GENERATED_DATA.json` gives an additional
root-relative manifest. Keep the reconstructed data out of Git.

## Fresh source build

```sh
lake update
lake exe cache get
lake env python scripts/build.py
```

The driver compiles the complete project import closure in dependency order,
then executes `Audit.lean`. This can be expensive: the large integer certificates
are checked using Lean reduction. It writes local logs and an incremental manifest
under ignored `logs/` and `.lake/` directories. No precompiled project objects are
distributed or required for a fresh build.

After a successful local build, `--incremental` reuses unchanged objects but always
reruns the final audit. `--check-only` verifies the local integrity manifest without
claiming a new compilation. Set `--lean /path/to/lean` and `LEAN_PATH` explicitly
when using an existing pinned dependency cache instead of Lake's environment.

## Published integration evidence

The integrated entry and project-wide audit were run in the pinned Windows Lean
environment. Existing dependency objects were reused only after comparing source,
object and recursive project dependencies against the completed section snapshots.
Allowed source-only differences were CRLF normalization, trailing blank lines,
diagnostic `#print axioms` commands, and one reviewed prose change in a module comment.
No mathematical declaration or proof body was replaced by this equivalence check.

`verification.json` records the final counts, hashes and explicit verification scope.
`axioms.json` records each imported kernel declaration and its actual dependencies.
`source-manifest.json` binds the released import closure to exact source and object
hashes. These are final verification artifacts, not accumulated execution histories.
This verification is not represented as an all-modules fresh source rebuild or a
tested clean-machine Lake installation.
