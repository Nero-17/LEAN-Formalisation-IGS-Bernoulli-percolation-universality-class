"""Independently compare emitted Lean allocation literals with the original JSON.

This audit does not import the generator and makes no claim to replace Lean.
It checks that stronger auxiliary slacks have not altered the allocation.
"""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import re
import sys
from math import comb
from section5_certificate_proof_split import OVERLAY, SOURCE, ORIGINAL_SHA256, validate_overlay

sys.set_int_max_str_digits(0)
ROOT = Path(__file__).resolve().parents[1]
checked_at = datetime.now().astimezone().isoformat(timespec="seconds")
records = []
if (ROOT / OVERLAY).exists():
    proof_split = validate_overlay(ROOT)
else:
    assert hashlib.sha256((ROOT / SOURCE).read_bytes()).hexdigest() == ORIGINAL_SHA256
    proof_split = None
for folder, name in [("n424", "Base19"), ("n936", "Base661"),
                     ("n952", "Base739"), ("transcendental", "Shifted19")]:
    source = ROOT / "supplementary" / "section5" / "certificates" / folder
    raw_base = (source / "word_base.json").read_bytes()
    raw_packet = (source / "packet_repair.json").read_bytes()
    base, packet = json.loads(raw_base), json.loads(raw_packet)
    lean_path = ROOT / "Universality" / "Certificates" / f"Section5Input{name}.lean"
    lean = lean_path.read_text(encoding="utf-8")
    rows_text = lean.split("  rows := [", 1)[1].split("  slacks := [", 1)[0]
    packets_text = lean.split("  packets := [", 1)[1].split("end Universality", 1)[0]
    rows = [tuple(map(int, row)) for row in re.findall(r"⟨(\d+), (\d+), (\d+)⟩", rows_text)]
    expected_rows = [(*floors, remainder) for floors, remainder in
                     zip(base["floor_groups"], base["lex_remainders"])]
    assert rows == expected_rows
    lean_packets = [(int(layer), first == "true", repeated == "true", int(remaining), int(coefficient))
                    for layer, first, repeated, remaining, coefficient in re.findall(
                        r"⟨(\d+), (false|true), (false|true), (\d+), (-?\d+)⟩", packets_text)]
    expected_packets = []
    for layer in packet["layers"]:
        assert layer["h"] == 2 * layer["t"] + 1
        assert layer["suffix_length"] + 2 * layer["h"] == base["candidate"]["n"]
        expected_packets.extend((layer["t"], first, repeated, layer["suffix_length"] - 2, coefficient)
                                for (first, repeated), coefficient in zip(
                                    [(False, False), (True, False), (True, True), (False, True)],
                                    layer["coefficients"]))
    assert lean_packets == expected_packets
    for data, filename in [(raw_base, "word_base.json"), (raw_packet, "packet_repair.json")]:
        assert f"{filename} SHA256: {hashlib.sha256(data).hexdigest()}" in lean
    assert f"  depth := {base['candidate']['n']}" in lean
    depth = base["candidate"]["n"]
    moments_path = ROOT / "Universality" / "Certificates" / f"Section5Moments{name}.lean"
    counts_path = ROOT / "Universality" / "Certificates" / f"Section5Counts{name}.lean"
    counts = counts_path.read_text(encoding="utf-8")
    count_lists = re.findall(r"  values := \[([^\]]*)\]", counts)
    assert len(count_lists) == 2
    assert [int(value) for value in count_lists[0].split(",")] == [comb(depth, zeros) for zeros in range(depth + 1)]
    assert [int(value) for value in count_lists[1].split(",")] == [comb(depth - 1, zeros) for zeros in range(depth)]
    mass_path = ROOT / "Universality" / "Certificates" / f"Section5InitialMass{name}.lean"
    mass = mass_path.read_text(encoding="utf-8")
    expected_pair = re.search(r"InitialMass : ℕ × ℕ := \((\d+), (\d+)\)", mass)
    assert expected_pair is not None
    assert tuple(map(int, expected_pair.groups())) == tuple(base["mass_vector_numerator"])
    assert hashlib.sha256(raw_base).hexdigest() in mass
    final_mass_path = ROOT / "Universality" / "Certificates" / f"Section5Mass{name}.lean"
    final_mass = final_mass_path.read_text(encoding="utf-8")
    final_body = final_mass.split(f"theorem allocation{name}_mass :", 1)[1]
    final_body = final_body.split(f"#print axioms allocation{name}_mass", 1)[0]
    expected_final_body = f"""
    Section5.allocationMassNumerator {depth} allocation{name}.allocation *ᵥ
      (![55, 23] : Fin 2 → ℤ) =
      (16 ^ ({depth} + 1) * ({base['candidate']['s']} : ℤ) ^ 219) • (![55, 23] : Fin 2 → ℤ) :=
  allocation{name}.mass_certificate_at {depth} {base['candidate']['s']} rfl allocation{name}_capacityValid
    allocation{name}InitialMass allocation{name}_initialMassEvaluation
    allocation{name}_massRepairEvaluation
"""
    assert " ".join(final_body.split()) == " ".join(expected_final_body.split())
    repair_body = final_mass.split(f"theorem allocation{name}_massRepairEvaluation :", 1)[1]
    repair_body = repair_body.split(f"#print axioms allocation{name}_massRepairEvaluation", 1)[0]
    expected_repair_type = f"""
    massEvaluationWithInitial {depth} allocation{name}.packets allocation{name}InitialMass =
      massCertificateValue {depth} {base['candidate']['s']} := by
"""
    expected_bounded_repair = expected_repair_type + f"""
  simpa only [allocation{name}InitialMass, allocation{name}RepairInitialMass] using
    allocation{name}_massRepairLiteral
"""
    expected_direct_repair = expected_repair_type + "  decide +kernel\n"
    repair_data_sha256 = None
    if " ".join(repair_body.split()) == " ".join(expected_bounded_repair.split()):
        assert f"import Universality.Certificates.Section5MassRepair{name}" in final_mass
        repair_data_path = ROOT / "Universality" / "Certificates" / f"Section5MassRepairData{name}.lean"
        repair_data = repair_data_path.read_text(encoding="utf-8")
        repair_pair = re.search(r"RepairInitialMass : ℕ × ℕ := \((\d+), (\d+)\)", repair_data)
        assert repair_pair is not None
        assert tuple(map(int, repair_pair.groups())) == tuple(base["mass_vector_numerator"])
        repair_data_sha256 = hashlib.sha256(repair_data_path.read_bytes()).hexdigest()
        repair_route = "exact bounded packet assembly, retaining the original initial-mass proof premise"
    else:
        assert " ".join(repair_body.split()) == " ".join(expected_direct_repair.split())
        repair_route = "direct kernel arithmetic, retaining the original initial-mass proof premise"
    records.append({"name": name, "status": "EXACT ALLOCATION LITERALS MATCH JSON",
                    "checked_at": checked_at,
                    "rows": len(rows), "packets": len(lean_packets),
                    "lean_sha256": hashlib.sha256(lean_path.read_bytes()).hexdigest(),
                    "moments_lean_sha256": hashlib.sha256(moments_path.read_bytes()).hexdigest(),
                    "counts_lean_sha256": hashlib.sha256(counts_path.read_bytes()).hexdigest(),
                    "initial_mass_lean_sha256": hashlib.sha256(mass_path.read_bytes()).hexdigest(),
                    "final_mass_lean_sha256": hashlib.sha256(final_mass_path.read_bytes()).hexdigest(),
                    "final_mass_shape": "exact depth/base eigenvector target and capacity, original initial sum, and signed repair premises",
                    "repair_route": repair_route,
                    "repair_data_lean_sha256": repair_data_sha256,
                    "repair_evidence_scope": "bounded chunk manifests and proof files are covered by the independent repair source audit and successful Lean receipts, not this literal checker",
                    "scope": "source correspondence only; successful Lean receipts establish theorem completion",
                    "binomial_tables": "exact Python math.comb match",
                    "initial_mass_target": "exact source numerator match; equality still requires Lean proof",
                    "initial_mass_proof_layout_overlay": proof_split if name == "Base661" else None,
                    "word_base_sha256": hashlib.sha256(raw_base).hexdigest(),
                    "packet_repair_sha256": hashlib.sha256(raw_packet).hexdigest()})
report = ROOT / "docs" / "section5-certificate-sourcecheck.json"
if report.exists():
    previous_raw = report.read_bytes()
    history_path = ROOT / "docs" / "section5-certificate-sourcecheck-history.json"
    history = json.loads(history_path.read_text(encoding="utf-8")) if history_path.exists() else []
    previous_hash = hashlib.sha256(previous_raw).hexdigest()
    if not any(entry["report_sha256"] == previous_hash for entry in history):
        history.append({"preserved_at": checked_at, "report_sha256": previous_hash,
                        "raw_report_utf8": previous_raw.decode("utf-8")})
        history_path.write_text(json.dumps(history, indent=2, ensure_ascii=False), encoding="utf-8")
report.write_text(json.dumps(records, indent=2), encoding="utf-8")
print(json.dumps(records, indent=2))
