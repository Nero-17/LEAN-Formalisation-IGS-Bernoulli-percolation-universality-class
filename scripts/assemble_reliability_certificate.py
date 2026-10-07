from pathlib import Path
from math import comb
root=Path(__file__).resolve().parents[1]
counts=[0,0,0,5,54,251,660,1056,1036,661,281,78,13,1]
coefficients=[sum(counts[k]*comb(13-k,j-k)*(-1)**(j-k) for k in range(j+1)) for j in range(14)]
expression=' + '.join(f'({coefficient}) * X ^ {degree}' for degree,coefficient in enumerate(coefficients) if coefficient)
imports='\n'.join(f'import Universality.Certificates.Opposite.Crossing{i:02d}' for i in range(64))
batchproofs=',\n      '.join(f'oppositeRows{i:02d}_crossing' for i in range(64))
proofs='\n'.join(f'  have h{i} : oppositeWheatstoneNetwork.crossingCountBySize {i} = {counts[i]} := oppositeWheatstone_crossing_counts_by_size ({i} : Fin 14)' for i in range(14))
text=f'''{imports}
import Universality.Percolation.OppositeWheatstoneCounts
import Universality.Percolation.ReliabilityDerivative

namespace Universality
open FiniteNetwork Polynomial

def oppositeWheatstoneCrossingTable : Fin 14 → ℕ := ![{','.join(map(str,counts))}]

set_option maxHeartbeats 2000000 in
theorem oppositeWheatstone_crossing_counts_by_size (size : Fin 14) :
    oppositeWheatstoneNetwork.crossingCountBySize size.val = oppositeWheatstoneCrossingTable size := by
  rw [← certified_crossingCountBySize oppositeWheatstoneNetwork oppositeComponentRows
    oppositeComponentRows_indices oppositeComponentRows_valid]
  simp only [oppositeComponentRows, List.map_append, List.sum_append,
      {batchproofs}]
  fin_cases size <;> rfl

theorem oppositeWheatstone_reliabilityPolynomial :
    oppositeWheatstoneNetwork.reliabilityPolynomial = {expression} := by
  rw [reliabilityPolynomial_bernstein]
{proofs}
  norm_num [Finset.sum_range_succ, {', '.join(f'h{i}' for i in range(14))}]
  ring

theorem oppositeWheatstone_thermal_derivative :
    oppositeWheatstoneNetwork.reliabilityPolynomial.derivative.eval₂ (Rat.castHom ℝ) (1 / 2) =
      (67 / 32 : ℝ) := by
  rw [oppositeWheatstone_reliabilityPolynomial]
  norm_num [Polynomial.derivative_mul, Polynomial.derivative_sub,
    Polynomial.derivative_add, Polynomial.derivative_X_pow]

theorem oppositeWheatstone_deriv_half :
    deriv oppositeWheatstoneNetwork.reliability (1 / 2) = 67 / 32 := by
  have h := oppositeWheatstoneNetwork.hasDerivAt_reliability (1 / 2)
  rw [oppositeWheatstone_thermal_derivative] at h
  exact h.deriv

end Universality
'''
(root/'Universality'/'Percolation'/'OppositeWheatstoneReliability.lean').write_text(text,encoding='utf-8')
print(expression)
