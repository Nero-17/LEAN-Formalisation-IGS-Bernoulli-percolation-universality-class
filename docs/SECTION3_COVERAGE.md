# Section 3 — verified final coverage


Project: universality_class / R077. Source: [section3-20261006.tex](section3-20261006.tex).
This map follows the frozen original Section 3, including the four additional
exponents now placed in an appendix of the local manuscript. It supersedes
the former accumulating checkpoint table. Historical evidence remains in
the single R077 complete report.

## Acceptance status

**Section 3 accepted.** The complete canonical import closure passed at
2026-10-06T20:05:04.0560222Z: **863 modules / 956 ordered kernel axiom outputs /
136 finite-certificate batches**. Independent source/build verification has
zero errors; observed axioms are only propext, Classical.choice and Quot.sound.
Code commit: `5b80bbe96fd5d55e4ce2ee03e3576665d5e37eb6`. Post-build source/object hashes, recursive project
dependency fingerprints and the Lean binary hash are sealed in
`section3-final-integrity.json`.

The scope is the original manuscript's **12 independent theorem/lemma/
proposition/corollary statements, five definitions and three examples**,
including the four additional exponents later moved to an appendix. All
Tie/Gem numerical claims, the additional gamma/alpha intervals, electrical
examples and actual Hausdorff classification wrappers are now in this build.
The focused entry is `Universality.Section3`. Proof-display boundaries below
remain explicit; completion concerns the stated conclusions and examples.

## Scope, definitions and conditions

The source has **12 theorem/lemma/proposition/corollary environments**, five
definition environments, and three example environments. The second label
def:static-class belongs to thm:exponent-class-dimensions; it is not an
additional theorem. Both physical-observable definition labels name the same
definition.

Rule.Classical records the actual finite loopless simple two-terminal rule,
full connectivity, every edge on a terminal simple path, terminal distance
at least two, survival of every single-edge deletion, and involutive terminal
exchange. No desired mass, exponent, or density conclusion is a field of this
structure. At criticality, theorem parameters are 0<pc<1 and reliability(pc)=pc;
the existence and uniqueness of that interior critical point are proved
elsewhere in the formal chain.

Unless explicitly stated otherwise, probabilities use the physical parameter
interval [0,1]. Physical observables outside it have an artificial zero
extension; no physical assertion for p<0 or p>1 is intended.

| Manuscript definition | Formal interpretation and conditions |
| --- | --- |
| def:physical-observables; def:annealed-percolation | Graph.UniformRootProbabilitySpace constructs the actual age-mixture rooted graph with independent Bernoulli edge bits. Graph.UniformRootLocalLimit proves convergence of every fixed-radius full rooted-ball isomorphism event from uniform finite vertices. Graph.UniformRootLocalFiniteness proves almost-sure finite neighbor sets. Finite/infinite cluster probabilities are identified by UniformRootSizeIdentification and PhysicalObservables. For size>0, n_s is physicalFiniteClusterProbability/s and equals the actual cluster-count density limit; size zero contributes zero. The graph/local-limit bridge is verified in the final full build. |
| def:four-exponents | Rule.HasCriticalExponents in PhysicalExponentDefinition uses actual physical infinite-cluster probability, actual crossingCorrelationLength, actual physical finite-cluster point probability, and finite averagedWindowConnectivity. The point law is eventually positive. The eta statement covers every fixed 0<a<b<1, ordered vertex pairs, deterministic ambient distance, and connecting paths inside the finite graph. |
| def:other-exponents | physicalFiniteClusterMoment is an ENNReal finite-cluster moment, assigning zero to infinite clusters. physicalClusterNumberDensity is the sum of physical probability/size. Actual infinite ambient-radius tail/point events are in UniformRootRadiusIdentification and UniformRootRadiusPointLaw. Susceptibility and gap conclusions retain side and moment-order conditions; raw alpha requires eventual nonvanishing; radius logarithms are along positive integer radii. |
| def:general-class | SameCriticalExponentUniversalityClass means existence of common actual beta, nu, delta and eta limits. It does not require equality or existence of all eight exponents. Existence and uniqueness of the selected four are separate proved results. |
| def:multiplicative-dimension | The arbitrary-index-family multiplicative observation/dimension theorems include every positive scalar functional satisfying the stated admissible-composition law. They apply simultaneously to all such functionals, hence in particular to finite families. Effective resistance is an actual variational example on connected rules. |

### Actual ambient geometry

The map no longer treats the ambient Hausdorff formula as only an external
citation or a definition of a logarithmic number.
Rule.GenerationMetricSpace is the completion of the actual directed union of
rescaled generation graph metrics. GenerationCompletion, GenerationCompactness,
GenerationMetricSpace and GenerationMetricCells establish its metric,
compactness, finite-generation inclusions and cell similarities.
Rule.generationMetricSpace_dimH_eq in Geometry.GenerationHausdorffDimension
proves

    dimH (univ : Set (GenerationMetricSpace h))
      = ENNReal.ofReal (log(rule.edges) / log(terminal distance)).

The lower bound uses separated interior cell copies; no bounded-degree
assumption or desired Hausdorff-dimension equality is postulated. This new
geometry chain is formal, with upstream R08022 verification; its first local
recompilation and the previously untested GeometricPhysicalClass wrappers
have passed the integrated full audit.

## Complete original statement map

Names below are in Universality or its Rule/Classical and FiniteNetwork
namespaces. Module paths remove ambiguity without repeating every prefix.

| Original label (source line) | Full mathematical scope | Formal declarations / modules and acceptance boundary |
| --- | --- | --- |
| lem:conditional-mass-moments (109) | All live states, actual internal vertices excluding both outer terminals; 2<=d<rho<m; first moment comparable to rho^n; every integer r>=1 upper bound; birth series for every 0<p<1 and s>=1; theta(pc)=0. | terminal_degree_spectral_bounds; internal_vertex_mass_bounds; internal_vertex_moment_bounds; generation_finiteClusterDensity_tendsto; critical_cluster_size_mass_hasSum; critical_escapingRootMass_zero. PhysicalObservables transfers the size/infinite law. Actual model bounds and birth series are in the last full snapshot; the full rooted-graph-law bridge is included in the verified final build. |
| lem:conditional-mass-local-limit (164) | Smooth probability density on [0,infinity) for every live state; uniform over all integer sizes; single-state density strictly positive on (0,infinity); all integer-order spatial point tails. | internal_mass_smooth_positive_integer_local_limit and internal_mass_polynomial_point_tail already checked in the full source chain. internal_mass_paper_normalization adds the exact original depth convention with the same law, normalized rescaled density, and error identity; its three-module chain is verified in the final full audit. |
| thm:critical-exponents-dimensions (281) | Actual beta and nu exist for every Classical rule and have the stated dimension fractions. | PhysicalCriticalExponents.physical_beta_exponent; CrossingExponent.crossing_length_exponent; PhysicalExponentDefinition.hasCriticalExponents. The actual crossing limit, positivity, supercritical order parameter and log rates are proved. GenerationHausdorffDimension now supplies the actual ambient dimH identification. |
| thm:delta-eta-dimensions (342) | Actual finite-cluster point-law delta and averaged-connectivity eta exist; any fixed 0<a<b<1 window has the same eta. | physical_delta_exponent; CriticalRootSizePowerBounds, CriticalRootSizeExponent and birth point upper/lower chains; AveragedConnectivityExponent.averaged_connectivity_exponent; PhysicalExponentDefinition.hasCriticalExponents. The size conclusion uses point probabilities, not just cumulative tails. Eta uses actual finite ordered-pair expectations and window normalization. |
| prop:annealed-moments (448) | For every k>=1, finiteness for pc<p<=1; for 0<p<pc, iff d^(k+1)<m; nearcritical comparison with sum from 1 through N(p) on each finite side; finite positive critical limit below the rho threshold. | physical_supercritical_moment_ne_top; physical_subcritical_moment_finite_iff; NearCriticalRootMoment.supercritical_nearcritical_root_moment_comparison and subcritical counterpart; ActualMomentPowerBounds; ActualRootMomentContinuity; CriticalMomentPositive; physicalFiniteClusterMoment_eq. Equality at the degree threshold diverges. The actual initial birth level is included. No target moment estimate is assumed. |
| prop:cluster-number-response (602) | Kappa is the unique bounded solution on [0,1] of the stated equation, analytic off pc, C^j at pc when thermal^j<m, always C2, and raw alpha=2-j under the stated vanishing/leading-jet hypotheses. | PhysicalClusterNumber.physicalClusterNumberDensity_eq plus ClassicalClusterNumber.cluster_number_density; PhysicalClusterNumberAnalyticity; physical_cluster_number_contDiffAt; pivotal_response_sq_lt_edges; physical_cluster_number_raw_alpha_criterion. The true sum of physical size densities is identified at every p in [0,1]. Endpoint analyticity is within [0,1] or via an actual analytic extension. This seven-module physical-kappa chain is verified in the final full audit. |
| prop:annealed-radius-tail (756) | Actual critical ambient-radius cumulative two-constant power law for every Classical rule; if a finite point exponent exists, its necessary value; ordinary diamond point exponent does not exist. | Graph.PhysicalRadiusExponents.uniformRoot_critical_radius_power_bounds; uniformRoot_critical_radius_point_exponent_value; diamond_uniformRoot_radius_point_log_limit_nonexistent. UniformRootRadiusIdentification/PointLaw identify actual infinite ambient-radius probabilities with the proved thermodynamic tail/point laws. The diamond input is the actual isolated-cell exact-radius spike event, not an assumed spike. New physical radius bridges are verified in the final full audit. |
| thm:exponent-class-dimensions; def:static-class (833) | Same actual four-exponent class iff all three critical dimensions agree. | PhysicalExponentClass.Classical.same_critical_exponent_class_iff_dimensions; GeometricPhysicalClass.Classical.same_critical_exponent_class_iff_geometric_dimensions; PhysicalExponentDefinition existence/uniqueness; Algebra.ExponentRecovery. Both directions use actual observable limits. The geometric wrapper directly uses actual metric dimH and has passed its first complete canonical check and final audit. |
| lem:transposition-invariance (1026) | Every cyclic rotation of every finite word of at least two terminal-symmetric factors, with admissible cyclic composites, preserves all three dimensions and gives real similarity of the critical three-state matrices. | Graph.ArbitraryCyclicWord.cyclic_block_word_fixed_point, response, edges, distance, spectralRadius, real_similarity and three_growth_values; Percolation.CyclicPhysicalClass.cyclic_block_word_physical_exponent_class. The factor conditions permit path/triangle factors of scale or cut one; admissibility is on the composites. The mapped critical parameter is explicit. This is arbitrary cuts, not only two fixed sample matrices. |
| lem:permutation-obstruction (1070) | Two actual admissible rules whose alternating and grouped fourfold composites have equal ambient and pivotal dimensions but different mass dimensions. | Examples.ClassicalSeeds, GraphNoncommutativity and ClassicalNoncommutativity; reordered_rules_edge_counts, fixed_points, terminal_distances and response; reordered_graph_mass_spectralRadii_ne. The actual Wheatstone/opposite-Wheatstone graph data and rational trace obstruction are kernel-certified, including finite configuration certificates. |
| thm:no-multiplicative-classification (1127) | No finite family can classify the three dimensions; the same pair defeats all positive substitution-multiplicative dimensions simultaneously. | no_multiplicative_classification_of_graph_mass; reordered_classical_multiplicative_dimensions; multiplicative_observations_fail_physical_classification; multiplicative_dimensions_fail_physical_classification. The actual unequal mass Perron roots are part of the witness, not merely unequal labels for a class. Arbitrary index families strengthen the finite-family assertion. |
| cor:ambient-does-not-classify (1142) | Equal ambient dimension need not imply equal critical-exponent class. | Examples.PhysicalClassCounterexample.ambient_dimension_does_not_classify_physical_exponents; reordered_physical_exponent_classes_differ; GeometricPhysicalClass.hausdorff_dimension_does_not_classify_physical_exponents. The last theorem directly states equal actual metric dimH and has passed the final full audit. |

## Additional stated conclusions and examples

These claims are kept separate from the 12 labelled theorem environments so
that examples and proof displays are not accidentally double-counted.

| Original item | Coverage |
| --- | --- |
| Susceptibility paragraph after prop:annealed-moments | ActualMomentPowerBounds gives true power bounds and equality-case logarithmic bounds; ActualRootMomentContinuity and CriticalMomentPositive give the finite positive critical limit. PhysicalMomentExponents gives both permitted-side gamma formulas. The supercritical side is always finite; the subcritical side requires d^2<m. |
| Moment-ratio paragraph | PhysicalMomentExponents gives the exact positive-part difference for every order, the subcritical requirement d^(k+2)<m, eventual common high-order gap, and the all-k>=1 common-gap iff rho^2>=m. physical_subcritical_eventually_moment_eq_top proves that the original subcritical ratios cannot all remain finite. |
| ex:dhl-four-exponents (404) | Examples.DiamondFourPhysicalExponents.diamond_four_physical_exponents and diamond_four_exponent_decimal_bounds give actual four-exponent values and rigorous intervals supporting the displayed decimals. |
| ex:cluster-number-responses (671), including eq:wheatstone-third-response | Examples.PhysicalRawAlphaExamples gives actual kappa raw alpha -1 for diamond, -2 for central Wheatstone, and 2-log(5)/log(13/8) for Wheatstone. wheatstone_physical_third_response_two_sided_power_bounds proves the strong two-constant fractional-power bound for the actual third derivative on (0,1) except 1/2. The physical wrappers are included in the verified final build; the underlying forcing certificates and strong bounds are proved. |
| ex:tie-gem-similarity (859): exact graph, reliability, critical-parameter relations and common class | TieGemData, TieGemSimilarity, TieGemClassical and TieGemPhysicalClass prove six edges, terminal distance two, both reliability formulas, the exact relation between critical parameters, equality of thermal and mass spectral data, explicit real similarity, and the same actual physical exponent class. These exact statements are not conditional on decimal experiments. |
| ex:tie-gem-similarity: resistance 4/3 | Graph.DirichletEnergy, SubstitutionEnergy, ConductanceMultiplicativity and ConnectedConductance plus Examples.TieGemResistance: path conductance 1/2, triangle conductance 3/2, hence Tie/Gem conductance 3/4 and connected effective resistance 4/3. Six electrical modules are individually checked and verified in the final full audit. |
| ex:tie-gem-similarity, tab:tie-gem-detail, and the three approximate eigenvalues | Eight canonical Examples/Matrix modules through TieGemCommonSpectrum certify critical points, thermal response, the actual Perron interval (5.708705,5.708725), and a common actual full-spectrum third eigenvalue in (1.42005,1.42015). All included in the final full audit. |
| Diamond gamma+ approximately 2.9412 and Wheatstone raw alpha approximately -1.3150 | **Included in the verified final build.** DiamondSusceptibilityNumerical and WheatstoneAlphaNumerical give the explicit rounding intervals stated above. The diamond module also directly proves physicalFiniteClusterMoment p 1=top for every 0<p<pc. |
| Effective-resistance multiplicative dimension after def:multiplicative-dimension | Graph.ResistanceObservation.effectiveResistance_mul; Classical.effectiveResistance_pos; equal_resistance_dimension_does_not_classify. The variational definition is actual unit-edge resistance on connected rules, and the physical classification counterexample applies. |

## Proof identities and normalization

The principal displayed identities needed to connect the observables are
present, rather than assumed:

- eq:conditional-mass-recursion: internalSelectedMass_substitute and the
  actual conditional-substitution observable/PGF law. Reward and child types
  retain their joint coarse dependence.
- eq:birth-cluster-series and eq:birth-moment-series: exact birth decomposition,
  vertex normalization and nonnegative series interchange, including infinite
  moments.
- eq:mass-smoothing: actual mass_limit_distribution_smoothing, with independent
  child laws conditional on the coarse configuration.
- eq:conditional-mass-llt and eq:conditional-mass-point-bound: smooth positive
  integer LLT, exact paper normalization, and all-order actual point tails.
- eq:critical-escape-time, eq:near-critical-moment-sum and
  eq:pre-exit-birth-moment: actual first-exit time, bounded logarithmic
  distortion, uniform pre-exit moments and complete post-exit series control.
- eq:annealed-mass-point-law: actual birth point upper and lower estimates,
  geometric summation and the physical size-law bridge.
- eq:cluster-number-functional and eq:cluster-number-series: actual finite
  cluster-count recursion and the bounded discounted series, now identified
  with physical kappa on [0,1].
- eq:diamond-radius-spikes: actual finite graph metric geometry, compatible
  positive-probability event, exact-radius root count and transfer to the
  thermodynamic point law; then the actual infinite-radius identification.
- eq:substitution-responses: actual edge/distance multiplication, crossing
  composition and three-state matrix product under the terminal-symmetry
  conditions.

Lean generation 0 is the first rule graph, so generation n is paper depth
n+1. The LLT uses the exact change W_paper=W_Lean/rho and
w_paper(x)=rho*w_Lean(rho*x), with error multiplied by rho. The actual
pushforward law, integral one and support are preserved by the checked
normalization chain. Fixed one-level shifts in inequalities with unspecified
positive constants and in logarithmic exponents have their usual harmless
constant/index adjustments; this observation was not used as a substitute
for density rescaling.

The proof-level actual mass limit is L2, with a positive mean and an almost
surely nonnegative limit. The paper does not assert almost-sure convergence
of these normalized masses. The final LLT bundle should not be described as
an a.s. convergence theorem merely because it contains MemLp and a density law.

## Explicit scope boundaries

1. The new actual metric Hausdorff result, full rooted-ball convergence and
   infinite ambient-radius identification are present in formal source;
   older notes treating them as missing or only externally cited are obsolete.
   Their complete canonical integration and final audit have passed.
2. The periodic/resonant representation eq:cluster-number-log-periodic and its
   analytic linearizing-coordinate construction have not been separately
   formalized. The original proposition's analyticity, C^j and raw-alpha
   conclusions have alternate checked proofs. Likewise, the LLT uses
   sufficiently strong polynomial Fourier domination rather than separately
   asserting the proof's exact stretched-exponential display.
3. Kappa endpoint analyticity means an analytic extension agreeing on [0,1],
   or AnalyticWithinAt there. The physical function's zero extension outside
   [0,1] is not claimed analytic at the endpoints.
4. Radius means ambient deterministic graph distance, not intrinsic open-path
   distance. The point exponent requires eventual positive probabilities;
   zeros do not become a fictitious finite exponent through Lean's totalized
   real logarithm.
5. Effective resistance is physically interpreted on connected terminal
   pairs. The all-Rule real reciprocal convention assigns 0 to conductance
   zero, not the infinite resistance of a disconnected circuit. All
   Classical rules and all examples used in the classification result are
   connected with positive conductance.
6. Concrete finite enumeration is kernel-certified. Decimal illustrations
   require proved interval bounds; all Tie/Gem and additional numerical modules are included in the final full build.

## Final acceptance evidence

All canonical modules are reachable from Audit.lean. The full Lean build,
ordered axiom output, source SHA256 verification, and post-build source/object/
dependency integrity check passed. The final archive is the existing R077 ZIP,
not a new checkpoint file. The project progress index uses its existing ID.

DiamondSusceptibilityNumerical certifies gamma+ in [2.94115,2.94125] and the
actual infinite subcritical susceptibility. WheatstoneAlphaNumerical certifies
raw alpha in [-1.31505,-1.31495]. These canonical modules are included in 863.
