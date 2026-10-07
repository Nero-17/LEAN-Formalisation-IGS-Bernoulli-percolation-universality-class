# Section 3 coverage — R077 (work in progress)

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
| Critical size-law convergence | `Classical.critical_cluster_size_total_variation` | Actual finite uniform-root cluster-size laws converge in total variation to the normalized birth-series law; infinite rooted graph identification remains separate |
| Full degree and spectral inequalities | `Classical.terminal_degree_spectral_bounds` | Actual graph degree satisfies `2 ≤ d_R < ρ < m`; valid for all interior percolation parameters |
| `lem:conditional-mass-moments`: remaining identification | Not yet | Identification of the normalized limiting size law with percolation on the uniformly rooted infinite graph |
| Common infinite configuration space | `ConfigurationHistory.infiniteLaw_history_atom`, `infiniteLaw_coarsens`, `infinite_randomEIGS_joint_law` | Actual conditional Bernoulli history laws, simultaneous almost-sure coarsening consistency, complete finite labelled observables; this is not the uniformly rooted infinite graph |
| Perron population martingale | `Classical.exists_population_martingale`, `ConfigurationHistory.infiniteLaw_condExp` | Actual graph-derived weighted live-cell population, conditioned on the whole past; strictly positive eigenweights and actual spectral radius |
| Population limit | `Classical.exists_nonzero_population_L2_limit`, `ConfigurationHistory.population_L2_limit_mean` | Almost-sure and L² convergence, exact preserved positive mean; all normalized integer moments uniformly bounded |
| Exact normalized vertex-mean limit | `Classical.internal_vertex_mean_limit` | Actual affine mass recursion; strictly positive limiting vector in the genuine Perron eigenspace |
| Actual centered vertex reward | `Classical.vertex_innovation_second_moment_bound`, `Classical.vertex_reward_compensation_L2_zero` | Conditional independence proves a `C * ρ^n` innovation second-moment bound; cumulative centered reward divided by `ρ^n` vanishes in L² |
| Complementary reward population | `Classical.subcritical_population_L2_zero`, `Classical.subcritical_population_sum_L2_zero`, `Classical.vertex_reward_spectral_split` | Arbitrary real eigenweights; both population and accumulated contribution vanish at the spectral scale; exact split of the true reward into positive Perron and complementary components |
| Actual accumulated vertex-mass limit | `Classical.internal_vertex_mass_L2_limit`, `Classical.nonnegative_internal_vertex_mass_L2_limit` | Actual graph-derived internal mass converges in L² on the coherent history space to an almost surely nonnegative limit with strictly positive mean |
| Actual characteristic functions and smoothing | `Classical.internal_vertex_mass_characteristic_limit`, `Classical.internal_vertex_mass_smoothing` | Actual finite conditional mass characteristic functions converge locally uniformly to a three-type family of nonnegative positive-mean L² random variables satisfying the Fourier smoothing equation |
| Nonconstancy and nonlattice limits | `Classical.internal_single_mass_nonconstant_limit`, `Classical.internal_vertex_mass_nonlattice_limits` | Every type has characteristic function of modulus strictly less than one at every nonzero frequency; all-closed positive-weight configurations and the genuine inequality `d_R < ρ` rule out a deterministic single-state limit |
| Actual uniform mass local limit | `Classical.internal_mass_local_limit`, `internal_mass_limit_weighted_integrable` | Uniform lattice local limit to the inverse characteristic transform of the same actual limit family; finite lattice aperiodicity, global Fourier domination, L¹ convergence, and every polynomial frequency weight are proved |
| Actual smooth probability densities | `Classical.internal_mass_limit_smooth_density`, `measure_eq_withDensity_inverseCharacteristic` | For the same actual limit witness, Fourier inversion gives a globally C∞, nonnegative integrable density of total mass one, and its withDensity measure equals the actual limit law; Gaussian smoothing, Fatou, Fourier inversion and characteristic uniqueness supply the identification |
| Actual distributional smoothing | `Classical.mass_limit_distribution_smoothing` | Equality of actual limit laws with the genuine coarse-configuration mixture of independent child laws divided by the mass spectral radius; child types retain their joint coarse dependence |
| `lem:conditional-mass-local-limit`: remaining support and tail claims | In progress | Full positive support, strict density positivity, zero density on the negative half-line and the integer-index LLT wrapper, and uniform spatial pointwise tails remain separate obligations |
| Finite uniform-root cluster law | `uniformVertexClusterMassProbability_eq`, `sum_uniformVertexClusterMassProbability` | Actual finite law, root/cluster counting identity and normalization; infinite-volume local law still missing |
| `def:physical-observables`: infinite volume | Partial | Individual limiting cluster densities and uniform-root size probabilities proved; construction of the uniformly rooted infinite graph and identification of percolation on it still missing |
| `thm:critical-exponents-dimensions`: ν | `Classical.crossing_length_exponent` | Actual normalized log-crossing limit and its critical logarithmic exponent; polynomial repelling fixed-point escape estimate and compact exit-interval control are proved |
| `thm:critical-exponents-dimensions`: β; `thm:delta-eta-dimensions` | Not yet | Actual β, δ, averaged η; existing algebraic fractions do not discharge these |
| Crossing correlation length and scaling | `Classical.crossing_length_limit`, `continuous_inverseCrossingLength`, `inverseCrossingLength_iterate` | Actual normalized log-crossing limit exists and is finite and strictly positive below criticality; continuity and exact iteration scaling proved |
| Limiting size law at every parameter | `Rule.limitingRootSizeProbability_tsum_le_one`, `generation_boundary_mass_density_limit` | Actual limiting finite uniform-root size law is a subprobability law, and its missing mass equals the actual boundary-mass density limit; no infinite rooted graph identification is asserted |
| Actual moment series | `Rule.limitingRootSizeMoment_expected_birth_series`, `limitingRootSizeMoment_finite_iff_birth_summable` | Extended nonnegative moments equal the exact birth-moment series; infinite moments are retained |
| `prop:annealed-moments`: critical integer moment threshold | `Classical.critical_root_moment_finite_iff` | Actual limiting uniform-root size law has finite kth moment exactly when `ρ^(k+1) < m`, including divergence at equality; all natural k |
| `prop:annealed-moments`: fixed supercritical parameter | `Classical.supercritical_root_moment_ne_top` | For every fixed `pc < p ≤ 1`, all natural moments of the actual limiting finite uniform-root finite-cluster size law are finite; weighted crossing-failure summability follows from `φ'(1)=0` |
| `prop:annealed-moments`: fixed positive subcritical parameter | `Classical.subcritical_root_moment_finite_iff` | For `0 < p < pc`, the actual limiting uniform-root kth size moment is finite exactly when `d_R^(k+1) < m`, including divergence at equality; the necessity statement excludes `p=0` |
| Subcritical actual boundary growth and size-law normalization | `Classical.subcritical_source_mean_limit`, `subcritical_boundary_mean_limit`, `subcritical_cluster_size_total_variation` | Actual unconditional source and boundary means have positive finite limits after division by `d_R^n`; all natural moments have the corresponding upper scale; missing size mass is zero and finite uniform-root size laws converge in total variation |
| Actual moments before the critical orbit exits | `Classical.preexit_moment_comparison_with_distortion`, `preexit_moment_bounds`, `preexit_birth_moment_upper`, `preexit_birth_moment_eventual_lower` | Uniform conditional moments on both sides; distortion can be made arbitrarily close to one, and actual birth moments have matching bounds after a uniform initial depth; the lower bound retains the required two extra orbit steps |
| Actual initial-condition comparison after exit | `Classical.postexit_moment_initial_comparison` | A finite-order scale comparison for actual conditional moments propagates under the identical subsequent orbit, without replacing cluster size by incident-edge counts |
| `prop:annealed-moments`: remaining cases | Not yet | Uniform post-exit tail bounds, complete near-critical moment asymptotics and ratios, and infinite rooted graph identification |
| `prop:cluster-number-response`: physical limit and functional equation | `Rule.Classical.cluster_number_density` | Actual expected cluster count/volume converges to the unique bounded solution of the paper's equation |
| Cluster-number continuity | `FiniteNetwork.continuous_clusterNumberSeries` | Continuous on the entire closed parameter interval |
| Cluster-number forcing | `internalClusterPolynomial_eval` | True internal-cluster expectation is an explicitly defined integer polynomial |
| Two exact cluster-number forcing examples | `diamond_expectedInternalClusterNumber`, `wheatstone_expectedInternalClusterNumber` | Complete component certificates and exact integer polynomials checked in the kernel; this does not yet prove their raw α values |
| Exact cluster-number values and symmetry | `FiniteNetwork.clusterNumberSeries_fixed_point`, `wheatstone_clusterNumberSeries_half`, `wheatstone_clusterNumberSeries_reflection` | Actual series at a reliability fixed point; Wheatstone value `9/64` and reflection identity |
| Actual critical first derivative | `Classical.cluster_number_linear_remainder`, `cluster_number_hasDerivAt_critical` | The actual density has an affine approximation with a quadratic remainder bound, hence the stated first derivative at the critical point, without assuming regularity of κ |
| Actual critical C² regularity | `Classical.cluster_number_contDiffOn_two`, `cluster_number_second_deriv_continuousAt_critical` | The actual analytic extension is C² throughout (0,1); punctured derivative limits are extended using a genuine derivative theorem, beyond a Peano remainder estimate |
| Noncritical analyticity | `Classical.cluster_number_analyticAt_offcritical`, `cluster_number_densityExtension_analyticAt_offcritical` | Actual density has an analytic extension at every noncritical point of [0,1], including the endpoints; proved from complex attracting neighborhoods and the discounted polynomial series, without regularity assumptions on κ |
| `prop:cluster-number-response`: arbitrary critical order and raw response | `Classical.cluster_number_contDiffAt`, `cluster_number_raw_alpha_criterion` | Actual κ is C^j at criticality whenever φ′(pc)^j<m; hence vanishing orders 3 through j−1 and a nonzero jth derivative give raw exponent 2−j without assuming κ regularity. The proof differentiates the actual scalar equation and bootstraps, without assuming a linearizing coordinate |
| Cluster-number examples and proof expansion | In progress | Three concrete raw-α examples remain; the general proposition is proved. The manuscript's optional log-periodic/resonant representation is not claimed by the derivative-bootstrap proof |
| `prop:annealed-radius-tail` | Not yet | Cumulative radius tails and diamond point-probability nonexistence |
| Geometric prerequisites for radius arguments | `Classical.generation_diameter_bound`, `FiniteNetwork.substitute_coarse_distance`, `substitute_cell_distance` | Actual generation diameter is at most `C ℓ^n`; all coarse distances multiply by the terminal distance, and every substituted cell is isometrically embedded in the whole graph |
| `thm:exponent-class-dimensions` | Algebra only from previous rounds | Physical theorem depends on the unfinished exponent results |
| `lem:transposition-invariance`: two-factor step | `Rule.cyclic_substitution_real_similarity` plus existing spectral/response results | Full real similarity for actual matrices, even with response/secondary eigenvalue coincidence; composites mass-admissible, factors terminal-symmetric; list-rotation wrapper and tie–gem data still missing |
| Classical substitution closure | `Rule.Classical.mul`, `Rule.Classical.generation` | All six actual rule conditions: full connectivity, simple edges, every edge on a terminal simple path, scale, cut, and involutive terminal exchange |
| `lem:permutation-obstruction`, `thm:no-multiplicative-classification` | `groupedRule_classical`, `alternatingRule_classical`, `no_classification_by_classical_multiplicative_observations`, `reordered_classical_multiplicative_dimensions` | Actual classical counterexample and arbitrary families of measurements multiplicative only on the classical domain; exact common distance and different actual mass-growth limits; conversion to different critical-exponent classes still depends on the remaining exponent results |

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
