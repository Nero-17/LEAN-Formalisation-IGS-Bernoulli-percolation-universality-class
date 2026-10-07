"""Import the four Section 5 allocation encodings as literal Lean data.

This program computes convenient slacks but supplies no proof oracle: every
claim about the literals is proved by ordinary Lean kernel reduction.
"""
from pathlib import Path
from math import comb
import hashlib
import json
import sys
import argparse

sys.set_int_max_str_digits(0)
ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "supplementary" / "section5" / "certificates"


def generate(folder, name, inputs_only=False):
    raw_base = (SOURCE / folder / "word_base.json").read_bytes()
    raw_packets = (SOURCE / folder / "packet_repair.json").read_bytes()
    base = json.loads(raw_base)
    repair = json.loads(raw_packets)
    depth = base["candidate"]["n"]
    assert base["candidate"] == repair["candidate"]
    rows, slacks, packets = [], [], []
    for zeros, ((first_false, first_true), remainder) in enumerate(
            zip(base["floor_groups"], base["lex_remainders"])):
        assert min(first_false, first_true, remainder) >= 0
        rows.append(f"⟨{first_false}, {first_true}, {remainder}⟩")
        count0 = comb(depth - 1, zeros - 1) if zeros else 0
        count1 = comb(depth - 1, zeros) if zeros < depth else 0
        bounds = []
        if count0:
            bounds.extend([first_false, 2 ** zeros - first_false - 1])
        if count1:
            bounds.extend([first_true, 2 ** zeros - first_true - 1])
        assert min(bounds) >= 0
        slacks.append(str(min(bounds)))
    for layer in repair["layers"]:
        index, height, tail_length = layer["t"], layer["h"], layer["suffix_length"]
        assert height == 2 * index + 1
        assert tail_length >= 2 and 2 * height + tail_length == depth
        for (first, repeated), coefficient in zip(
                [(False, False), (True, False), (True, True), (False, True)],
                layer["coefficients"]):
            packets.append(f"⟨{index}, {str(first).lower()}, {str(repeated).lower()}, "
                           f"{tail_length - 2}, {coefficient}⟩")
    sha_base = hashlib.sha256(raw_base).hexdigest()
    sha_packets = hashlib.sha256(raw_packets).hexdigest()
    content = f'''import Universality.Certificates.Section5RowChecks
import Universality.Certificates.Section5PacketChecks
import Universality.Certificates.Section5FastRank

/-!
Literal Section 5 allocation from supplementary/section5/certificates/{folder}.
word_base.json SHA256: {sha_base}
packet_repair.json SHA256: {sha_packets}
The generated slacks are independently checked against the original floors
and remainders by the Lean kernel.  No execution oracle is used.
-/

namespace Universality.Certificates

set_option maxHeartbeats 0
set_option maxRecDepth 100000
set_option exponentiation.threshold 4096

def allocation{name} : CompressedAllocation where
  depth := {depth}
  rows := [
    {',\n    '.join(rows)}]
  slacks := [
    {',\n    '.join(slacks)}]
  packets := [
    {',\n    '.join(packets)}]

set_option maxHeartbeats 0
set_option maxRecDepth 100000
set_option exponentiation.threshold 4096

theorem allocation{name}_uniform_slacks :
    ∀ zeros ∈ List.range (allocation{name}.depth + 1),
      (allocation{name}.rows[zeros]!).hasUniformSlack allocation{name}.depth zeros
        (allocation{name}.slacks[zeros]!) := by
  apply uniformAllocationRowsCheck_correct allocation{name} <;> decide +kernel
#check allocation{name}_uniform_slacks

theorem allocation{name}_initial_slacks :
    ∀ zeros ∈ List.range (allocation{name}.depth + 1),
      (allocation{name}.rows[zeros]!).hasSlack allocation{name}.depth zeros
        (allocation{name}.slacks[zeros]!) := by
  intro zeros member
  exact InitialAllocationRow.hasSlack_of_uniform _ _ _ _
    (allocation{name}_uniform_slacks zeros member)

theorem allocation{name}_disjoint :
    allocation{name}.packets.Pairwise
      (fun packet other => packet.signature ≠ other.signature) := by
  apply packets_pairwise_of_consecutive
  decide +kernel
#check allocation{name}_disjoint

theorem allocation{name}_packet_checks :
    ∀ packet ∈ allocation{name}.packets,
      2 * (2 * packet.layer + 1) + (packet.remaining + 2) = allocation{name}.depth ∧
      (|packet.coefficient| ≤ (allocation{name}.slacks[packet.zeros]! : ℤ) ∨
        packet.capacityChecked allocation{name}.rows) := by
  apply allocationPacketsCheckFast_correct allocation{name}.depth allocation{name}.slacks
    allocation{name}.rows (CorrectionPacket.fastCapacityCheck allocation{name}.rows)
    allocation{name}.packets
  · intro packet _ checked
    exact (CorrectionPacket.fastCapacityCheck_iff allocation{name}.rows packet).mp checked
  · decide +kernel
#check allocation{name}_packet_checks

theorem allocation{name}_capacityValid : allocation{name}.capacityValid :=
  ⟨by decide +kernel, by decide +kernel, by decide +kernel, allocation{name}_initial_slacks,
    allocation{name}_disjoint, allocation{name}_packet_checks⟩

theorem allocation{name}_capacity (word : List Bool)
    (length_checked : word.length = {depth}) :
    allocation{name}.allocation word ≤ 2 ^ zeroCount word :=
  allocation{name}.allocation_capacity allocation{name}_capacityValid word length_checked

end Universality.Certificates
'''
    directory = ROOT / "Universality" / "Certificates"
    destination = directory / f"Section5Data{name}.lean"
    input_content, theorem_content = content.rsplit("set_option maxHeartbeats 0", 1)
    input_path = directory / f"Section5Input{name}.lean"
    input_path.write_text(input_content + "end Universality.Certificates\n", encoding="utf-8")
    if not inputs_only:
        settings, theorem_content = theorem_content.split(f"theorem allocation{name}_uniform_slacks", 1)
        settings = "set_option maxHeartbeats 0" + settings
        theorem_content = f"theorem allocation{name}_uniform_slacks" + theorem_content
        rows_content, theorem_content = theorem_content.split(f"theorem allocation{name}_disjoint", 1)
        disjoint_content, theorem_content = (f"theorem allocation{name}_disjoint" + theorem_content).split(
            f"theorem allocation{name}_packet_checks", 1)
        packet_content, final_content = (f"theorem allocation{name}_packet_checks" + theorem_content).split(
            f"theorem allocation{name}_capacityValid", 1)
        for part, body in [("Rows", rows_content), ("Disjoint", disjoint_content), ("PacketCapacity", packet_content)]:
            part_content = (f"import Universality.Certificates.Section5Input{name}\n\n"
                            "namespace Universality.Certificates\n\n" + settings + body +
                            "end Universality.Certificates\n")
            (directory / f"Section5{part}{name}.lean").write_text(part_content, encoding="utf-8")
        content = ("".join(f"import Universality.Certificates.Section5{part}{name}\n"
                           for part in ["Rows", "Disjoint", "PacketCapacity"]) +
                   "\nnamespace Universality.Certificates\n\n" + settings +
                   f"theorem allocation{name}_capacityValid" + final_content)
        destination.write_text(content, encoding="utf-8")
    return {"folder": folder, "lean": str(destination.relative_to(ROOT)),
            "literal_lean": str(input_path.relative_to(ROOT)),
            "depth": depth, "rows": len(rows), "packets": len(packets),
            "word_base_sha256": sha_base, "packet_repair_sha256": sha_packets}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs-only", action="store_true")
    args = parser.parse_args()
    manifest = [generate(folder, name, args.inputs_only) for folder, name in [
        ("n424", "Base19"), ("n936", "Base661"),
        ("n952", "Base739"), ("transcendental", "Shifted19")]]
    (ROOT / "docs" / "section5-certificate-inputs.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))
