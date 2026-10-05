# Hierarchical-percolation universality in Lean

This is the first six-hour formalisation round for *Iterated Graph Systems (II):
Bernoulli percolation and universality class on hierarchical lattices*.
It is an independent local project; the Overleaf manuscript was not modified.

Manuscript baseline: Overleaf project `69b4d5f8e9e9b26ffd015f17`, Git `6270a59`.
Lean **4.32.1**, mathlib **520045ab14e26149ee970e2e617ca04b09bde5d6**.
The complete Chinese record and its precise limits are in
[R071](docs/R071_完整研究记录.md).

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
| Noncommutative obstruction | `no_classification_by_admissible_multiplicative_observations` | Actual finite-rule counterexample and annealed mass-growth limits, with multiplicativity required only on the mass-admissible domain; not yet a physical-exponent classification theorem |
| Cyclic substitution | `Rule.cyclic_substitution_spectralRadius`; `cyclic_substitution_response` | Actual reversed substitutions preserve edge count, distance, response and mass spectral radius at the corresponding fixed points; requires terminal symmetry for mass |
| Exponent/dimension inversion | `four_exponent_formulas_eq_iff_dimensions_eq` | Algebraic equivalence of the displayed fractions only; physical existence and formula theorems remain separate |
| Commensurability arithmetic | `commensurate_iff_rational_log_ratio`; `explicit_scales_pairwise_incommensurate` | Positive integer blocking and the explicit scale family |
| Large counterexample data | `Certificates.certificate*_integer_moments`; `signed_wheatstone_packet` | Four integer datasets, word expansions, capacity allocation and commutator algebra; full graph realisation still missing |

Strict instability follows from a finite-product variance inequality. Uniqueness
follows because the difference of crossing and occupation log odds is strictly
increasing on `(0,1)`. No transcendence or percolation theorem was added as an axiom.

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
* `Rule.MassAdmissible` is weaker than `Rule.Classical`. Its substitution closure
  is proved, as is preservation of full vertex connectivity. Full classical closure is not yet proved; the former cannot silently
  stand in for the latter's canonicality or simplicity requirements.
* Mass dimension means the annealed finite-generation expected edge-growth
  limit. Ambient edge growth is not called Hausdorff dimension without a proof
  of the metric-limit correspondence.

## Build and trust

The command actually checked in this environment is:

```powershell
./scripts/build.ps1
```

It dependency-orders every project import of `Audit.lean`, calls Lean on each
source, and prints milestone axiom dependencies. `docs/build-results.json`
records source SHA256, check time, exit code and duration. After a checked full
build, `./scripts/build.ps1 -ReuseVerified` recompiles new or changed sources and
their importing modules, retaining records for unchanged sources. The default
command rebuilds everything.

The Windows helper defaults to the shared dependency cache
`C:/Users/lzysh/Documents/Codex/lean32/packages` and the installed Lean 4.32.1
binary. Override `PackageCache` and `LeanBin` to change those paths. Dependencies
are pinned by `lean-toolchain`, `lakefile.toml` and `lake-manifest.json`. A standard
Lake build is the intended portable route, but **a fresh `lake build` has not been
verified in this round**. The direct Lean build is the verification evidence.
`lake --no-cache env lean Universality/Percolation/ClassicalCriticalPoint.lean`
was also checked successfully using the same installed dependencies. On this
shared Windows cache, Git ownership exceptions were limited to the exact package
directories in that one process; no global Git configuration was changed.

The checked library contains no `sorry`, `admit`, `native_decide`, or added
mathematical axioms. The audit reports only `propext`, `Classical.choice` and
`Quot.sound`; some finite certificates need only `propext`. Finite computations
use proof-producing tactics checked by Lean's kernel. All literals needed for
compilation are already in the source. Regenerating manuscript integer inputs
requires the original certificate JSON files, whose hashes are recorded in `docs/`.

## What is not formalised

1. The infinite-volume graph, local or metric scaling limits, and identification
   of crossing criticality with bulk infinite-cluster criticality.
2. Existence and formulas for the four selected physical critical exponents,
   the other four exponent classifications, and exponent/dimension equivalence.
3. Full preservation of the classical rule category under arbitrary substitution.
4. The six exponentials theorem and the global arithmetic rigidity theorem.
5. Full mass repair, finite rule realisation and infinite families for the large
   Section 5 certificates. Integer moments alone do not prove those claims.

Next: full classical substitution closure and the distributional random-EIGS
representation, then analytic estimates needed for the physical exponent
definitions. These remain separate theorem obligations, not bundled assumptions.
