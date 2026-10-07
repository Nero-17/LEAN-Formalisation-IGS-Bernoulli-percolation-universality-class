# Section 5 streaming evaluator: static performance review

Checked on 2026-10-07 by the graph agent while the production 661/739 checks continued. This is a read-only source and literal-data inspection, not a Lean benchmark, a replacement evaluator, or a numerical certificate. No production Lean file, generator, or running queue was changed. The parent supplied the observed late-block duration of approximately 213 seconds per 16 levels; this review does not independently attribute that duration to one operation.

The relevant definitions are `advanceLexState` and `advanceLexStates` in `Universality/Certificates/Section5MatrixStream.lean:57`, the bit extractors in `Section5BitExtraction.lean:6`, and `LexMassCheckpoint.step` / `runLexMassChunk` in `Section5MassChunks.lean:16`. The production proof at `Section5MassChunkProofBase66108.lean:11` checks the complete 16-step checkpoint equality using `decide +kernel`.

## What the source establishes

Positive remainders never become zero in `advanceLexState`: the first branch retains the remainder, and the second is taken only when the remainder is strictly greater than the subtracted first-block count. Zero remainders remain unchanged. Consequently all initially active states continue to receive matrix updates throughout the entire stream, even after their suffix choices become deterministic. `advanceLexStates` also retains every inactive state and its original list position.

For an active state with `remainingZeros = 0`, the first count is zero, the contribution is zero, and every later step multiplies its accumulated matrix on the right by the central kernel. At depth zero it contributes that matrix applied to `(3139,1313)`. The current implementation has no early finalization or merging of these states.

A short read-only Python parser inspected the existing Base661 checkpoint literals, counting state rows and their leading zero/remainder fields without executing the evaluator. There are 937 rows and 813 positive remainders at every inspected checkpoint. These are literal-data observations, not an additional kernel proof.

| Levels completed | Active states with zero remaining zeroes | Active states with positive remaining zeroes | Distinct positive remaining-zero values | Largest prefix literal, bits |
|---:|---:|---:|---:|---:|
| 0 | 0 | 813 | 813 | 1 |
| 128 | 29 | 784 | 553 | 627 |
| 256 | 89 | 724 | 475 | 1253 |
| 384 | 153 | 660 | 380 | 1879 |
| 512 | 211 | 602 | 285 | 2505 |
| 640 | 272 | 541 | 194 | 3131 |
| 768 | 326 | 487 | 103 | 3758 |
| 936 | 813 | 0 | 0 | — |

No prefix uses split-limb syntax through the inspected level 768. At level 896, 194 prefixes do use it. In particular, a claimed 4096-bit representation boundary near level 512 would be false. The packed source lines become shorter as depth decreases, whereas all 813 accumulated matrices grow; the latter supplies a concrete growing component of the per-step work. This does not prove that it dominates the measured kernel time.

## Candidates for a separately proved future evaluator

1. **Merge active zero-zero states by adding their accumulated matrices entrywise.** They all have the same future central-kernel suffix. Right multiplication and final vector action distribute over matrix addition, so a merged state with zero remaining zeroes and positive remainder has exactly the sum of their future contributions. This preserves every original matrix order: it factors a common right suffix and does not commute kernels. The proof can be made at the existing checkpoint `value` boundary. At level 512 the observed 211 such states would become one; at level 768, 326 would become one. Alternatively, settle these states immediately using the appropriate power of the central kernel. Neither optimization has been implemented, proved in Lean, or benchmarked here.
2. **Share coefficient extraction among equal remaining-zero values.** At level 512, the 602 positive-zero states request counts from only 285 indices; at level 768, 487 states use only 103 indices. The current function interface evaluates the lookup separately for each state. Grouping or a proved lookup table could reduce repeated work. A naive list-indexed cache could itself add traversal cost, so no speedup is claimed. More general merging of equal `(remainingZeros,remainder)` states follows the same matrix-linearity argument but requires an additional grouping implementation.

The complete checkpoint equality fixes the entire state list, so either state-merging variant changes the checkpoint witnesses and requires new generic correctness proofs and new future data. It must not be inserted into the running production chain. The existing chunks' compositional value theorem supplies a possible future integration boundary; it does not validate an unproved replacement.

There is also a possible normalization-sharing question because both projections of `advanceLexStates` are used in each checkpoint, and both projections of recursive pairs are consumed by the list recursion. Source inspection alone cannot tell whether the kernel cache duplicates substantial work here. No causal claim or rewrite recommendation is based on that possibility.

The official Lean 4.32.1 kernel has fast reductions for the natural-number division, remainder, shifts, and bitwise mask operations used here, as verified separately by the parent. Their logical recursive definitions are therefore not an explanation for this slowdown. The previously measured whole-structure Boolean comparison did not improve performance, and this review does not recommend repeating it. All optimization candidates remain unmeasured; the production checks continue unchanged.
