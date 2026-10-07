"""Emit literal binomial tables and group checks for actual allocation moments."""
from pathlib import Path
from math import comb
import json
import sys

sys.set_int_max_str_digits(0)
ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "supplementary" / "section5" / "certificates"

for folder, name in [("n424", "Base19"), ("n936", "Base661"),
                     ("n952", "Base739"), ("transcendental", "Shifted19")]:
    source = json.loads((SOURCE / folder / "word_base.json").read_bytes())
    depth, base = source["candidate"]["n"], source["candidate"]["s"]
    offset = source["candidate"]["ell"] - base ** 100
    content = f'''import Universality.Certificates.Section5NaturalMoments
import Universality.Certificates.Section5BinomialBoolean
import Universality.Certificates.Section5GroupChecks
import Universality.Certificates.Section5Distance
import Universality.Certificates.Section5Data{name}
import Universality.Certificates.Data.{name}

namespace Universality.Certificates

set_option maxHeartbeats 0
set_option maxRecDepth 100000
set_option exponentiation.threshold 4096

def allocation{name}AllCounts : BinomialTable where
  top := {depth}
  values := [{', '.join(str(comb(depth, i)) for i in range(depth+1))}]

def allocation{name}FirstCounts : BinomialTable where
  top := {depth-1}
  values := [{', '.join(str(comb(depth-1, i)) for i in range(depth))}]

def allocation{name}Moments : AllocationMomentCertificate where
  allocation := allocation{name}
  moments := certificate{name}
  allCounts := allocation{name}AllCounts
  firstCounts := allocation{name}FirstCounts

set_option maxHeartbeats 0
set_option maxRecDepth 100000
set_option exponentiation.threshold 4096

theorem allocation{name}_allCounts_valid : allocation{name}AllCounts.valid := by
  apply BinomialTable.valid_of_boolean <;> decide +kernel
#check allocation{name}_allCounts_valid
theorem allocation{name}_firstCounts_valid : allocation{name}FirstCounts.valid := by
  apply BinomialTable.valid_of_boolean <;> decide +kernel
#check allocation{name}_firstCounts_valid
theorem allocation{name}_groups_checked : allocation{name}Moments.groupChecked := by
  apply AllocationMomentCertificate.groupChecked_of_linear <;> decide +kernel
#check allocation{name}_groups_checked

theorem allocation{name}_length :
    2 ^ {depth} + allocation{name}.allocation (List.replicate {depth} false) =
      {base} ^ 100 + {offset} := by
  exact allocation{name}.length_certificate allocation{name}_capacityValid {base} {offset}
    (by decide +kernel)

theorem allocation{name}_volume :
    (5 : ℤ) ^ {depth} + 4 * ((binaryWords {depth}).map fun word =>
      (allocation{name}.allocation word : ℤ) * 2 ^ zeroCount word).sum = {base} ^ 232 :=
  allocation{name}Moments.volume_identity_at allocation{name} {depth} {base} rfl rfl rfl
    allocation{name}_capacityValid
    certificate{name}_integer_moments allocation{name}_allCounts_valid
    allocation{name}_firstCounts_valid allocation{name}_groups_checked

theorem allocation{name}_thermal :
    8 * (13 : ℤ) ^ {depth} + 5 * ((binaryWords {depth}).map fun word =>
      (allocation{name}.allocation word : ℤ) * 6 ^ zeroCount word).sum =
      8 ^ ({depth} + 1) * {base} ^ 70 :=
  allocation{name}Moments.thermal_identity_at allocation{name} {depth} {base} rfl rfl rfl
    allocation{name}_capacityValid
    certificate{name}_integer_moments allocation{name}_allCounts_valid
    allocation{name}_firstCounts_valid allocation{name}_groups_checked

theorem allocation{name}_volume_nat :
    5 ^ {depth} + 4 * ((binaryWords {depth}).map fun word =>
      allocation{name}.allocation word * 2 ^ zeroCount word).sum = {base} ^ 232 :=
  allocation{name}Moments.volume_identity_nat_at allocation{name} {depth} {base} rfl rfl rfl
    allocation{name}_capacityValid
    certificate{name}_integer_moments allocation{name}_allCounts_valid
    allocation{name}_firstCounts_valid allocation{name}_groups_checked

theorem allocation{name}_thermal_nat :
    8 ^ ({depth} + 1) * {base} ^ 70 =
      8 * 13 ^ {depth} + 5 * ((binaryWords {depth}).map fun word =>
        allocation{name}.allocation word * 6 ^ zeroCount word).sum :=
  allocation{name}Moments.thermal_identity_nat_at allocation{name} {depth} {base} rfl rfl rfl
    allocation{name}_capacityValid
    certificate{name}_integer_moments allocation{name}_allCounts_valid
    allocation{name}_firstCounts_valid allocation{name}_groups_checked

end Universality.Certificates
'''
    directory = ROOT / "Universality" / "Certificates"
    counts_content, remainder = content.split(f"def allocation{name}Moments", 1)
    moment_definition, remainder = (f"def allocation{name}Moments" + remainder).split(
        f"theorem allocation{name}_allCounts_valid", 1)
    count_proofs, remainder = (f"theorem allocation{name}_allCounts_valid" + remainder).split(
        f"theorem allocation{name}_groups_checked", 1)
    group_proof, identities = (f"theorem allocation{name}_groups_checked" + remainder).split(
        f"theorem allocation{name}_length", 1)
    (directory / f"Section5Counts{name}.lean").write_text(
        counts_content + count_proofs + "end Universality.Certificates\n", encoding="utf-8")
    (directory / f"Section5Groups{name}.lean").write_text(
        f"import Universality.Certificates.Section5Counts{name}\n\n"
        "namespace Universality.Certificates\n\n" + moment_definition + group_proof +
        "end Universality.Certificates\n", encoding="utf-8")
    endpoint_header = (f"import Universality.Certificates.Section5Groups{name}\n"
               "import Universality.Certificates.Section5LengthCertificate\n\n"
               "namespace Universality.Certificates\n\n"
               "set_option maxHeartbeats 0\nset_option maxRecDepth 100000\n"
               "set_option exponentiation.threshold 4096\n\n")
    length_body, responses = (f"theorem allocation{name}_length" + identities).split(
        f"theorem allocation{name}_volume", 1)
    (directory / f"Section5Length{name}.lean").write_text(
        endpoint_header + length_body + "end Universality.Certificates\n", encoding="utf-8")
    (directory / f"Section5Responses{name}.lean").write_text(
        "import Universality.Certificates.Section5MomentSpecialization\n" +
        endpoint_header.replace("set_option maxHeartbeats 0", "set_option maxHeartbeats 200000") +
        f"theorem allocation{name}_volume" + responses, encoding="utf-8")
    content = (f"import Universality.Certificates.Section5Length{name}\n"
               f"import Universality.Certificates.Section5Responses{name}\n")
    destination = directory / f"Section5Moments{name}.lean"
    destination.write_text(content, encoding="utf-8")
    print(destination.name, len(content))
