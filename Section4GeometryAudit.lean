import Universality.Arithmetic.Section4Geometry
import Universality.Geometry.CellHausdorffUpperBound
import Section4KernelAudit

/-! Complete Section 4 arithmetic and actual compact metric geometry audit.
This command checks every project declaration in the imported closure. -/

#audit_section4_axioms

#print axioms Universality.Rule.generationMetricSpace_dimH_eq
#print axioms Universality.Rule.Classical.criticalDimensions_ambient_hausdorff
#print axioms Universality.Rule.Classical.criticalDimensions_geometric_finite_growth
#print axioms Universality.Geometry.SymbolicHausdorff.logarithmic_dimension_le_of_separation
#print axioms Universality.Geometry.SeparatedSimilarities.logarithmic_dimension_le
#print axioms Universality.Geometry.SeparatedBlocks.integer_scale_dimension_le
#print axioms Universality.Geometry.IsometricSequence.completionCell_dist
#print axioms Universality.Geometry.exists_internal_similarity
#print axioms Universality.logarithmic_dimension_le_of_block_bounds