# Independent review of signed repair chunks

Graph-agent review on 2026-10-07. This review inspected the generic bridge, generator, generated Lean sources, manifests, and existing input literals. It did not run Lean or the generator and did not change production data. The generic bridge had an author-reported successful source compilation; the concrete numerical checks were being run separately by the certificate agent.

## Generic proof boundary

`Universality/Certificates/Section5MassRepairChunks.lean` retains the exact obligations needed for `massEvaluationWithInitial_of_chunks`:

- `parts : chunks.flatten = packets` identifies the complete ordered list, including repetitions and zero or negative coefficients.
- `checked : List.Forall₂ (fun chunk value => correctionsMassEvaluation chunk = value) chunks values` supplies one actual equality for every chunk and requires the two lists to have the same length.
- `baseline_checked` independently proves `baselineMassEvaluation depth = baseline`.
- `total_checked` includes that baseline, both original natural initial-value coordinates cast to integers, and the integer sum of every checked chunk value. Its conclusion uses the supplied original target.

The proof unfolds the original `massEvaluationWithInitial`, substitutes the exact flattening and checked chunk sum, and applies the independent baseline and total equalities. The append/flatten lemmas only reassociate integer pair addition. They do not commute matrix words, modify packet coefficients, truncate a zip, or replace an integer sum by a natural sum. The resulting theorem is the original evaluator equality, not a new approximate or filtered quantity.

This repair equality still does not establish the initial stream value. The existing `mass_certificate_at` assembly separately requires the actual `initialMassEvaluation` theorem, in addition to allocation capacity and this repair equality.

## Generator and actual emitted sources

`scripts/section5_certificate_repair_chunks.py` reads every repair layer and all four coefficients in the original `(false,false), (true,false), (true,true), (false,true)` order. It appends all packets without sign or zero filtering, then takes consecutive Python slices of size 32. Its packet formula matches the original evaluator: apply the repeated tail, then the first letter, then the signed coefficient times `18^layer` and the unchanged commutator action. The separate baseline retains the factor 16. Python's target assertion proposes witnesses; it is not used as a Lean proof.

The independent literal/source inspection found:

| Seed | Original packets | Negative coefficients | Zero coefficients | Positive coefficients | Chunk lengths |
|---|---:|---:|---:|---:|---|
| 661 | 936 | 220 | 221 | 495 | 29 × 32, then 8 |
| 739 | 952 | 245 | 243 | 464 | 29 × 32, then 24 |

For each seed, concatenating the emitted packet tuples equals the tuples in the actual existing `Section5InputBase*.lean` source, in exactly the same order. Both `chunks` and `values` name indices 00 through 29 once. All thirty `checked00` through `checked29` declarations assert `correctionsMassEvaluation packetsNN = valueNN` with `decide +kernel`; the final `List.Forall₂.cons` chain includes each once in the same order. The final assembly imports all eight proof modules and the separate checks module.

The generated `Checks` module separately requires kernel proofs for the exact `flatten` equality, baseline, and final target. The final `allocationBase661_massRepairLiteral` and `allocationBase739_massRepairLiteral` statements are unchanged: their targets are respectively `massCertificateValue 936 661` and `massCertificateValue 952 739`. That definition is exactly `16^(depth+1) * base^219` times `(55,23)` over the integers. The new initial-value literals equal both the original JSON values and the existing stream endpoint source literals exactly.

Every generated module hash matched its manifest, and the generator/source-input hashes matched the recorded provenance. A source scan found no proof placeholders, new axioms, or unsafe/native evaluation shortcuts. Exact observed hashes, coverage, coefficient counts, and source checks are in `docs/section5-mass-repair-chunk-static-observations.json`. These are static observations and do not replace the outstanding Lean numerical equalities.

## Status and integration boundary

No mathematical or semantic discrepancy was found in the reviewed chunk construction. At this checkpoint, the existing `Section5MassBase661.lean` and `Section5MassBase739.lean` still contained the earlier monolithic `massRepairEvaluation` check. The certificate agent was notified that final wiring must use the new proved literal equality and identify the equal initial literals, while retaining the independent stream theorem. The review does not claim that this final wiring or all thirty concrete chunk checks have already compiled.
