# Section 3 conclusion-level coverage review — R077

Final mass/local-limit agent review, 2026-10-07 (Asia/Shanghai).
This document is an attachment to the single R077 project archive.
It supersedes this document's earlier provisional gap notes. It does not
replace the root-maintained SECTION3_COVERAGE.md or the final whole-library audit.

**Integration update:** the subsequent final SECTION3_COVERAGE.md supersedes
the historical boundary observations below. In particular, actual metric
Hausdorff dimension is now proved by generationMetricSpace_dimH_eq, and full
rooted-ball convergence plus physical ambient-radius identification are
formally integrated. They are no longer mathematical gaps or merely external
identifications. Root reports the graph/radius individual checks complete;
the geometry has upstream R08022 verification and is undergoing its first
local recompilation, while GeometricPhysicalClass wrappers are first checked
in the combined 852-module / 928-audit target. The still-unaccepted numerical
illustrations are explicitly listed in the current coverage map.

## Conclusion and verification boundary

**No still-unformalized independent lemma/proposition clause was identified
in the conditional-mass, local-limit, finite-moment/nearcritical, or
cluster-number/raw-alpha statements reviewed below.** The former kappa
observable-identification gap has been closed. The literal manuscript-depth
LLT normalization has also passed its three-module check (root reported
checker 11522) and has been migrated.

The kappa seven-module chain and LLT normalization chain have individual
kernel evidence; their newly migrated canonical imports still await the
next full-library audit. This distinction is integration status, not a
remaining mathematical assumption.

This review does not independently certify the graph agent's newest full
uniform-root local-limit and radius-identification work. Their current
compiler/coverage status must be taken from that agent and root, not inferred
from finite-size-law convergence alone. Likewise, the cited ambient
metric-limit Hausdorff-dimension theorem is an external geometric
identification; the Lean logarithmic growth ratio is not by itself a proof
of that metric Hausdorff theorem.

## Sources and interpretation

The principal source is docs/section3-20261006.tex. The local
../overleaf-universality/main.tex was also checked for definitions and standing
assumptions. The local main moves the other four exponents to an appendix;
this does not remove their original Section 3 obligations. This review does
not claim to have freshly synchronized remote Overleaf.

The original lemma/proposition conclusions are the coverage unit. A proof's
intermediate displayed estimate is not automatically an additional theorem
obligation if the stated conclusion has another checked proof. In particular,
this applies to the stretched-exponential Fourier estimate, analytic
linearizing coordinate, and periodic/resonant representation.

The Classical assumptions match the paper's standing canonical,
terminal-symmetric, simple, connected geometry and terminal edge-connectivity
conditions. The critical parameter is an interior fixed point; the
existence/uniqueness results are already separate theorems.

## Conditional internal mass and the local-limit lemma

| Original conclusion | Declaration or chain | Review |
| --- | --- | --- |
| Actual internal mass in all three live states, with neither outer terminal counted | conditionalVertexMass, conditionalVertexMoment and actual configuration-history mass | Correct observable. It is not merely incident-edge count or an assumed branching mass. |
| 2 <= terminal degree < critical mass spectral radius < edge count | Classical terminal-degree/spectral bounds | Covered with the original geometric hypotheses. |
| First moments comparable to rho^n; all integer moments bounded by C_r rho^(rn) | Classical.internal_vertex_mass_bounds; Classical.internal_vertex_moment_bounds | Covered uniformly in generation and live state. |
| Birth series for each size and every 0<p<1 | generation_finiteClusterDensity_tendsto; clusterSizeBirthSeries; physicalFiniteClusterProbability_eq | Covered. For positive size, dividing actual root probability by size gives the limiting cluster density. The zero-size term is separately proved zero. |
| No infinite root mass at criticality | critical_escapingRootMass_zero and physicalInfiniteClusterProbability_eq | Covered for the actual annealed observable. |
| L2 mass limit used in the proof | Classical.nonnegative_internal_vertex_mass_L2_limit | Its statement includes eLpNorm convergence of normalized actual mass minus the limit, plus nonnegativity and positive mean. MemLp alone was not mistaken for convergence. |
| Smooth probability density on the nonnegative half-line | Classical.internal_mass_smooth_positive_integer_local_limit | Includes global real C-infinity regularity, nonnegativity, integrability, integral one, the actual pushforward-law identity, and zero density at negative arguments. This is at least as strong as smoothness on [0,infinity). |
| Strict positivity for the single-state density at every positive x | Same theorem, using ActualMassDensityPositive | Covered. No stronger all-state positivity is needed by the paper. |
| Uniform LLT over all integer lattice points | Same theorem | Covered including negative integers, not only natural sizes or compact spatial intervals. |
| Every integer-order spatial point tail, all nonnegative sizes and generations | Classical.internal_mass_polynomial_point_tail | Covered without assuming the desired atom bound, moment estimate, or birth LLT. |

The paper's proof claims **L2 convergence, not almost-sure convergence**.
No a.s. convergence assertion was found in the original Section 3. It is
therefore not a missing task. The final smooth-LLT theorem retains MemLp and
the density law but does not bundle the full L2 convergence statement into
its conclusion; the separate actual L2 theorem supplies the proof-level
fact. Reporting must preserve this distinction.

### Exact manuscript depth normalization

Lean generation n is manuscript depth n+1. The checked normalization is

    W_paper = W_Lean / rho
    w_paper(x) = rho * w_Lean(rho*x).

Classical.internal_mass_paper_normalization explicitly retains both laws,
MemLp for the rescaled variable, smoothness, nonnegativity, integrability,
integral one, zero density for negative x, single-state strict positivity,
and the uniform integer LLT at scale rho^(n+1).
local_limit_depth_shift_error identifies the new error as exactly rho times
the old error. Root confirmed all three modules check0 (11522).

For inequalities with an unspecified constant, the fixed one-level change
is legitimately absorbed in that constant: this applies to moment and
spatial point bounds. It is not a valid argument for identifying a normalized
density, which is why the explicit rescaling wrapper was necessary.

## Finite moments, susceptibility and moment ratios

| Original conclusion | Declaration or chain | Review |
| --- | --- | --- |
| Finite moments for every p>pc in the physical parameter interval | Classical.physical_supercritical_moment_ne_top | Includes p=1. No unmentioned strict p<1 hypothesis remains. |
| For 0<p<pc, finiteness iff d^(k+1)<m | Classical.physical_subcritical_moment_finite_iff | Exact threshold; equality gives infinity. The paper excludes p=0 from this assertion. |
| Comparison with the geometric sum from 1 through the first exit N(p) | Classical.supercritical_nearcritical_root_moment_comparison; subcritical_nearcritical_root_moment_comparison | The sum is powers n+1 over range N, exactly 1 through N. The genuine initial birth level is included. The subcritical hypothesis is precisely the stated finiteness threshold. |
| Power-divergent regime | ActualMomentPowerBounds | Genuine two-constant bounds, stronger than only a logarithmic rate. |
| Equality regime | ActualMomentPowerBounds | Two-constant logarithmic divergence, not a false positive-power assertion. |
| Below-threshold convergence to the finite positive critical value | ActualRootMomentContinuity; critical_root_moment_ne_top; CriticalMomentPositive | All three parts are present: convergence, finiteness and positivity. |
| Physical interpretation of these moment statements | physicalFiniteClusterMoment_eq | Equality holds on the entire closed probability interval, so the thermodynamic-moment estimates apply to actual finite-cluster moments. Infinity is represented in ENNReal before taking toReal in finite regimes. |
| Susceptibility on both permitted sides | PhysicalMomentExponents | Correct max-positive-part formula; subcritical susceptibility assumes d^2<m. |
| kth moment ratio | PhysicalMomentExponents | Correct difference of positive parts; subcritical ratio requires d^(k+2)<m. |
| Eventual common high-order gap; common gap for every k>=1 iff rho^2>=m | PhysicalMomentExponents; ActualMomentGap | Both quantifier ranges and the equality threshold are covered. |
| Original subcritical ratios cannot all remain finite | physical_subcritical_eventually_moment_eq_top | Covered by eventual divergence as the order increases. |

The paper's ordinary-diamond subcritical divergence is included in the
threshold theorem because d^2=m=4. The numerical exponent illustrations are
handled by root's example/numerical modules, not by weakening the above
general statements to numerical evidence.

## Kappa and raw alpha

The paper defines kappa as the sum of finite-cluster densities, not just an
arbitrary bounded solution of a functional equation. This was the substantive
gap found by the first review, and it is now closed:

    physicalClusterNumberDensity p
      = sum_s physicalFiniteClusterProbability p s / s
      = clusterNumberSeries p,       0 <= p <= 1.

The zero-size summand is zero. The proof uses the actual finite-cluster
partition to bound the contribution beyond a size cutoff by 1/cutoff,
uniformly in volume and p. Thus it remains valid when root mass escapes to
infinite clusters; it does not assume critical total finite-cluster mass one.

| Original proposition clause | Declaration or chain | Review |
| --- | --- | --- |
| Unique bounded solution and stated functional equation on [0,1] | physicalClusterNumberDensity_eq plus Classical.cluster_number_density | Covered by exact equality on the entire closed interval, including the iterate parameter. |
| Offcritical analyticity | PhysicalClusterNumberAnalyticity | Interior AnalyticAt; at endpoints, AnalyticWithinAt on [0,1] or existence of an analytic extension agreeing on [0,1]. The artificial physical zero extension is not claimed analytic across endpoints. |
| C^j at criticality whenever thermal derivative^j<m | Classical.physical_cluster_number_contDiffAt | Directly states regularity of physical kappa. |
| Always C2 | Previous theorem plus strict pivotal-response square bound | Covered without an extra hypothesis beyond Classical. |
| Raw alpha=2-j under the stated vanishing and first-nonzero derivative assumptions | Classical.physical_cluster_number_raw_alpha_criterion | Uses derivatives of physical kappa, includes punctured nonvanishing on both sides, and subtracts no analytic background. |
| Diamond alpha=-1; central Wheatstone alpha=-2 | PhysicalRawAlphaExamples | Actual kappa statements proved. |
| Wheatstone alpha=2-log(5)/log(13/8) | PhysicalRawAlphaExamples | Transported by equality on neighborhoods, not incorrectly forced through an integer Taylor-order criterion. |
| Wheatstone third-response two-constant power bound | wheatstone_physical_third_response_two_sided_power_bounds | Holds for the actual third derivative on all of (0,1) except 1/2, matching the original proved range. |

Kappa individual check evidence: UniformCountTailLimit 73945,
ClusterCountCutoff 19988, ClusterNumberSizeSum 57768,
PhysicalClusterNumber 35015, PhysicalClusterNumberResponses 74908,
PhysicalRawAlphaExamples 56922, PhysicalClusterNumberAnalyticity 22775;
all exited 0. The first Responses attempt failed only when creating its
output file; after a formal write-permission renewal the same proof checked.

## Other Section 3 conclusion-level cross-checks

The earlier review and the completed actual modules confirm that the
averaged-connectivity observable uses ordered finite-volume vertex pairs,
deterministic ambient distances, paths inside the finite graph, and every
fixed 0<a<b<1. It is not a fixed-root or spherical-shell substitute.

The four-exponent class statements use actual physical beta/delta,
crossing-length nu, and this averaged eta. The class equivalence, arbitrary
cyclic cuts, and noncommutative obstruction to arbitrary families of
multiplicative observations retain the manuscript's quantifiers. Their
remaining dimension notation requires the already stated external ambient
Hausdorff identification.

The actual diamond finite-event spike chain was individually checked and
migrated through DiamondRadiusNonexistence. It gives genuine thermodynamic
exact-radius probabilities and failure of a point logarithmic exponent.
The physical infinite-graph radius identification remains the separate graph
agent responsibility noted above; this review does not silently equate
thermodynamic tails with an ambient infinite-graph radius law.

The electrical six-module read-only review found no mathematical defect:
indexed-edge Dirichlet energy counts each unit conductance once, substitution
multiplies conductances and hence connected resistances, and Tie/Gem have
conductance 3/4 and resistance 4/3. The all-Rule real reciprocal convention
assigns zero to a disconnected conductance-zero network; that totalized value
is not a physical infinite disconnection resistance. All Classical uses are
connected and positive, so this convention does not affect the paper's
conclusions. Electrical compiler status remains root's responsibility.

## Explicit remaining status

No additional independent lemma/proposition clause in the reviewed
mass/LLT/moment/kappa conclusions is left as an assumed conclusion or an
unproved hypothesis. Remaining work is the team's tracked graph-law/radius
closure, the final whole-library integration/audit, and accurate reporting of
the external ambient geometric identification. Do not list absent alternative
proof displays or an unclaimed a.s. convergence theorem as new obligations.
