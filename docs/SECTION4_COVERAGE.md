# Section 4: independent formalisation and exact coverage

Current round: R078, 2026-10-06. The target is the manuscript section
“The six exponentials theorem and common scales”; labels are authoritative
because numbering may change. Baseline: `de5c6e9c2d6f025665f20a5ee2c54ba373f28741`.
Branch: `codex/section4-independent`. Lean 4.32.1; mathlib
`520045ab14e26149ee970e2e617ca04b09bde5d6`.

**All Section 4 finite-rule arithmetic obligations have compiled proofs.** Final closure verification passed for 289 modules, with 3046 project kernel declarations checked against the authorized axiom list. This table distinguishes completed graph
statements from conditional intermediate lemmas and remaining obligations.
The single complete R078 report is [here](R078_完整研究记录.md).

## Authorized external theorems

The user explicitly accepts six exponentials and Gelfond–Schneider as known
external results. Their only declarations are
`Universality.External.six_exponentials` and
`Universality.External.gelfond_schneider_real`. Exact formulations occur in
`SixExponentials.lean` and `GelfondSchneider.lean`; axiom audits expose each use.
No other mathematical axioms or admitted proofs are allowed. These two
accepted dependencies are not unfinished proof obligations.

## Statement map

| Manuscript item | Verified implementation | Status and exact boundary |
| --- | --- | --- |
| `conj:scale-commensurability` | No theorem or axiom asserted | The opening unconditional conjecture is outside this proof obligation list; Section 5 counterexample constructions are also outside this round. |
| `thm:six-exponentials` | `SixExponentials`, `SixExponentialsReal` | Authorized external complex theorem; real specialization proved. |
| `lem:algebraicity` | `GraphAlgebraicHelpers`, `GraphAlgebraicity` | Actual fixed point, derivative, mass entries and spectrum/spectral radius proved algebraic. |
| `def:commensurate` | `Commensurability`, `CommonPrimitiveBase` | Rational-log equivalence and common primitive integer base for arbitrary nonempty families. |
| `thm:dimension-rank`, `prop:arithmetic-alternatives` | `DimensionRank`, `ScaleLogRank`, `GraphDimensionRank` | Actual graph rank ≥3 implies commensurability; contraposition gives rank ≤2; a common irrational dimension bounds the cardinal rank of all scale logs by2, including infinite families. |
| `ex:wheatstone-arithmetic` | `WheatstoneArithmetic`, `GraphWheatstoneArithmetic` | Exact integer valuations at2,5,13; actual ambient/pivotal dimension independence; every classical partner has scale2^k. |
| `prop:iterated-response`, `lem:aligned-class` | `ScaleBlocking`, `GraphIteration` | Actual positive iterations, fixed-point equivalence, edge/scale/derivative/matrix/spectral-radius powers, dimension invariance and aligned response equivalence. |
| `lem:fixed-point-polynomial-structure`: integer quotient and endpoints | `GraphFixedPointPolynomial` | Complete quotient from actual configuration sum, integer coefficients, primitive, F(0)=−1, F(1)=1, critical root. |
| Same lemma: precise degree | `FixedPointCoefficientPositive`, `GraphFixedPointDegree` | Complete actual Classical theorem: deg(phi)=number of edges and deg(F)=edges−2. The signed top coefficient is strictly nonzero by proved deletion/contraction induction; no beta-invariant axiom or nonvanishing premise. |
| Same lemma: reduction at every prime | `GraphFixedPointCoefficients` | Complete: actual coefficient identities plus the graph involution prove all-prime nonconstancy. `GraphFixedPointParity` and `GraphFixedPointStructure` discharge every parity premise. |
| `thm:irreducible-commensurability`: local arithmetic | `IrreducibleHensel`, `IrreducibleValuations`, `IrreducibleThermal`, `IrreducibleGraphThermal` | Nonmonic Hensel, Witt lifts, integer valuations and perfect-power conclusion are proved. `IrreducibleCommensurability` discharges mod2 nonconstancy and supplies the final actual no-integer-power theorem. |
| Same theorem: integer multiplier contradiction | `IntegerMultiplierObstruction` | New coefficient recurrence excludes every integer multiplier>1. This replaces the original residue argument. Exact graph degree is proved separately in GraphFixedPointDegree. |
| Same theorem: mass conjugation and logarithmic independence | `IrreducibleConjugation`, `IrreducibleMass`, `LogarithmicIndependence` | Complete actual graph criterion in `IrreducibleCommensurability`: nonsplit mass powers, three independent dimensions, pair commensurability and common primitive base for arbitrary families. No extra reduction/degree/lifting premise. |
| Pivotal dimension transcendence | `NoIntegerPower`, `GelfondSchneider` | Complete actual classical-graph specialization under full-quotient irreducibility in `IrreducibleCommensurability`; uses only authorized GS beyond foundational axioms. |
| Closing rational pivotal dimension obstruction | `RationalPivotalObstruction` | Complete actual Classical corollary: rational pivotal dimension forces the complete quotient to fail irreducibility. Only foundational axioms; no GS or mass premise. |
| `cor:diamond-commensurability`, `ex:diamond-irreducibility` | `DiamondArithmetic` | Complete: actual mass nonsplitting via norm209, actual pivotal transcendence, actual quotient X²+X−1 irreducible, and whole-class scale2^k in `GraphDiamondArithmetic`. |

## Independence from Section 3

The actual three critical growth dimensions are tied to established finite
graph growth limits in `GraphCriticalDimensions`. Section 3's physical
exponent existence and exponent/dimension equivalence are being developed in
a separate checkout. None of its newer uncommitted results are imported here.
The physical-class translation must use that eventual theorem; it is not
assumed or disguised as a definition in this branch.

## Verification

`Universality.Arithmetic.Section4` is the standalone public import. `Section4Audit.lean` imports the completed independent arithmetic chain and
prints principal axiom dependencies. `scripts/check-section4.ps1` builds its
project dependency closure, checks source and object hashes recursively,
binds reuse to the actual compiler binary, toolchain/manifest and clean pinned package revisions, rechecks all source/object hashes at the end, always reruns the all-project kernel-declaration axiom audit, and saves logs and a manifest separately
from Section 3's build records. Passing targeted checks is not represented as
a completed clean-environment `lake build`.

The historical feasibility probe has been superseded by these implementations.
In particular, the old recommendation to reprove the two external
transcendence theorems is withdrawn under the user's explicit authorization.

The final run completed at 2026-10-06 15:56:57 UTC: 289 modules verified, 28 rebuilt in this pass and 261 reused only after recursive source/object/environment checks. The immediately preceding full pass verified 262 modules and rebuilt 197. The final root always reruns the kernel audit; it checked 3046 declarations from 287 imported project modules. See "docs/section4-build-metadata.json" and the recorded same-session environment migration. The checked command is the direct Lean PowerShell build, not a fresh-environment Lake build.
