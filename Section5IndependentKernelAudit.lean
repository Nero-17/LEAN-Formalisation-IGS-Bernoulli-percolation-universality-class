import Universality.Percolation.Section5ProductDisintegration
import Universality.Section5.WheatstoneMassKernels
import Universality.Section5.AllocationMatrices
import Universality.Certificates.Section5InitialSums

/-! Independent re-audit of the 21 reviewer-authored boundaries.
No nonlogical external axiom is expected in this list. -/

#print axioms Universality.finite_dependent_product_local_moment
#print axioms Universality.FiniteNetwork.heterogeneous_coarse_fiber_cell_moment
#print axioms Universality.FiniteNetwork.heterogeneous_coarse_fiber_conditional_response
#print axioms Universality.FiniteNetwork.heterogeneous_coarse_cell_expectation
#print axioms Universality.Section5.wheatstone_slot_conditional_response
#print axioms Universality.Section5.wheatstone_mass_kernel_aggregation
#print axioms Universality.Section5.allocatedExpression_matrixResponse
#print axioms Universality.Section5.allocatedExpression_matrixResponse_ordered_sum
#print axioms Universality.Section5.addressWeight_eq_wordProduct
#print axioms Universality.Section5.K3real_massPlaneBlock
#print axioms Universality.Section5.J3real_massPlaneBlock
#print axioms Universality.Section5.K3real_massPlaneLift
#print axioms Universality.Section5.J3real_massPlaneLift
#print axioms Universality.Section5.wordProduct_massPlaneLift
#print axioms Universality.Certificates.fixedZeroWords_length
#print axioms Universality.Certificates.fixedZeroLexRank_range
#print axioms Universality.Certificates.initialAllocation_fixed_zero_sum
#print axioms Universality.Certificates.lexPrefixWordSum_split
#print axioms Universality.Certificates.sum_grouped_zeroCount
#print axioms Universality.Certificates.initialAllocation_grouped_moment
#print axioms Universality.Certificates.initialAllocation_ordered_word_sum

#check Universality.FiniteNetwork.heterogeneous_coarse_cell_expectation
#check Universality.Section5.wheatstone_mass_kernel_aggregation
#check Universality.Section5.allocatedExpression_matrixResponse_ordered_sum
#check Universality.Section5.wordProduct_massPlaneLift
#check Universality.Certificates.initialAllocation_grouped_moment
#check Universality.Certificates.initialAllocation_ordered_word_sum

namespace Universality.Section5IndependentReview
open Matrix Certificates

/-- An order reversal is numerically detectable for the actual numerator kernels. -/
theorem numerator_order_witness :
    wordProduct outerKernelNumerator centralKernelNumerator [false, true] 0 0 = 252 ∧
    wordProduct outerKernelNumerator centralKernelNumerator [true, false] 0 0 = 258 := by
  constructor <;>
    norm_num [wordProduct, outerKernelNumerator, centralKernelNumerator,
      Matrix.mul_apply, Fin.sum_univ_two]

/-- The first fixed-zero prefix is false-then-true, with the outer kernel on the left. -/
theorem two_letter_prefix_order {R : Type*} [Semiring R] (outer central : R) :
    lexPrefixWordSum outer central 2 1 1 = outer * central ∧
    lexPrefixWordSum outer central 2 1 2 = outer * central + central * outer := by
  simp [lexPrefixWordSum, fixedZeroWords, binaryWords, zeroCount, fixedZeroLexRank,
    firstZeroWordCount, binomialByRatio, wordProduct]

end Universality.Section5IndependentReview
