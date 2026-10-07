"""Emit exact bounded checks for the two large signed packet repairs.

Each consecutive block is checked against the unchanged packet evaluator.
The exact flattening back to the actual input packet list, the baseline and
the final target are separate kernel obligations. Python proposes literals;
it supplies no proof oracle and does not change the initial-stream data.
"""

from pathlib import Path
from datetime import datetime
import argparse
import hashlib
import json
import sys

sys.set_int_max_str_digits(0)
ROOT = Path(__file__).resolve().parents[1]


def kernel_step(bit, value):
    first, second = value
    return (9 * first + 12 * second, 3 * first + 6 * second) if bit else (
        22 * first + 18 * second, 5 * first + 18 * second)


def packet_value(packet):
    layer, first, repeated, remaining, coefficient = packet
    value = (3139, 1313)
    for _ in range(remaining + 1):
        value = kernel_step(repeated, value)
    first_value, second_value = kernel_step(first, value)
    scaled_coefficient = coefficient * 18 ** layer
    return (scaled_coefficient * (-6 * first_value - 6 * second_value),
            scaled_coefficient * (3 * first_value + 6 * second_value))


def generate(folder, name, size, checks_per_module):
    directory = ROOT / "supplementary" / "section5" / "certificates" / folder
    base_raw = (directory / "word_base.json").read_bytes()
    repair_raw = (directory / "packet_repair.json").read_bytes()
    data, repair = json.loads(base_raw), json.loads(repair_raw)
    if data["candidate"] != repair["candidate"]:
        raise ValueError("Original input candidate identities differ")
    depth, base = data["candidate"]["n"], data["candidate"]["s"]
    packets = []
    for layer in repair["layers"]:
        if layer["h"] != 2 * layer["t"] + 1 or 2 * layer["h"] + layer["suffix_length"] != depth:
            raise ValueError("Original layer length is inconsistent")
        coefficients = layer["coefficients"]
        if len(coefficients) != 4 or layer["suffix_length"] < 2:
            raise ValueError("Original packet layer is malformed")
        for (first, repeated), coefficient in zip(
                [(False, False), (True, False), (True, True), (False, True)], coefficients):
            packets.append((layer["t"], first, repeated, layer["suffix_length"] - 2, coefficient))
    chunks = [packets[index:index + size] for index in range(0, len(packets), size)]
    values = []
    for chunk in chunks:
        pair_values = [packet_value(packet) for packet in chunk]
        values.append((sum(value[0] for value in pair_values), sum(value[1] for value in pair_values)))
    baseline = (55, 23)
    for _ in range(depth):
        first, second = baseline
        baseline = (53 * first + 48 * second, 13 * first + 42 * second)
    baseline = (16 * baseline[0], 16 * baseline[1])
    initial = data["mass_vector_numerator"]
    target_scale = 16 ** (depth + 1) * base ** 219
    target = (target_scale * 55, target_scale * 23)
    total = tuple(baseline[index] + initial[index] + sum(value[index] for value in values) for index in range(2))
    if total != target or sum(chunks, []) != packets:
        raise ValueError("Proposed bounded repair does not reproduce the original final target")

    namespace = f"Universality.Certificates.MassRepairChunks{name}"
    options = ("set_option maxHeartbeats 0\nset_option maxRecDepth 100000\n"
               "set_option exponentiation.threshold 10000\nset_option Elab.async false\n\n")
    provenance = (f"/-! Consecutive signed packet blocks from the original {folder} certificate.\n"
                  f"word_base.json SHA256: {hashlib.sha256(base_raw).hexdigest()}\n"
                  f"packet_repair.json SHA256: {hashlib.sha256(repair_raw).hexdigest()}\n"
                  "All proposed block values require independent kernel checks. -/\n\n")
    modules, order = [], []

    def write(module, content):
        destination = ROOT / "Universality" / "Certificates" / (module + ".lean")
        destination.write_text(content, encoding="utf-8")
        payload = destination.read_bytes()
        modules.append({"module": module, "bytes": len(payload), "sha256": hashlib.sha256(payload).hexdigest()})
        order.append(module)

    data_module = f"Section5MassRepairData{name}"
    content = (f"import Universality.Certificates.Section5Input{name}\n"
               "import Universality.Certificates.Section5MassRepairChunks\n\n" + provenance +
               "namespace Universality.Certificates\n\n" + options +
               f"def allocation{name}RepairInitialMass : ℕ × ℕ := ({initial[0]}, {initial[1]})\n\n" +
               f"namespace MassRepairChunks{name}\n\n")
    for index, (chunk, value) in enumerate(zip(chunks, values)):
        rendered = ",\n  ".join(f"⟨{layer}, {str(first).lower()}, {str(repeated).lower()}, {remaining}, {coefficient}⟩"
                                 for layer, first, repeated, remaining, coefficient in chunk)
        content += f"def packets{index:02d} : List CorrectionPacket := [\n  {rendered}]\n\n"
        content += f"def value{index:02d} : ℤ × ℤ := ({value[0]}, {value[1]})\n\n"
    content += "def chunks : List (List CorrectionPacket) := [" + ", ".join(f"packets{index:02d}" for index in range(len(chunks))) + "]\n\n"
    content += "def values : List (ℤ × ℤ) := [" + ", ".join(f"value{index:02d}" for index in range(len(chunks))) + "]\n\n"
    content += f"def baseline : ℤ × ℤ := ({baseline[0]}, {baseline[1]})\n\n"
    content += f"end MassRepairChunks{name}\nend Universality.Certificates\n"
    write(data_module, content)

    checks_module = f"Section5MassRepairChecks{name}"
    content = f"import Universality.Certificates.{data_module}\n\nnamespace {namespace}\n\n" + options
    content += f'''theorem parts_checked : chunks.flatten = allocation{name}.packets := by
  decide +kernel

theorem baseline_checked : baselineMassEvaluation {depth} = baseline := by
  decide +kernel

theorem total_checked :
    addIntegerMassPairs
      (addIntegerMassPairs baseline
        ((allocation{name}RepairInitialMass.1 : ℤ), (allocation{name}RepairInitialMass.2 : ℤ)))
      (sumIntegerMassPairs values) = massCertificateValue {depth} {base} := by
  decide +kernel

#print axioms parts_checked
#print axioms baseline_checked
#print axioms total_checked
end {namespace}
'''
    write(checks_module, content)
    proof_modules = []
    for batch, start in enumerate(range(0, len(chunks), checks_per_module)):
        module = f"Section5MassRepairProof{name}{batch:02d}"
        content = f"import Universality.Certificates.{data_module}\n\nnamespace {namespace}\n\n" + options
        for index in range(start, min(start + checks_per_module, len(chunks))):
            content += f'''theorem checked{index:02d} : correctionsMassEvaluation packets{index:02d} = value{index:02d} := by
  decide +kernel

#print axioms checked{index:02d}
'''
        content += f"\nend {namespace}\n"
        write(module, content)
        proof_modules.append(module)

    content = "".join(f"import Universality.Certificates.{module}\n" for module in [checks_module, *proof_modules])
    content += "\nnamespace Universality.Certificates\n\n" + options + f"open MassRepairChunks{name}\n\n"
    chain = "List.Forall₂.nil"
    for index in reversed(range(len(chunks))):
        chain = f"(List.Forall₂.cons checked{index:02d} {chain})"
    content += f'''theorem allocation{name}_repairChunksChecked :
    List.Forall₂ (fun chunk value => correctionsMassEvaluation chunk = value) chunks values :=
  {chain}

theorem allocation{name}_massRepairLiteral :
    massEvaluationWithInitial {depth} allocation{name}.packets allocation{name}RepairInitialMass =
      massCertificateValue {depth} {base} :=
  massEvaluationWithInitial_of_chunks {depth} allocation{name}.packets allocation{name}RepairInitialMass
    chunks values baseline (massCertificateValue {depth} {base}) parts_checked
    allocation{name}_repairChunksChecked baseline_checked total_checked

#print axioms allocation{name}_repairChunksChecked
#print axioms allocation{name}_massRepairLiteral
end Universality.Certificates
'''
    write(f"Section5MassRepair{name}", content)
    manifest = {"name": name, "generated": datetime.now().astimezone().isoformat(timespec="seconds"),
                "depth": depth, "base": base, "packet_count": len(packets),
                "chunk_size": size, "chunks": len(chunks), "checks_per_module": checks_per_module,
                "word_base_sha256": hashlib.sha256(base_raw).hexdigest(),
                "packet_repair_sha256": hashlib.sha256(repair_raw).hexdigest(),
                "generator_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                "chunk_coverage": [{"index": index, "start": index * size, "length": len(chunk),
                                    "kernel_power_steps": sum(packet[3] + 1 for packet in chunk),
                                    "first_letter_steps": len(chunk),
                                    "maximum_repeated_steps": max(packet[3] + 1 for packet in chunk)}
                                   for index, chunk in enumerate(chunks)],
                "modules": modules, "check_order": order,
                "status": "Python proposed literals reproduce the original target; Lean checks still required"}
    manifest_path = ROOT / "docs" / f"section5-certificate-repair-chunks-{name}.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps({"name": name, "packets": len(packets), "chunks": len(chunks),
                      "modules": len(modules), "bytes": sum(item["bytes"] for item in modules),
                      "max_chunk_kernel_steps": max(sum(packet[3] + 2 for packet in chunk) for chunk in chunks)}), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chunk-size", type=int, default=32)
    parser.add_argument("--checks-per-module", type=int, default=4)
    args = parser.parse_args()
    if args.chunk_size <= 0 or args.checks_per_module <= 0:
        parser.error("chunk sizes must be positive")
    for folder, name in [("n936", "Base661"), ("n952", "Base739")]:
        generate(folder, name, args.chunk_size, args.checks_per_module)


if __name__ == "__main__":
    main()
