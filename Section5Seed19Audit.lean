import Universality.Section5.Seed19
import Universality.Section5.HausdorffDimensions

#print axioms Universality.Section5.exactAllocationBase19
#print axioms Universality.Section5.certifiedRule19_responses
#print axioms Universality.Section5.ExactAllocationCertificate.actual_growth_limits
#print axioms Universality.Section5.RuleResponses.hausdorff_dimension

example : Universality.Section5.certifiedRule19.Classical :=
  Universality.Section5.certifiedRule19_responses.classical

example : dimH (Set.univ : Set (Universality.Rule.GenerationMetricSpace
    Universality.Section5.certifiedRule19_responses.classical)) = ENNReal.ofReal (58 / 25) :=
  Universality.Section5.certifiedRule19_responses.hausdorff_dimension (by norm_num)
