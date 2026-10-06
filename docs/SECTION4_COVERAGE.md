# Section 4: independent formalisation and exact coverage

Current continuation: R080, started 2026-10-06 16:12:04 UTC. The completed arithmetic baseline is R078. The target is the manuscript section
“The six exponentials theorem and common scales”; labels are authoritative
because numbering may change. Baseline: `de5c6e9c2d6f025665f20a5ee2c54ba373f28741`.
Branch: `codex/section4-independent`. Lean 4.32.1; mathlib
`520045ab14e26149ee970e2e617ca04b09bde5d6`.

**All Section 4 theorem, lemma and corollary obligations have compiled proofs, including the actual geometry and four-exponent-class interfaces.** The final combined closure passed for 647 modules and 5740 project kernel declarations. The independent arithmetic core also retains its 294-module / 3088-declaration audit. This table distinguishes completed graph
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
| `ex:wheatstone-arithmetic` | `WheatstoneArithmetic`, `GraphWheatstoneArithmetic` | Exact integer valuations at2,5,13; actual ambient/pivotal dimension independence; every classical rule with the same finite ambient/pivotal growth dimensions has scale2^k; GraphPhysicalClass supplies the actual four-exponent whole-class corollary. |
| `prop:iterated-response`, `lem:aligned-class` | `ScaleBlocking`, `GraphIteration` | Actual positive iterations, fixed-point equivalence, edge/scale/derivative/matrix/spectral-radius powers, dimension invariance and aligned response equivalence. |
| `lem:fixed-point-polynomial-structure`: integer quotient and endpoints | `GraphFixedPointPolynomial` | Complete quotient from actual configuration sum, integer coefficients, primitive, F(0)=−1, F(1)=1, critical root. |
| Same lemma: precise degree | `FixedPointCoefficientPositive`, `GraphFixedPointDegree` | Complete actual Classical theorem: deg(phi)=number of edges and deg(F)=edges−2. The signed top coefficient is strictly nonzero by proved deletion/contraction induction; no beta-invariant axiom or nonvanishing premise. |
| Same lemma: reduction at every prime | `GraphFixedPointCoefficients` | Complete: actual coefficient identities plus the graph involution prove all-prime nonconstancy. `GraphFixedPointParity` and `GraphFixedPointStructure` discharge every parity premise. |
| `thm:irreducible-commensurability`: local arithmetic | `IrreducibleHensel`, `IrreducibleValuations`, `IrreducibleThermal`, `IrreducibleGraphThermal` | Nonmonic Hensel, Witt lifts, integer valuations and perfect-power conclusion are proved. `IrreducibleCommensurability` discharges mod2 nonconstancy and supplies the final actual no-integer-power theorem. |
| Same theorem: integer multiplier contradiction | `IntegerMultiplierObstruction` | New coefficient recurrence excludes every integer multiplier>1. This replaces the original residue argument. Exact graph degree is proved separately in GraphFixedPointDegree. |
| Same theorem: mass conjugation and logarithmic independence | `IrreducibleConjugation`, `IrreducibleMass`, `LogarithmicIndependence` | Complete actual graph criterion in `IrreducibleCommensurability`: nonsplit mass powers, three independent dimensions, pair commensurability and common primitive base for arbitrary families. No extra reduction/degree/lifting premise. |
| Pivotal dimension transcendence | `NoIntegerPower`, `GelfondSchneider` | Complete actual classical-graph specialization under full-quotient irreducibility in `IrreducibleCommensurability`; uses only authorized GS beyond foundational axioms. |
| Closing rational pivotal dimension obstruction | `RationalPivotalObstruction` | Complete actual Classical corollary: rational pivotal dimension forces the complete quotient to fail irreducibility. Only foundational axioms; no GS or mass premise. |
| `cor:diamond-commensurability`, `ex:diamond-irreducibility` | `DiamondArithmetic` | Complete: actual mass nonsplitting via norm209, actual pivotal transcendence, actual quotient X²+X−1 irreducible, and scale2^k for every classical rule with the same finite growth triple in `GraphDiamondArithmetic`, and for the actual four-exponent class in `GraphPhysicalClass`. |

## Actual geometry and observable interfaces

`GraphHausdorffDimension` identifies the ambient coordinate with the genuine
Hausdorff dimension of `GenerationMetricSpace`: the compact completion of the
rescaled generation graphs with their compatible old-vertex isometries.
The lower bound uses actual separated interior copies and a proved symbolic
measure estimate. The upper bound uses the actual finite vertex covers.
The complete geometry closure passed for **359 modules / 3842 declarations**.
Mass and pivotal dimensions already have their manuscript meaning as finite
conditional-expectation growth limits in `GraphCriticalDimensions`.

`CoreExponentFormula` is an explicitly conditional algebraic interface, not a
replacement definition of physical exponents. `GraphCoreObservableExponents`
then proves that the actual crossing-length, escaping-mass and finite-cluster
size logarithmic limits exist uniquely and supply those formula witnesses.
`GraphObservableCommensurability` transports all nine scale conclusions to
these actual limits. The nu/beta closure passed for **482 modules / 4541
declarations**, and the delta closure for **493 modules / 4548 declarations**.
These closure counts overlap and must not be added together.

`GraphPhysicalClass` uses `SameCriticalExponentUniversalityClass`, whose four
coordinates are beta, nu, delta and eta defined by the actual observations.
The sampled ancestral graph's finite-component probabilities are proved to
equal every corresponding finite-volume limiting root-size probability; its
infinite-component probability is the complement of their sum. Thus the beta
and delta events are genuinely identified. Nu and eta use the manuscript's
finite crossing and averaged window connectivity observations directly.
No exponent formula is assumed as a mathematical axiom.

The bridge `same_physical_class_iff_criticalDimensions` proves the actual
four-exponent-class equivalence, and nine wrappers provide the rank and
irreducibility criteria, common primitive base, scale-log rank, aligned
response equivalence, and Wheatstone/diamond whole-class conclusions.
`QuadraticMassIrreducibility` also proves the stated equivalence between
irreducibility of the actual mass-plane characteristic polynomial over Q(p)
and the actual full mass spectral radius lying outside Q(p).

General graph-space local-weak convergence and almost-sure local finiteness
remain separate Section 3 object-construction statements. They are not
asserted here. Independent scope review established that these stronger
statements are not extra premises for Section 4's conclusions about the four
observable numbers: the probability identities just described give all the
observations consumed by these conclusions.

## Independent branch and public imports

All imported project source is present in this branch. Selected Section 3
sources are frozen only after their complete certified source-bound audit,
then compiled locally; no upstream object file or live checkout is used.
The R080 report records each source freeze, earlier wrong scope descriptions
and their correction. Concurrent Section 3 and Section 5 checkouts are not
modified.

- `Universality.Arithmetic.Section4`: independent finite-rule arithmetic core.
- `Universality.Arithmetic.Section4Geometry`: core plus actual Hausdorff geometry.
- `Universality.Arithmetic.Section4Observables`: geometry and actual nu/beta/delta limits.
- `Universality.Arithmetic.Section4Complete`: complete Section 4 entry including the actual four-exponent class.

The opening unconditional conjecture is not asserted as a proved theorem.
The complete entry does not claim completion of the rest of Section 3.

## Verification

Final integrated target: `Section4CombinedAudit.lean`. Its complete local closure audit passed at 2026-10-06 18:40:51 UTC: **647 modules, 58 rebuilt, 5740 mathematical kernel declarations from 645 project modules**. The final root checked every project declaration and all 25 requested endpoint prints. A separate verifier then checked every source/object pair, all recursive fingerprints, the frozen source provenance and the environment. Compiler-generated entries (76334) were counted separately.

The reproducible pinned-environment command is:

```powershell
./scripts/check-section4.ps1 -Target Section4CombinedAudit.lean -ReportName section4-combined
```

The script constructs the complete project dependency closure, checks source
and object hashes recursively, binds reuse to the actual compiler binary,
toolchain, manifest and clean pinned package revisions, rechecks all hashes
at the end, and always reruns the all-project kernel-declaration axiom audit.
It checks every imported project declaration, including unused ones, against
the foundational axioms and the two explicitly authorized external theorems.
Compiler-generated implementation entries are counted separately from
mathematical kernel declarations.

Build metadata, environment fingerprints, individual logs and dependency
records are retained under `docs/section4-*-build-*`. This is a direct Lean
PowerShell build against the stated pinned environment, not a claimed
fresh-environment portable Lake build. See the single complete
[R080 record](R080_完整研究记录.md) for independent verification and provenance.
