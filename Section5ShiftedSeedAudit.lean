import Universality.Section5.SeedShifted19
import Universality.Section5.HausdorffDimensions

#print axioms Universality.Section5.exactAllocationShifted19
#print axioms Universality.Section5.certifiedRuleShifted19_classical
#print axioms Universality.Section5.certifiedRuleShifted19_transcendental_dimensions

example : Transcendental ℚ (dimH (Set.univ : Set
    (Universality.Rule.GenerationMetricSpace
      Universality.Section5.certifiedRuleShifted19_classical))).toReal :=
  Universality.Section5.exactAllocationShifted19.shifted_hausdorff_dimension_transcendental

example := Universality.Section5.exactAllocationShifted19.shifted_dimensions_span_ranks
