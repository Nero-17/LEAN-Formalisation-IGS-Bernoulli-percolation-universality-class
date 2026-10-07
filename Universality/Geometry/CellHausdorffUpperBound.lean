import Universality.Geometry.CompactCellTree
import Mathlib.Topology.MetricSpace.HausdorffDimension

namespace Universality.Geometry.CompactCellTree
noncomputable section
open Set Filter Metric MeasureTheory MeasureTheory.Measure
open scoped Topology ENNReal NNReal
variable {X : Type*} [MetricSpace X] [MeasurableSpace X] [BorelSpace X] (tree : CompactCellTree X)

theorem hausdorffMeasure_limit_le_liminf (dimension : ℝ) (hdimension : 0 ≤ dimension) :
    MeasureTheory.Measure.hausdorffMeasure dimension tree.limit ≤
      liminf (fun n : ℕ => (Fintype.card (tree.Node n) : ℝ≥0∞) *
        ENNReal.ofReal (tree.ratio ^ n * tree.diameterBound) ^ dimension) atTop := by
  have hshrink : Tendsto (fun n : ℕ => ENNReal.ofReal (tree.ratio ^ n * tree.diameterBound))
      atTop (𝓝 0) := by
    simpa only [Function.comp_def, zero_mul, ENNReal.ofReal_zero] using ENNReal.continuous_ofReal.tendsto
      (0 * tree.diameterBound) |>.comp
        ((tendsto_pow_atTop_nhds_zero_of_lt_one tree.ratio_nonneg tree.ratio_lt_one).mul_const
          tree.diameterBound)
  calc
    _ ≤ liminf (fun n => ∑ w : tree.Node n, ediam (tree.cell n w) ^ dimension) atTop :=
      hausdorffMeasure_le_liminf_sum dimension tree.limit _ hshrink tree.cell
        (Eventually.of_forall (fun n w => ediam_le_of_forall_dist_le (tree.shrinking n w)))
        (Eventually.of_forall (fun n => iInter_subset tree.level n))
    _ ≤ _ := by
      refine liminf_le_liminf ?_
      filter_upwards [] with n
      calc
        _ ≤ ∑ _w : tree.Node n, ENNReal.ofReal (tree.ratio ^ n * tree.diameterBound) ^ dimension := by
          apply Finset.sum_le_sum
          intro w _
          exact ENNReal.rpow_le_rpow (ediam_le_of_forall_dist_le (tree.shrinking n w)) hdimension
        _ = _ := by simp

/-- Exponentially many geometrically shrinking cells have zero Hausdorff
measure at every exponent for which the covering contents decrease. -/
theorem hausdorffMeasure_limit_eq_zero_of_geometric_cover
    (branching : ℕ) (hcard : ∀ n, Fintype.card (tree.Node n) ≤ branching ^ n)
    (dimension : ℝ) (hdimension : 0 ≤ dimension)
    (hdecrease : (branching : ℝ≥0∞) * ENNReal.ofReal tree.ratio ^ dimension < 1) :
    MeasureTheory.Measure.hausdorffMeasure dimension tree.limit = 0 := by
  have hbound (n : ℕ) :
      (Fintype.card (tree.Node n) : ℝ≥0∞) *
        ENNReal.ofReal (tree.ratio ^ n * tree.diameterBound) ^ dimension ≤
      ((branching : ℝ≥0∞) * ENNReal.ofReal tree.ratio ^ dimension) ^ n *
        ENNReal.ofReal tree.diameterBound ^ dimension := by
    calc
      _ ≤ (branching : ℝ≥0∞) ^ n *
          ENNReal.ofReal (tree.ratio ^ n * tree.diameterBound) ^ dimension := by
        apply mul_le_mul_left
        exact_mod_cast hcard n
      _ = _ := by
        rw [ENNReal.ofReal_mul (pow_nonneg tree.ratio_nonneg n),
          ENNReal.ofReal_pow tree.ratio_nonneg,
          ENNReal.mul_rpow_of_nonneg _ _ hdimension,
          ← ENNReal.rpow_natCast_mul, mul_comm (n : ℝ) dimension,
          ENNReal.rpow_mul_natCast, mul_pow, mul_assoc]
  have hlimit : Tendsto (fun n : ℕ =>
      ((branching : ℝ≥0∞) * ENNReal.ofReal tree.ratio ^ dimension) ^ n *
        ENNReal.ofReal tree.diameterBound ^ dimension) atTop (𝓝 0) := by
    simpa only [zero_mul] using
      ENNReal.Tendsto.mul_const (ENNReal.tendsto_pow_atTop_nhds_zero_of_lt_one hdecrease)
        (Or.inr (ENNReal.rpow_ne_top_of_nonneg hdimension ENNReal.ofReal_ne_top))
  apply le_antisymm _ bot_le
  calc
    _ ≤ _ := tree.hausdorffMeasure_limit_le_liminf dimension hdimension
    _ ≤ liminf (fun n : ℕ =>
        ((branching : ℝ≥0∞) * ENNReal.ofReal tree.ratio ^ dimension) ^ n *
          ENNReal.ofReal tree.diameterBound ^ dimension) atTop :=
      liminf_le_liminf (Eventually.of_forall hbound)
    _ = 0 := hlimit.liminf_eq
/-- The Hausdorff dimension of the compact limit is bounded by the logarithmic
cell-count rate. This is a statement about `dimH`, not box
dimension or finite vertex growth. -/
theorem dimH_limit_le_log_branching_div_neg_log_ratio
    (branching : ℕ) (hbranching : 0 < branching)
    (hcard : ∀ n, Fintype.card (tree.Node n) ≤ branching ^ n)
    (hratio : 0 < tree.ratio) :
    dimH tree.limit ≤
      ENNReal.ofReal (Real.log (branching : ℝ) / (-Real.log tree.ratio)) := by
  apply dimH_le
  intro dimension htop
  by_contra hnot
  have hreal : Real.log (branching : ℝ) / (-Real.log tree.ratio) < (dimension : ℝ) := by
    by_contra hle
    apply hnot
    have hle' := ENNReal.ofReal_le_ofReal (le_of_not_gt hle)
    simpa only [ENNReal.ofReal_coe_nnreal] using hle'
  have hratioLog : Real.log tree.ratio < 0 := Real.log_neg hratio tree.ratio_lt_one
  have hlogInequality : Real.log (branching : ℝ) + Real.log tree.ratio * dimension < 0 := by
    have hmul := (div_lt_iff₀ (neg_pos.mpr hratioLog)).mp hreal
    nlinarith
  have hbranchingReal : 0 < (branching : ℝ) := by exact_mod_cast hbranching
  have hdecreaseReal : (branching : ℝ) * tree.ratio ^ (dimension : ℝ) < 1 := by
    calc
      _ = Real.exp (Real.log (branching : ℝ) + Real.log tree.ratio * dimension) := by
        rw [Real.exp_add, Real.exp_log hbranchingReal, Real.rpow_def_of_pos hratio]
      _ < 1 := Real.exp_lt_one_iff.mpr hlogInequality
  have hdecrease : (branching : ℝ≥0∞) * ENNReal.ofReal tree.ratio ^ (dimension : ℝ) < 1 := by
    have h := ENNReal.ofReal_lt_ofReal_iff (show (0 : ℝ) < 1 by norm_num) |>.mpr hdecreaseReal
    simpa only [ENNReal.ofReal_one, ENNReal.ofReal_mul hbranchingReal.le,
      ENNReal.ofReal_natCast, ENNReal.ofReal_rpow_of_nonneg tree.ratio_nonneg dimension.coe_nonneg] using h
  have hzero := tree.hausdorffMeasure_limit_eq_zero_of_geometric_cover branching hcard
    dimension dimension.coe_nonneg hdecrease
  rw [htop] at hzero
  exact ENNReal.top_ne_zero hzero

end
end Universality.Geometry.CompactCellTree
#print axioms Universality.Geometry.CompactCellTree.hausdorffMeasure_limit_le_liminf
#print axioms Universality.Geometry.CompactCellTree.hausdorffMeasure_limit_eq_zero_of_geometric_cover
#print axioms Universality.Geometry.CompactCellTree.dimH_limit_le_log_branching_div_neg_log_ratio