# Exact restoration of generated data

The Drive connector limits one upload to 100 MiB. This single archive retains
the complete research report, every original certificate JSON, all proof
sources, all generators, compilation records, and source manifests. The 44
large pure-data checkpoint modules are stored as a deterministic reconstruction
recipe. Their exact restoration has been executed and every byte hash checked;
see code/docs/section5-chunk-data-restoration.json and GENERATED_DATA.json.
The live local workspace retains the full ready-to-build generated sources.

For this GitHub branch, run the following from the repository root. For the
original Drive archive, run them from its extracted `code` directory:

```powershell
python scripts/restore_section5_chunk_data.py --output-dir ../restored-data
Get-ChildItem -LiteralPath ../restored-data/Universality/Certificates -File | Copy-Item -Destination ./Universality/Certificates
```

The first command refuses to overwrite a nonempty output directory and verifies
all 44 expected hashes before reporting success. The copy command is intended
only for this freshly extracted source tree, where those files are absent.
It completes the original source layout without changing any proof statement.
Run the archived Lean checks afterwards. Reconstruction is not a Lean proof.

All remaining archived files are covered by SHA256.json. GENERATED_DATA.json
lists the reconstructed file hashes and byte counts separately.
