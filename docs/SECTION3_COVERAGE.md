# Section 3 coverage — R074 (work in progress)

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
| Vertex normalisation | `Rule.generation_vertices`, `generation_volume_formula`, `generation_volume_ratio_tendsto` | Exact finite-volume counts and limiting vertex/edge ratio |
| `lem:conditional-mass-moments`: spectral upper bound | `Rule.Classical.mass_spectralRadius_lt_edges` | Strict `ρ < m`, from an actual deficit in the single-state row and strict positivity of the fourth matrix power |
| Conditional boundary mass/volume vanishes | `Rule.Classical.conditional_boundary_mass_density_tendsto_zero` | All three actual conditional masses; infinite-volume `θ(pc)=0` still requires additional arguments |
| Higher-moment expansion | `conditionalInternalMoment_substitute`, `generation_conditionalVertexMoment` | Exact actual conditional recursion; graph associativity connects bottom-up generation to top-level cells |
| All integer higher-moment bounds | `Rule.Classical.internal_vertex_moment_bounds` | All orders, actual conditional internal-vertex masses, constants uniform in state and generation; derived by strong induction without assuming higher-moment bounds |
| Birth series by size | `generation_finiteClusterDensity_tendsto` | Exact pathwise decomposition, Bernoulli expectation, convergent birth series and actual vertex normalization; every parameter in [0,1] |
| Critical limiting cluster-size mass | `Classical.critical_cluster_size_mass_hasSum` | The pointwise limits of actual uniform-root size probabilities sum to one; derived by nonnegative double-series interchange and vanishing boundary mass |
| Full degree and spectral inequalities | `Classical.terminal_degree_spectral_bounds` | Actual graph degree satisfies `2 ≤ d_R < ρ < m`; valid for all interior percolation parameters |
| `lem:conditional-mass-moments`: remaining identification | Not yet | Identification of the normalized limiting size law with percolation on the uniformly rooted infinite graph |
| `lem:conditional-mass-local-limit` | Not yet | Infinite branching limit, smooth densities, local limit, full positive support and uniform pointwise tails |
| Finite uniform-root cluster law | `uniformVertexClusterMassProbability_eq`, `sum_uniformVertexClusterMassProbability` | Actual finite law, root/cluster counting identity and normalization; infinite-volume local law still missing |
| `def:physical-observables`: infinite volume | Partial | Individual limiting cluster densities and uniform-root size probabilities proved; construction of the uniformly rooted infinite graph and identification of percolation on it still missing |
| `thm:critical-exponents-dimensions`, `thm:delta-eta-dimensions` | Not yet | Actual ν, β, δ, averaged η; existing algebraic fractions do not discharge these |
| Crossing correlation length before its critical exponent | `Classical.crossing_length_limit`, `continuous_inverseCrossingLength`, `inverseCrossingLength_iterate` | Actual normalized log-crossing limit exists and is finite and strictly positive below criticality; continuity and exact iteration scaling proved; critical escape estimates and ν limit still missing |
| `prop:annealed-moments` | Not yet | Susceptibility and higher-moment exponent classification |
| `prop:cluster-number-response`: physical limit and functional equation | `Rule.Classical.cluster_number_density` | Actual expected cluster count/volume converges to the unique bounded solution of the paper's equation |
| Cluster-number continuity | `FiniteNetwork.continuous_clusterNumberSeries` | Continuous on the entire closed parameter interval |
| Cluster-number forcing | `internalClusterPolynomial_eval` | True internal-cluster expectation is an explicitly defined integer polynomial |
| Two exact cluster-number forcing examples | `diamond_expectedInternalClusterNumber`, `wheatstone_expectedInternalClusterNumber` | Complete component certificates and exact integer polynomials checked in the kernel; this does not yet prove their raw α values |
| `prop:cluster-number-response`: remaining regularity and examples | Not yet | Off-critical analyticity, critical `C^j`, singular response, raw α criteria, and the nine-edge example |
| `prop:annealed-radius-tail` | Not yet | Cumulative radius tails and diamond point-probability nonexistence |
| `thm:exponent-class-dimensions` | Algebra only from previous rounds | Physical theorem depends on the unfinished exponent results |
| `lem:transposition-invariance`: two-factor step | `Rule.cyclic_substitution_real_similarity` plus existing spectral/response results | Full real similarity for actual matrices, even with response/secondary eigenvalue coincidence; composites mass-admissible, factors terminal-symmetric; list-rotation wrapper and tie–gem data still missing |
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
