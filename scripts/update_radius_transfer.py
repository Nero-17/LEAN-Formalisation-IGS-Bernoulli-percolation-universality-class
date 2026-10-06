from pathlib import Path
p=Path('scratch/RadiusPointTransfer.lean');t=p.read_text(encoding='utf-8-sig').replace('import Universality.Percolation.RadiusPointLaw','import scratch.RadiusPointCounts')
old='\nend\nend Universality.Rule'
new='''
theorem Classical.internal_radius_point_expectation_le_limit {rule : Rule} (h : rule.Classical)
    {p : ℝ} (hp : 0 ≤ p) (hp' : p ≤ 1) (radius n : ℕ) :
    (((rule.edges : ℝ) - 1) / ((rule.vertices : ℝ) - 2)) *
      ((rule.generation n).network.expectedInternalRadiusPointRootCount p radius /
        (rule.edges : ℝ) ^ (n + 1)) ≤ rule.limitingRootRadiusProbability p radius := by
  rw [FiniteNetwork.expectedInternalRadiusPointRootCount_eq_difference]
  exact h.internal_radius_point_partial_sum_le_limit hp hp' radius n

end
end Universality.Rule'''
t=t.replace(old,new);p.write_text(t,encoding='utf-8')
