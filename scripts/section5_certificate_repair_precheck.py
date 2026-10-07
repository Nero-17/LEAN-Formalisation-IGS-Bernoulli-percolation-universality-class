"""Prepare independent final repair checks without waiting for stream proofs.

The numerical check is exactly the existing final mass check, specialized to
the original JSON's initial-sum literal. Its use for the actual allocation
still requires the complete initial stream theorem. No data, initial-mass,
chunk manifest, or already checked depth-424 module is changed.
"""

from pathlib import Path
import argparse
import hashlib
import json
import sys

from section5_receipt_closure import output_artifacts, snapshot_module

sys.set_int_max_str_digits(0)
ROOT = Path(__file__).resolve().parents[1]


def require_checked_module(relative, history):
    source_hash = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
    object_path = ROOT / ".lake" / "build" / "lib" / "lean" / Path(relative).with_suffix(".olean")
    if not object_path.is_file():
        raise ValueError(f"{relative}: repair object is absent")
    current_snapshot = snapshot_module(ROOT, relative)
    current_outputs = output_artifacts(ROOT, relative)
    for entry in reversed(history):
        if (entry["module"] == relative and entry["source_sha256"] == source_hash
                and entry["exit_code"] == 0 and entry["source_unchanged_during_check"]
                and entry.get("dependencies_unchanged_during_check")
                and entry.get("snapshot_before") == entry.get("snapshot_after") == current_snapshot
                and entry.get("output_artifacts") == current_outputs):
            return
    raise ValueError(f"{relative}: no successful strong receipt matches current source, dependencies and objects")


def require_checked_helper(name, history):
    manifest_path = ROOT / "docs" / f"section5-certificate-repair-chunks-{name}.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest["name"] != name:
            raise ValueError(f"{name}: repair manifest names another seed")
        # This includes the exact flattening, all thirty chunk checks, the
        # baseline/total checks and final repair assembly, not just its object.
        for entry in manifest["modules"]:
            relative = f"Universality/Certificates/{entry['module']}.lean"
            if hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() != entry["sha256"]:
                raise ValueError(f"{relative}: source differs from repair manifest")
            require_checked_module(relative, history)
    else:
        require_checked_module(f"Universality/Certificates/Section5MassRepair{name}.lean", history)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bridges", action="store_true",
                        help="after selected repair modules compile, replace their pending final mass assemblies")
    parser.add_argument("--name", action="append", choices=["Base661", "Base739"],
                        help="select one seed (repeatable); default requires both seeds")
    args = parser.parse_args()
    selected = args.name or ["Base661", "Base739"]
    if not args.bridges and any((ROOT / "docs" / f"section5-certificate-repair-chunks-{name}.json").exists()
                                for name in selected):
        parser.error("bounded repair manifests exist; preserve their proof assemblies and use section5_certificate_repair_chunks.py")
    if args.bridges:
        history = json.loads((ROOT / "docs" / "section5-certificate-kernel-checks.json").read_text(encoding="utf-8"))
        # Preflight every selected helper before changing any final assembly.
        for name in selected:
            require_checked_helper(name, history)
    for folder, name in [("n936", "Base661"), ("n952", "Base739")]:
        if name not in selected:
            continue
        raw = (ROOT / "supplementary" / "section5" / "certificates" / folder / "word_base.json").read_bytes()
        data = json.loads(raw)
        depth, base = data["candidate"]["n"], data["candidate"]["s"]
        first, second = data["mass_vector_numerator"]
        if args.bridges:
            content = f'''import Universality.Certificates.Section5InitialMass{name}
import Universality.Certificates.Section5Data{name}
import Universality.Certificates.Section5MassSpecialization
import Universality.Certificates.Section5MassRepair{name}

namespace Universality.Certificates
open Matrix

theorem allocation{name}_massRepairEvaluation :
    massEvaluationWithInitial {depth} allocation{name}.packets allocation{name}InitialMass =
      massCertificateValue {depth} {base} := by
  simpa only [allocation{name}InitialMass, allocation{name}RepairInitialMass] using
    allocation{name}_massRepairLiteral

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
            destination = ROOT / "Universality" / "Certificates" / f"Section5Mass{name}.lean"
        else:
            content = f'''import Universality.Certificates.Section5Input{name}
import Universality.Certificates.Section5MassCertificate

/-! The original initial-sum literal is checked against baseline plus all
signed packet repairs here. This arithmetic equality alone does not prove
that the allocation has that initial sum; the final mass assembly also
requires its independently checked complete stream theorem.
word_base.json SHA256: {hashlib.sha256(raw).hexdigest()} -/

namespace Universality.Certificates

set_option maxHeartbeats 0
set_option maxRecDepth 100000
set_option exponentiation.threshold 10000
set_option Elab.async false

def allocation{name}RepairInitialMass : ℕ × ℕ := ({first}, {second})

theorem allocation{name}_massRepairLiteral :
    massEvaluationWithInitial {depth} allocation{name}.packets allocation{name}RepairInitialMass =
      massCertificateValue {depth} {base} := by
  decide +kernel

#print axioms allocation{name}_massRepairLiteral
end Universality.Certificates
'''
            destination = ROOT / "Universality" / "Certificates" / f"Section5MassRepair{name}.lean"
        destination.write_text(content, encoding="utf-8")
        print(destination.relative_to(ROOT).as_posix(), hashlib.sha256(destination.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
