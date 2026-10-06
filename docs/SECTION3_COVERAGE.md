# Section 3 coverage — R073

Source: `section3-20261006.tex`, frozen from manuscript commit
`fccfba64fd345f8b0cbaafd94abec48420c0c6fa`.

This table distinguishes exact finite-model results from the still missing
infinite-volume and analytic arguments. A proof of displayed algebraic
formulas is not counted as a proof of physical exponent existence.

| Manuscript item | Lean result | Scope |
|---|---|---|
| Internal masses, excluding both planting vertices | `FiniteNetwork.internalSelectedMass`, `conditionalVertexMass` | Defined by graph reachability and actual conditional Bernoulli weights |
| `eq:conditional-mass-recursion` | `internalSelectedMass_substitute` | Exact identity for every configuration of an actual glued graph |
| Conditional decomposition used in its proof | `conditional_substitution_observable` | Joint conditional law for arbitrary observables; valid off criticality |
| Finite law of the mass | `conditionalInternalPGF_substitute` | Exact generating-function recursion; reward remains jointly distributed with child states |
| Reduction of oriented types to three types | `NetworkSymmetry.conditionalInternalPGF_swap`, `conditionalVertexMass_substitute` | Explicit terminal symmetry, connected-state identification, inactive state |
| Critical first-moment iteration | `Rule.generation_conditionalVertexMass` | Actual mean equals the sum of matrix powers applied to the one-cell mean |
| `lem:conditional-mass-moments`: first-moment comparison | `Rule.Classical.internal_vertex_mass_bounds` | Uniform in generation and state; actual complex spectral radius, classical rule, interior fixed point |
| Consequent logarithmic growth | `Rule.Classical.internal_vertex_mass_logarithmic_growth` | Limit of log actual internal-vertex expectation divided by generation |
| Vertex normalisation for the birth series | `Rule.generation_vertices`, `generation_volume_formula` | Exact finite-volume counts only; birth series itself not yet proved |
| `lem:conditional-mass-moments`: other assertions | Not yet | Higher moments, the full `2 ≤ d_R < ρ < m` statement, birth series, and `θ(pc)=0` |
| `lem:conditional-mass-local-limit` | Not yet | Infinite branching limit, smooth densities, local limit, full positive support and uniform pointwise tails |
| `def:physical-observables` | Not yet | Uniform-vertex infinite-volume law and normalised cluster densities |
| `thm:critical-exponents-dimensions`, `thm:delta-eta-dimensions` | Not yet | Actual ν, β, δ, averaged η; existing algebraic fractions do not discharge these |
| `prop:annealed-moments` | Not yet | Susceptibility and higher-moment exponent classification |
| `prop:cluster-number-response`, its examples | Not yet | Cluster-number functional equation and analytic/singular response |
| `prop:annealed-radius-tail` | Not yet | Cumulative radius tails and diamond point-probability nonexistence |
| `thm:exponent-class-dimensions` | Algebra only from previous rounds | Physical theorem depends on the unfinished exponent results |
| `lem:transposition-invariance` | Spectral/response part from previous rounds | Full matrix similarity statement and examples not completed here |
| `lem:permutation-obstruction`, `thm:no-multiplicative-classification` | Mass-admissible obstruction from previous rounds | Classical substitution closure and link to physical exponent classes still needed |

## Index convention

`rule.generation 0` is the first rule graph. Thus Lean index `n` corresponds
to the manuscript's `n+1` substitution levels. The exact first-moment formula
is `Σ k = 0,...,n, M^k * mean(rule)`; the comparison with `ρ^n` absorbs one
fixed power of `ρ` into its positive constants. There is no omitted terminal
contribution: the mass explicitly excludes the two outer terminals.

## Assumptions and verification

The pathwise recursion requires only finite loopless two-terminal networks.
The conditional tower needs a nonzero crossing and noncrossing probability
for the inner cell. The three-state reduction additionally needs a terminal
swap automorphism. The final first-moment theorem uses `Rule.Classical` and
an interior reliability fixed point; no desired mass-growth conclusion is
assumed. Positivity of the initial reward is proved using an actual internal
vertex adjacent to the source.

Verification is the Lean kernel build of the entire `Audit.lean` import
closure followed by `scripts/verify_snapshot.py`; see `source-audit.json`
and `build-results.json` for the final source hashes and results.
