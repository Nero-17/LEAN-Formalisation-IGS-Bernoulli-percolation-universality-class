import Universality.Section5.HausdorffDimensions
import Universality.Certificates.Section5CheckpointBoolean
import Universality.Section5.ThreeSeedConsequences
import Universality.Certificates.Section5GroupChecks
import Universality.Certificates.Section5MassCertificate
import Universality.Section5.FourExponentialsObstruction
import Universality.Section5.CertificateConsequences
import Universality.Section5.CertificateMassBridge
import Universality.Section5.GrowthDimensions
import Universality.Section5.DimensionSpan
import Universality.Section5.ScaleIndependence
import Universality.Section5.HeterogeneousReliability
import Universality.Section5.WheatstoneResponse
import Universality.Section5.HeterogeneousFullConnectivity
import Universality.Percolation.Section5ProductDisintegration
import Universality.Section5.WheatstoneMassKernels
import Universality.Section5.HeterogeneousMass
import Universality.Section5.WheatstoneMass
import Universality.Section5.WheatstoneGrammar
import Universality.Section5.AllocationMatrices
import Universality.Graph.Section5AllocationDistance
import Universality.Percolation.Section5Critical
import Universality.Certificates.Section5InitialSums

/-! Independent review audit. The only permitted external mathematical axiom
in this list is Gelfond--Schneider, for the transcendence results alone. -/

#print axioms Universality.Section5.RuleResponses.mul
#print axioms Universality.Section5.compositionFamily_responses
#print axioms Universality.Section5.RuleResponses.spectralRadius
#print axioms Universality.Section5.compositionFamily_incommensurate
#print axioms Universality.Section5.RuleResponses.dimensions
#print axioms Universality.Section5.RuleResponses.actual_growth_limits
#print axioms Universality.Section5.RuleResponses.crossing_transition
#print axioms Universality.Section5.compositionFamily_infinite
#print axioms Universality.Section5.four_exponent_values
#print axioms Universality.Section5.three_scale_logs_independent
#print axioms Universality.Section5.three_actual_scale_logs_independent
#print axioms Universality.Section5.shifted_log_ratio_irrational
#print axioms Universality.Section5.shifted_three_dimensions_transcendental
#print axioms Universality.Section5.shifted_dimensions_proportional
#print axioms Universality.Section5.shifted_dimensions_span_rank
#print axioms Universality.Section5.shifted_dimensions_with_one_span_rank
#print axioms Universality.FiniteNetwork.heterogeneousSubstitutedReachable_iff
#print axioms Universality.FiniteNetwork.heterogeneousSubstitutedReachable_iff_active
#print axioms Universality.FiniteNetwork.heterogeneousSubstitute_crosses
#print axioms Universality.FiniteNetwork.heterogeneousSubstitute_reliability
#print axioms Universality.FiniteNetwork.heterogeneousSubstitute_all_vertices_connected
#print axioms Universality.Section5.wheatstoneCrossingPatterns_exact
#print axioms Universality.Section5.wheatstoneProbabilityResponse_exact
#print axioms Universality.Section5.wheatstoneRule_edges
#print axioms Universality.Section5.wheatstoneRule_reliability
#print axioms Universality.Section5.wheatstoneRule_fixed_half

-- Expose the hypotheses in the emitted audit, so existential status is visible.
#check Universality.Section5.RuleResponses
#check Universality.Section5.compositionFamily_infinite
#check Universality.Section5.RuleResponses.actual_growth_limits
#check Universality.Section5.wheatstoneRule_reliability

-- Author checks: this disintegration module was implemented by the reviewer
-- after completing the independent review above, and is not independently reviewed here.
#print axioms Universality.finite_dependent_product_local_moment
#print axioms Universality.FiniteNetwork.heterogeneous_coarse_fiber_cell_moment
#print axioms Universality.FiniteNetwork.heterogeneous_coarse_fiber_conditional_response
#print axioms Universality.FiniteNetwork.heterogeneous_coarse_cell_expectation
#check Universality.FiniteNetwork.heterogeneous_coarse_cell_expectation
#print axioms Universality.Section5.wheatstone_slot_conditional_response
#print axioms Universality.Section5.wheatstone_mass_kernel_aggregation
#check Universality.Section5.wheatstone_mass_kernel_aggregation

-- Independent review of the subsequent actual graph transport and grammar.
#print axioms Universality.FiniteNetwork.heterogeneousSubstitutedActive_cell
#print axioms Universality.FiniteNetwork.heterogeneousSubstitutedChildState_eq_local
#print axioms Universality.FiniteNetwork.heterogeneousSubstitute_liveCount
#print axioms Universality.FiniteNetwork.heterogeneousSubstitute_massMatrix_common
#print axioms Universality.Section5.wheatstoneRule_derivative_half
#print axioms Universality.Section5.singleEdgeNetwork_massMatrix
#print axioms Universality.Section5.WheatstoneExpression.fixed_half
#print axioms Universality.Section5.WheatstoneExpression.node_derivative
#print axioms Universality.Section5.allocatedExpression_fixed_half
#print axioms Universality.Section5.wheatstoneRule_massMatrix

-- Author checks for the ordered algebraic response and invariant-plane bridge.
#print axioms Universality.Section5.allocatedExpression_matrixResponse
#print axioms Universality.Section5.allocatedExpression_matrixResponse_ordered_sum
#print axioms Universality.Section5.addressWeight_eq_wordProduct
#print axioms Universality.Section5.K3real_massPlaneBlock
#print axioms Universality.Section5.J3real_massPlaneBlock
#print axioms Universality.Section5.K3real_massPlaneLift
#print axioms Universality.Section5.J3real_massPlaneLift
#print axioms Universality.Section5.wordProduct_massPlaneLift

-- Independent graph-agent boundary checks.
#print axioms Universality.FiniteNetwork.heterogeneousSubstitute_simple
#print axioms Universality.FiniteNetwork.heterogeneousSubstitute_cut
#print axioms Universality.FiniteNetwork.heterogeneousSubstitute_canonical
#print axioms Universality.Section5.wheatstoneTerminalInvolution
#print axioms Universality.Section5.wheatstoneRule_distance
#print axioms Universality.Section5.WheatstoneExpression.terminalProperties
#print axioms Universality.Section5.WheatstoneExpression.classical
#print axioms Universality.Section5.WheatstoneExpression.finite_crossing_transition_half
#print axioms Universality.Section5.allocatedExpression_distance
#print axioms Universality.Section5.allocation_distance
#print axioms Universality.Section5.allocatedExpression_classical

-- Author checks for exact lexicographic allocation sums.
#print axioms Universality.Certificates.fixedZeroWords_length
#print axioms Universality.Certificates.fixedZeroLexRank_range
#print axioms Universality.Certificates.initialAllocation_fixed_zero_sum
#print axioms Universality.Certificates.lexPrefixWordSum_split
#print axioms Universality.Certificates.sum_grouped_zeroCount
#print axioms Universality.Certificates.initialAllocation_grouped_moment
#print axioms Universality.Certificates.initialAllocation_ordered_word_sum

-- Independent review: exact integer numerator to actual mass response.
#print axioms Universality.Section5.allocation_massMatrix_integer_action
#print axioms Universality.Section5.allocation_massMatrix_eigenvector

-- Independent review: actual consequences retain exact certificate hypotheses.
#print axioms Universality.Section5.exactCertificates_infinite_growth_family
#print axioms Universality.Section5.ExactAllocationCertificate.actual_growth_limits
#print axioms Universality.Section5.ExactAllocationCertificate.shifted_dimensions
#print axioms Universality.Section5.ExactAllocationCertificate.shifted_dimensions_transcendental
#print axioms Universality.Section5.ExactAllocationCertificate.shifted_dimensions_span_ranks

-- Independent review: four-exponentials discussion is explicitly conditional.
#print axioms Universality.Section5.incommensurate_scale_logs_independent
#print axioms Universality.Section5.common_irrational_dimension_obstructs_four_exponentials
#print axioms Universality.Section5.four_exponentials_commensurability_of_common_irrational_dimension

-- Independent source review: cast, streaming invariant, and signed repairs.
#print axioms Universality.Certificates.groupedMassVector_cast
#print axioms Universality.Certificates.lexPrefixMassVector_cast
#print axioms Universality.Certificates.runLexMassStream_correct
#print axioms Universality.Certificates.initialMassEvaluation_correct
#print axioms Universality.Certificates.correctionTailVector_correct
#print axioms Universality.Certificates.correctionsMassEvaluation_correct
#print axioms Universality.Certificates.baselineMassEvaluation_correct

-- Author checks: exact packed arithmetic and final generic assembly.
#print axioms Universality.Certificates.packedInitialVector_extract
#print axioms Universality.Certificates.packedGroupedFromRow_correct
#print axioms Universality.Certificates.packedPreviousVector_correct
#print axioms Universality.Certificates.packedBinomialFromRow_correct
#print axioms Universality.Certificates.CompressedAllocation.mass_certificate

-- Independent review: actual three-seed consequences and linear group checker.
#print axioms Universality.Section5.ruleResponses_three_scale_logs_independent
#print axioms Universality.Section5.exactCertificates_three_rules
#print axioms Universality.Certificates.linearGroupCheck_correct
#print axioms Universality.Certificates.AllocationMomentCertificate.groupChecked_of_linear

-- Independent review: actual generation-metric Hausdorff dimension bridges.
#print axioms Universality.Section5.RuleResponses.hausdorff_dimension
#print axioms Universality.Section5.ExactAllocationCertificate.hausdorff_dimension
#print axioms Universality.Section5.ExactAllocationCertificate.shifted_hausdorff_dimension
#print axioms Universality.Section5.ExactAllocationCertificate.shifted_hausdorff_dimension_toReal
#print axioms Universality.Section5.ExactAllocationCertificate.shifted_hausdorff_dimension_transcendental

-- Independent review: all checkpoint fields and ordered state-list equality.
#print axioms Universality.Certificates.kernelPrefixBoolean_iff
#print axioms Universality.Certificates.lexMassStateBoolean_iff
#print axioms Universality.Certificates.lexMassStatesBoolean_iff
#print axioms Universality.Certificates.lexMassCheckpointBoolean_iff
#print axioms Universality.Certificates.runLexMassChunk_eq_of_boolean
