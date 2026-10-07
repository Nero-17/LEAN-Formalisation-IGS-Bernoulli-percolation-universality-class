# Section 5: verified formalisation snapshot

This branch publishes the completed R079 Section 5 source and its exact dependencies.
Start with [publication and review notes](docs/SECTION5_PUBLICATION.md),
[the formal entry](Universality/Section5.lean), and
[the reproduction guide](docs/section5-guide.md).
**Restore the 44 generated data files before compiling:**
[restoration instructions](RESTORE_GENERATED_DATA.md).

The main branch retains the separately verified final Section 3 tree and the
[project progress overview](https://github.com/Nero-17/LEAN-Formalisation-IGS-Bernoulli-percolation-universality-class/blob/main/docs/FORMALISATION_PROGRESS.md).
This independent snapshot does not claim a merged Sections 2–5 build.

---

The original working snapshot README follows. Earlier chapter status below is historical.

# Hierarchical-percolation universality in Lean

This project formalises *Iterated Graph Systems (II):
Bernoulli percolation and universality class on hierarchical lattices*.
It is an independent local project; the Overleaf manuscript was not modified.

Manuscript baseline: Overleaf project `69b4d5f8e9e9b26ffd015f17`.
R071 used Git `6270a59`; the R072 Section 2 snapshot includes the additional
pivotal-response bound in Git `fccfba64`.
Lean **4.32.1**, mathlib **520045ab14e26149ee970e2e617ca04b09bde5d6**.
The complete Chinese record and its precise limits are in
[R071](docs/R071_完整研究记录.md), [R072](docs/R072_完整研究记录.md), and
[R074](docs/R074_完整研究记录.md), [R075](docs/R075_完整研究记录.md), and
[R077](docs/R077_完整研究记录.md).

Section 5 is documented in the [formalisation and verification guide](docs/section5-guide.md)
and the [R079 complete record](docs/R079_完整研究记录.md). These give its actual
graph interfaces, numerical certificate status, source provenance, and checked
reproduction procedure. The public entry point is `Universality.Section5`.

Section 5 is complete: all four original numerical certificates, the actual
three seeds, the specified infinite family, physical critical exponents,
Hausdorff dimension, and shifted transcendence conclusions have passed.
The four-exponentials conjecture remains an explicit hypothesis, and
transcendence uses the previously accepted Gelfond–Schneider interface.
The final incremental closure has 906 modules; its actual
top-level dependency output covers 8543 project kernel
declarations. Full evidence and reproduction instructions are in the
Section 5 guide and R079 record linked above.

## Historical Section 3 checkpoints (R073–early R077)

This section records the earlier baseline, rather than the current open-problem
list. R079 has since imported and recompiled the minimal upstream dependencies
for the actual uniformly rooted infinite graph, its physical critical exponents,
and the Hausdorff dimension of the compact metric completion. Their scope and
source provenance are recorded in the Section 5 guide linked above. This branch
does not claim to include every later, unrelated Section 3 or Section 4 module.

The first tranche proves the actual internal-vertex mass recursion, its full
finite probability-generating-function recursion (retaining the dependence
between the top-level reward and the offspring states), terminal-swap
invariance, and the resulting affine three-state expectation recursion.
`Rule.Classical.internal_vertex_mass_bounds` proves uniform positive lower
and upper multiples of the genuine mass spectral radius to the generation
power, from the classical geometric hypotheses. Exact finite-volume vertex
counts are also proved. The complete scope and remaining obligations are in
[the Section 3 map](docs/SECTION3_COVERAGE.md).

R074 adds all integer mass-moment bounds, `2 ≤ d_R < ρ < m`, the size-resolved
birth series and its actual finite-volume limit, and normalization and total
variation convergence of the critical uniform-root size law. It proves the
actual crossing-length limit and its critical exponent ν, including the
repelling fixed-point escape estimate. The cluster-number volume limit,
functional equation, uniqueness, continuity and two exact forcing polynomials
are proved. Full classical substitution closure and the resulting classical
noncommutative counterexample are also proved.

R075 constructs a common infinite probability space with exactly the actual
conditional Bernoulli history laws, simultaneous coarsening consistency,
and the full labelled EIGS law. The actual Perron-weighted population is a
martingale for the complete past, has uniformly bounded normalized moments
of every integer order, and converges almost surely and in L² to a limit
with strictly positive preserved mean. The actual accumulated internal
vertex mass also has an L² limit, with strictly positive mean.

The actual normalized vertex means converge to a strictly positive Perron
eigenvector. The centered reward from one actual refinement has second moment
at most `C * ρ^n`; the accumulated centered rewards divided by `ρ^n` converge
to zero in L². These estimates use the conditional cell product law, without
assuming independence between a cell's reward and its offspring types.
The complementary reward population and its accumulated sum vanish in L²
at the spectral scale. An exact telescoping identity identifies the vertex
limit with a positive scalar multiple of a Perron population limit. The
smoothing equation and local limit theorem were separate obligations at R075.

R077 proves the actual Fourier smoothing equation, locally uniform convergence
of the finite mass characteristic functions, and nonlattice limits for all
three types. It proves the exact critical integer moment threshold for the
limiting finite uniform-root size law, including divergence at equality, and
finiteness of all integer finite-cluster moments at fixed supercritical
parameters. The actual cluster-number density has the stated first derivative
at criticality without assumed regularity. Exact cell isometry and uniform
generation diameter bounds are also proved. The first R077 checkpoint passed
the complete 439-module build and 289 milestone audits. Further results in
the coverage map are being integrated and audited in the same ongoing round.

Further R077 single-module checks establish the fixed positive subcritical
moment threshold, actual mass local limits and smooth probability densities,
the cluster-number proposition at every allowed differentiability order,
and uniform pre-exit moment estimates. The second complete checkpoint passed
522 modules and 337 milestone audits, with zero source/build audit errors.

At that early checkpoint, the full Section 3 development remained incomplete.
Its then-open list included positive densities and spatial tails, the uniformly
rooted infinite graph, β/δ/averaged η, near-critical moments, examples and radius
laws. This is historical status, not the current status of the imported results.

## Section 2 continuation (R072)

The Section 2 proof chain now includes the full finite-dimensional joint law
of the critical random EIGS, its actual cluster extraction, the geometric
limit under compatible contractions, the exact counting polynomials and
critical characteristic polynomial, and the four-edge diamond example.
The added strict bound `deriv reliability p ^ 2 < edges` is proved from the
actual Bernoulli covariance. The statement-by-statement coverage table,
assumptions and current verification evidence are in the R072 report.

`Rule.critical_randomEIGS_joint_law` concerns arbitrary observables of every
generation's labels, rather than only their first moments.
`offspring_labels_conditionally_independent` supplies the state-dependent
joint rule kernels. Single-terminal orientation is retained until symmetry
is applied; sibling labels within one rule are not assumed independent.

`Geometry.TypedGraphRealisation.geometric_limit` is pathwise for every fixed
realisation of whole-rule choices. It proves a nonempty compact limit,
address coding, the graph-directed set equation and the precise Hausdorff
bound using the maximum diameter of the finitely many type spaces. Finite
rule laws are normalised. R075 additionally constructs the infinite
conditional configuration-history measure and identifies all its finite
labelled marginals with the actual percolation law. The later uniformly rooted
infinite-graph identification used by Section 5 is now imported and checked.

## What is actually proved

The core objects are actual edge-indexed finite graphs, Bernoulli configurations,
graph reachability, and conditional open-cluster edge counts. Their matrix
formulas are derived, rather than used as replacement definitions.

| Manuscript argument | Principal Lean entry points | Coverage |
|---|---|---|
| Finite classical rules | `Rule.Classical`; `wheatstoneRule_classical`; `oppositeWheatstoneRule_classical` | Connected simple rule, canonical paths, distance, single-edge cuts, involutive terminal swap; both seeds certified |
| Reliability under substitution | `FiniteNetwork.substitute_reliability`; `Rule.generation_reliability_iterate` | Actual glued graphs, independent child crossings and composition |
| Nontrivial crossing transition | `Rule.Classical.finite_crossing_transition` | Existence, uniqueness, strict instability, actual finite-generation crossing probabilities tending to 0 or 1 |
| Edge-cut criterion | `FiniteNetwork.interior_fixed_point_iff_terminalEdgeConnectivity` | The minimum cardinality of an actual terminal cut is at least two exactly when an interior fixed point exists, for connected rules of terminal distance at least two |
| Bernoulli response | `FiniteNetwork.russo_formula`; `strict_bernoulli_poincare` | Direct finite-product proofs and fixed-point derivative greater than 1 |
| Conditional mass recursion | `FiniteNetwork.substitutedMassMatrix_eq_mul`; `Rule.generation_massMatrix` | Actual conditional probabilities and local states, with terminal symmetry |
| Primitive mass matrix | `FiniteNetwork.massMatrix_fourth_power_pos` | Every entry of the actual fourth power is positive |
| Mass dimension | `Rule.Classical.mass_dimension` | Limit of log expected open-cluster edge count divided by log actual terminal distance |
| Pivotal dimension | `Rule.Classical.pivotal_dimension`; `pivotal_mass_inequalities` | Actual pivotal growth and `0 < dim_P < dim_M` |
| Three-state structure | `pivotal_left_eigenvector`; `massMatrix_real_diagonalization`; `exact_conditional_cluster_mass` | Off-critical left eigenvalue, invariant plane, critical 2+1 decomposition, real diagonalisation, exact mass expansion |
| Noncommutative obstruction | `no_classification_by_classical_multiplicative_observations` | Actual classical rules and annealed mass-growth limits; multiplicativity required only on the classical domain; conversion to different physical-exponent classes remains separate |
| Cyclic substitution | `Rule.cyclic_substitution_real_similarity`; `cyclic_substitution_response` | Full real similarity for two-factor cyclic composites, including repeated response/secondary eigenvalues; actual edge counts and distances agree |
| Exponent/dimension inversion | `four_exponent_formulas_eq_iff_dimensions_eq` | Algebraic equivalence; the actual physical existence and formula results used in Section 5 are supplied separately by `RuleResponses.hasCriticalExponents` |
| Commensurability arithmetic | `commensurate_iff_rational_log_ratio`; `explicit_scales_pairwise_incommensurate` | Positive integer blocking and the explicit scale family |
| Large counterexample data | `Certificates.certificate*_integer_moments`; `signed_wheatstone_packet` | Four integer datasets and actual finite-graph realisation; see the Section 5 guide for the remaining Base661 mass verification and final assembly |

Strict instability follows from a finite-product variance inequality. Uniqueness
follows because the difference of crossing and occupation log odds is strictly
increasing on `(0,1)`. These percolation arguments use only standard logical axioms. The separate Section 5 transcendence results use the accepted Gelfond–Schneider interface.

## The graph counterexample

The five-edge Wheatstone graph has conditional mass block
`[[53,48],[13,42]]/16`, fixed point `1/2`, derivative `13/8`, and distance 2.
The thirteen-edge opposite-pair replacement graph has block
`[[1896,2292],[627,1380]]/256`, fixed point `1/2`, derivative `67/32`, and distance 3.

All 8192 configurations of the second graph are checked. Python supplies
candidate component certificates; Lean checks their validity, coverage,
conditional counts and reliability histogram using ordinary kernel `decide`.
An externally computed count is never assumed to be correct.

The actual AABB and ABAB rules both have 4225 edges, terminal distance 36, fixed
point `1/2`, and derivative `(871/256)^2`. Their mass spectral radii and actual
iterated conditional cluster-mass growth rates differ, although every family
of scalar substitution-multiplicative observations agrees on the two rules.

## Conventions that matter

* `outer * inner` replaces each edge of `outer` by `inner`. In the manuscript's
  convention this is **`inner ∘ outer`**, not `outer ∘ inner`.
* `rule.generation 0` is the first rule graph. Generation `n` means **`n+1`**
  substitutions when the initial single edge is numbered zero.
* Connectivity is undirected; edge indices remain distinct for independent
  Bernoulli states. `Rule.Classical.simple` separately excludes parallel edges.
* `Rule.MassAdmissible` is weaker than `Rule.Classical`. Substitution closure
  is proved for both. The classical proof explicitly preserves simplicity,
  canonical terminal paths and an involutive terminal exchange.
* Mass dimension means the annealed finite-generation expected edge-growth
  limit. Ambient edge growth is not called Hausdorff dimension without a proof
  of the metric-limit correspondence.

## Build and trust

Use the [Section 5 verification guide](docs/section5-guide.md) for the current
public import closure and exact reproduction instructions. Its driver first
produces a plan without running Lean:

```powershell
python scripts/section5_final_driver.py --decisions docs/section5-final-history-decisions.json
```

Review any changed source, object or dependency evidence before adding
`--execute`. The incremental driver preserves genuine historical receipts and
runs the final declaration audit from source. `--fresh` explicitly selects a
full source rebuild. The earlier `build.ps1` logs belong to historical
milestones and are not the complete Section 5 acceptance record.

The pinned runtime is Lean 4.32.1 with the mathlib revision listed above.
Windows PowerShell helpers accept `LeanBin` and `PackageCache` overrides.
The Python driver uses paths in `scripts/section5_receipt_closure.py`; see the
guide before configuring another machine. A fresh portable `lake build` has
not been verified in this round.

No proof uses `sorry` or `native_decide`. The only external mathematical axiom
in the Section 5 dependency closure is the explicitly accepted
Gelfond–Schneider interface, used for transcendence. Other results use standard
Lean logical axioms (`propext`, `Classical.choice`, `Quot.sound` as needed).
The four-exponentials conjecture is an explicit proposition hypothesis, not
an axiom or a proved theorem. Finite checks produce ordinary kernel proofs.

The local workspace contains all generated data. The single round archive
stores 44 large data modules through an exact, fully tested restoration recipe;
follow its `RESTORE_GENERATED_DATA.md` before building an extracted archive.
The archive retains every proof, original certificate JSON, generator and
source hash. Reconstruction restores source and does not replace Lean checking.

## Current scope and remaining work

The checked actual 19 and 739 rules have the same physical critical exponents
and incommensurate scales. The shifted-19 rule, its three transcendental
dimensions, and their rational-span statements are checked. Base661's remaining
initial-mass checks and the final public assembly are still in progress; their
completion is required for the original three-seed and infinite-family claims.
The full current status is in the R079 report linked above.

The eta result concerns fixed macroscopic distance windows. The actual ambient
Hausdorff dimension concerns the compact completion of rescaled generation
graph metrics; it does not assert a random cluster scaling limit. Open
conjectures in the manuscript's discussion remain open, and conditional
four-exponentials consequences retain their hypothesis. Rounded decimal
illustrations are not certified error intervals.
