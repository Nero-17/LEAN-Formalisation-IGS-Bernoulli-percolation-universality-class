"""Emit separate kernel checks of streamed initial mass and final mass repair."""
from pathlib import Path
import json
import hashlib
import sys

sys.set_int_max_str_digits(0)
ROOT = Path(__file__).resolve().parents[1]
for folder, name in [("n424", "Base19"), ("n936", "Base661"),
                     ("n952", "Base739"), ("transcendental", "Shifted19")]:
    raw = (ROOT / "supplementary" / "section5" / "certificates" / folder / "word_base.json").read_bytes()
    source = json.loads(raw)
    depth, base = source["candidate"]["n"], source["candidate"]["s"]
    first, second = source["mass_vector_numerator"]
    initial = f'''import Universality.Certificates.Section5BitExtraction
import Universality.Certificates.Section5Input{name}

/-! Expected initial sum from the original word_base.json; it is not assumed
correct.  The equality below requires a full kernel evaluation of the actual
stream on the original allocation rows.
SHA256: {hashlib.sha256(raw).hexdigest()} -/

namespace Universality.Certificates

def allocation{name}InitialMass : ℕ × ℕ := ({first}, {second})

set_option maxHeartbeats 0 in
set_option maxRecDepth 100000 in
set_option exponentiation.threshold 10000 in
theorem allocation{name}_initialMassEvaluation :
    initialMassEvaluation {depth} allocation{name}.rows = allocation{name}InitialMass := by
  have checked : initialMassEvaluationBits {depth} allocation{name}.rows =
      allocation{name}InitialMass := by decide +kernel
  exact (initialMassEvaluationBits_eq {depth} allocation{name}.rows).symm.trans checked

#print axioms allocation{name}_initialMassEvaluation
end Universality.Certificates
'''
    final = f'''import Universality.Certificates.Section5InitialMass{name}
import Universality.Certificates.Section5Data{name}
import Universality.Certificates.Section5MassSpecialization

namespace Universality.Certificates
open Matrix

set_option maxHeartbeats 0 in
set_option maxRecDepth 100000 in
set_option exponentiation.threshold 10000 in
theorem allocation{name}_massRepairEvaluation :
    massEvaluationWithInitial {depth} allocation{name}.packets allocation{name}InitialMass =
      massCertificateValue {depth} {base} := by
  decide +kernel

#print axioms allocation{name}_massRepairEvaluation

theorem allocation{name}_mass :
    Section5.allocationMassNumerator {depth} allocation{name}.allocation *ᵥ
      (![55, 23] : Fin 2 → ℤ) =
      (16 ^ ({depth} + 1) * ({base} : ℤ) ^ 219) • (![55, 23] : Fin 2 → ℤ) :=
  allocation{name}.mass_certificate_at {depth} {base} rfl allocation{name}_capacityValid
    allocation{name}InitialMass allocation{name}_initialMassEvaluation
    allocation{name}_massRepairEvaluation

#print axioms allocation{name}_mass
end Universality.Certificates
'''
    # A complete chunk generator owns this endpoint once a manifest exists.
    # Regenerating scalar repair checks must not replace its bounded proof
    # chain with the earlier monolithic computational benchmark.
    chunk_manifest = ROOT / "docs" / f"section5-certificate-chunks-{name}.json"
    if not chunk_manifest.exists():
        (ROOT / "Universality" / "Certificates" / f"Section5InitialMass{name}.lean").write_text(initial, encoding="utf-8")
    (ROOT / "Universality" / "Certificates" / f"Section5Mass{name}.lean").write_text(final, encoding="utf-8")
    print(name, "mass digits", len(str(first)), len(str(second)))
