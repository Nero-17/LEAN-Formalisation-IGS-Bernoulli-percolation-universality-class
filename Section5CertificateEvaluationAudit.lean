import Universality.Certificates.Section5MassCertificate
import Universality.Certificates.Section5FastRank
import Universality.Certificates.Section5PacketChecks
import Universality.Certificates.Section5MomentSpecialization
import Universality.Certificates.Section5LengthCertificate
import Universality.Certificates.Section5BitExtraction

/-! Independent axiom audit of packed evaluation, scalar casts, packet repairs,
and final integer mass assembly. The streaming correctness dependency was
authored by this auditor and is not counted as independently reviewed here. -/

-- Packed extraction and inverse descent
#print axioms Universality.Certificates.packed_digit_extract
#print axioms Universality.Certificates.packedInitialVector_one_bound
#print axioms Universality.Certificates.packedInitialVector_eq_matrix
#print axioms Universality.Certificates.packed_grouped_matrix_sum
#print axioms Universality.Certificates.groupedMassVector_bound
#print axioms Universality.Certificates.matrixPackingBase_bound
#print axioms Universality.Certificates.ofDigits_map_range
#print axioms Universality.Certificates.list_sum_mulVec_apply
#print axioms Universality.Certificates.packedInitialVector_eq_ofDigits
#print axioms Universality.Certificates.packedInitialVector_extract_of_bound
#print axioms Universality.Certificates.packedInitialVector_extract
#print axioms Universality.Certificates.matrixPackingBase_global_bound
#print axioms Universality.Certificates.groupedMassVector_above_depth
#print axioms Universality.Certificates.packedGroupedVector_correct
#print axioms Universality.Certificates.packedPreviousVector_correct
#print axioms Universality.Certificates.packedGroupedFromRow_correct
#print axioms Universality.Certificates.packedBinomial_eq_ofDigits
#print axioms Universality.Certificates.packedBinomial_extract
#print axioms Universality.Certificates.packedBinomialFromRow_correct
#print axioms Universality.Certificates.packedBinomial_previous

-- Natural to integer casts
#print axioms Universality.Certificates.ringHom_wordProduct
#print axioms Universality.Certificates.ringHom_groupedWordSum
#print axioms Universality.Certificates.ringHom_lexPrefixWordSum
#print axioms Universality.Certificates.naturalOuterKernel_cast
#print axioms Universality.Certificates.naturalCentralKernel_cast
#print axioms Universality.Certificates.initialMassVector_cast
#print axioms Universality.Certificates.groupedWordSum_natural_cast
#print axioms Universality.Certificates.lexPrefixWordSum_natural_cast
#print axioms Universality.Certificates.groupedMassVector_cast
#print axioms Universality.Certificates.lexPrefixMassVector_cast

-- Signed packet repairs and baseline
#print axioms Universality.Certificates.integerKernelStep_correct
#print axioms Universality.Certificates.integerKernelPower_correct
#print axioms Universality.Certificates.correctionTailVector_correct
#print axioms Universality.Certificates.correctionMassEvaluation_correct
#print axioms Universality.Certificates.integerPairVector_add
#print axioms Universality.Certificates.correctionsMassEvaluation_correct
#print axioms Universality.Certificates.baselineMassVector_correct
#print axioms Universality.Certificates.baselineMassEvaluation_correct

-- Final integer mass assembly
#print axioms Universality.Certificates.list_matrix_sum_mulVec
#print axioms Universality.Certificates.integerIncrement_vector
#print axioms Universality.Certificates.CompressedAllocation.mass_numerator_decomposition
#print axioms Universality.Certificates.initialOrderedMass_natCast
#print axioms Universality.Certificates.integerPairVector_massCertificateValue
#print axioms Universality.Certificates.CompressedAllocation.mass_certificate_from_initial
#print axioms Universality.Certificates.initialMassEvaluation_integer_correct
#print axioms Universality.Certificates.CompressedAllocation.mass_certificate

-- Optimized rank and packet capacity checking.
#print axioms Universality.Certificates.fastBinomial_eq_choose
#print axioms Universality.Certificates.fastFixedZeroLexRankAux_correct
#print axioms Universality.Certificates.fastFixedZeroLexRank_correct
#print axioms Universality.Certificates.fastInitialAllocation_correct
#print axioms Universality.Certificates.CorrectionPacket.fastCapacityCheck_iff
#print axioms Universality.Certificates.allocationPacketsCheck_correct
#print axioms Universality.Certificates.ordinaryPacketExceptionCheck_correct
#print axioms Universality.Certificates.allocationPacketsCheck_ordinary_correct
#print axioms Universality.Certificates.CorrectionPacket.fastZeros_correct
#print axioms Universality.Certificates.allocationPacketsCheckFast_correct

-- Explicit scalar specialization and all-zero length certificate.
#print axioms Universality.Certificates.AllocationMomentCertificate.volume_identity_nat_at
#print axioms Universality.Certificates.AllocationMomentCertificate.thermal_identity_nat_at
#print axioms Universality.Certificates.AllocationMomentCertificate.volume_identity_at
#print axioms Universality.Certificates.AllocationMomentCertificate.thermal_identity_at
#print axioms Universality.Certificates.CompressedAllocation.length_certificate

-- Separate bit extraction implementation; production evaluator is unchanged.
#print axioms Universality.Certificates.packedBitDigit_eq
#print axioms Universality.Certificates.packedGroupedBits_eq
#print axioms Universality.Certificates.packedBinomialBits_eq
#print axioms Universality.Certificates.runLexMassBitStream_eq
#print axioms Universality.Certificates.initialFloorMassBits_eq
#print axioms Universality.Certificates.initialMassEvaluationBits_eq

#check Universality.Certificates.packedInitialVector_extract_of_bound
#check Universality.Certificates.packedPreviousVector_correct
#check Universality.Certificates.packedGroupedFromRow_correct
#check Universality.Certificates.packedBinomialFromRow_correct
#check Universality.Certificates.CompressedAllocation.mass_certificate
#check Universality.Certificates.fastFixedZeroLexRankAux_correct
#check Universality.Certificates.CorrectionPacket.fastCapacityCheck_iff
#check Universality.Certificates.allocationPacketsCheck_correct
#check Universality.Certificates.allocationPacketsCheckFast_correct

namespace Universality.Section5CertificateEvaluationReview
open Matrix Certificates Section5

/-- The checked finite evaluator binds to the original mass matrix of the
actual allocated graph, while both numerical equalities remain explicit. -/
theorem checked_evaluation_actual_mass (certificate : CompressedAllocation)
    (checked : certificate.capacityValid) (base : ℕ) (initialValue : ℕ × ℕ)
    (initial_checked : initialMassEvaluation certificate.depth certificate.rows = initialValue)
    (numerical_checked : massEvaluationWithInitial certificate.depth certificate.packets initialValue =
      massCertificateValue certificate.depth base) :
    (allocatedExpression certificate.depth (allocationDecoration certificate.allocation)).rule.network.massMatrix
        (1 / 2) *ᵥ certificateWeight = (base : ℝ) ^ 219 • certificateWeight := by
  apply allocation_massMatrix_eigenvector certificate.depth base certificate.allocation
  · intro word member
    exact certificate.allocation_capacity checked word (word_length_of_mem_binaryWords member)
  · exact certificate.mass_certificate checked base initialValue initial_checked numerical_checked

#print axioms checked_evaluation_actual_mass

/-- The independently checked bit evaluator satisfies the same actual graph
endpoint, retaining both explicit finite numerical equalities. -/
theorem checked_bit_evaluation_actual_mass (certificate : CompressedAllocation)
    (checked : certificate.capacityValid) (base : ℕ) (initialValue : ℕ × ℕ)
    (initial_checked : initialMassEvaluationBits certificate.depth certificate.rows = initialValue)
    (numerical_checked : massEvaluationWithInitial certificate.depth certificate.packets initialValue =
      massCertificateValue certificate.depth base) :
    (allocatedExpression certificate.depth (allocationDecoration certificate.allocation)).rule.network.massMatrix
        (1 / 2) *ᵥ certificateWeight = (base : ℝ) ^ 219 • certificateWeight := by
  apply checked_evaluation_actual_mass certificate checked base initialValue
  · rw [← initialMassEvaluationBits_eq]
    exact initial_checked
  · exact numerical_checked

#print axioms checked_bit_evaluation_actual_mass

end Universality.Section5CertificateEvaluationReview
