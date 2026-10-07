"""Emit a small, exact, kernel-checkable streaming-mass checkpoint trial.

Python constructs witnesses only.  The generated Lean file checks the actual
initial data and every bounded transition with ordinary kernel reduction.
Keep every state, including zero remainders, in its original order.
"""
from pathlib import Path
from dataclasses import dataclass
import argparse
import hashlib
import json
import sys
import time

sys.set_int_max_str_digits(0)
sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]
NAMES = {"n424": "Base19", "n936": "Base661", "n952": "Base739", "transcendental": "Shifted19"}


@dataclass
class Checkpoint:
    depth: int
    packed: tuple[int, int]
    counts: int
    states: list[tuple[int, int, int, int, int, int]]
    mass: tuple[int, int]


def initial_checkpoint(data, bits):
    depth = data["candidate"]["n"]
    packed = (3139, 1313)
    for _ in range(depth):
        first, second = packed
        packed = (((22 * first + 18 * second) << bits) + 9 * first + 12 * second,
                  ((5 * first + 18 * second) << bits) + 3 * first + 6 * second)
    return Checkpoint(depth, packed, ((1 << bits) + 1) ** depth,
                      [(zeros, remainder, 1, 0, 0, 1)
                       for zeros, remainder in enumerate(data["lex_remainders"])], (0, 0))


def step_checkpoint(checkpoint, bits):
    if checkpoint.depth == 0:
        return checkpoint
    base, mask = 1 << bits, (1 << bits) - 1
    determinant = 306 * base * base + 180 * base + 18
    first, second = checkpoint.packed
    first_numerator = (18 * base + 6) * first - (18 * base + 12) * second
    second_numerator = (22 * base + 9) * second - (5 * base + 3) * first
    assert first_numerator >= 0 and second_numerator >= 0
    first, first_remainder = divmod(first_numerator, determinant)
    second, second_remainder = divmod(second_numerator, determinant)
    counts, counts_remainder = divmod(checkpoint.counts, base + 1)
    assert first_remainder == second_remainder == counts_remainder == 0
    child_depth = checkpoint.depth - 1
    mass_first, mass_second = checkpoint.mass
    states = []
    for zeros, remainder, a, b, c, d in checkpoint.states:
        if remainder == 0:
            states.append((zeros, remainder, a, b, c, d))
            continue
        first_count = ((counts >> (bits * (zeros - 1))) & mask) if 0 < zeros <= child_depth + 1 else 0
        if remainder <= first_count:
            states.append((max(zeros - 1, 0), remainder, 22 * a + 5 * b, 18 * a + 18 * b,
                           22 * c + 5 * d, 18 * c + 18 * d))
        else:
            if 0 < zeros <= child_depth + 1:
                first_group = (first >> (bits * (zeros - 1))) & mask
                second_group = (second >> (bits * (zeros - 1))) & mask
                mass_first += (22 * a + 5 * b) * first_group + (18 * a + 18 * b) * second_group
                mass_second += (22 * c + 5 * d) * first_group + (18 * c + 18 * d) * second_group
            states.append((zeros, remainder - first_count, 9 * a + 3 * b, 12 * a + 6 * b,
                           9 * c + 3 * d, 12 * c + 6 * d))
    assert len(states) == len(checkpoint.states)
    return Checkpoint(child_depth, (first, second), counts, states, (mass_first, mass_second))


def render_nat(value, limb_bits=0, raw_literals=False):
    """Balanced literal limbs avoid quadratic elaboration of megabit tokens.

    This is an ordinary Nat expression, evaluated again by the Lean kernel.
    It changes only witness syntax, never which integer is asserted.
    """
    if not limb_bits or value.bit_length() <= limb_bits:
        return f"(nat_lit {hex(value)})" if raw_literals else hex(value)
    limbs = (value.bit_length() + limb_bits - 1) // limb_bits
    right_bits = (limbs // 2) * limb_bits
    left, right = value >> right_bits, value & ((1 << right_bits) - 1)
    return f"(Nat.shiftLeft {render_nat(left, limb_bits, raw_literals)} {right_bits} + {render_nat(right, limb_bits, raw_literals)})"


def render_checkpoint(name, checkpoint, limb_bits=0, raw_literals=False):
    def compact(value):
        return render_nat(value, limb_bits, raw_literals) if value.bit_length() > 64 else str(value)
    states = ",\n    ".join(f"⟨{zeros}, {compact(remainder)}, ⟨{compact(a)}, {compact(b)}, {compact(c)}, {compact(d)}⟩⟩"
                            for zeros, remainder, a, b, c, d in checkpoint.states)
    return f'''def {name} : LexMassCheckpoint where
  depth := {checkpoint.depth}
  packed := ({render_nat(checkpoint.packed[0], limb_bits, raw_literals)}, {render_nat(checkpoint.packed[1], limb_bits, raw_literals)})
  packedCounts := {render_nat(checkpoint.counts, limb_bits, raw_literals)}
  states := [
    {states}]
  mass := ({compact(checkpoint.mass[0])}, {compact(checkpoint.mass[1])})

'''


def floor_mass(data, first, bits):
    """Propose the separate first-letter floor contribution for kernel check."""
    child = step_checkpoint(first, bits)
    mask = (1 << bits) - 1
    total_first = total_second = 0
    for zeros, (first_false, first_true) in enumerate(data["floor_groups"]):
        if zeros:
            first_group = (child.packed[0] >> (bits * (zeros - 1))) & mask
            second_group = (child.packed[1] >> (bits * (zeros - 1))) & mask
            total_first += first_false * (22 * first_group + 18 * second_group)
            total_second += first_false * (5 * first_group + 18 * second_group)
        if zeros <= child.depth:
            first_group = (child.packed[0] >> (bits * zeros)) & mask
            second_group = (child.packed[1] >> (bits * zeros)) & mask
            total_first += first_true * (9 * first_group + 12 * second_group)
            total_second += first_true * (3 * first_group + 6 * second_group)
    return total_first, total_second


def production(data, raw, folder, name, bits, args):
    """Generate bounded witnesses and proof modules, never unchecked oracles."""
    depth = data["candidate"]["n"]
    first = initial_checkpoint(data, bits)
    checkpoints = [(0, first)]
    current = first
    for done in range(1, depth + 1):
        current = step_checkpoint(current, bits)
        if done % args.chunk_steps == 0 or done == depth:
            checkpoints.append((done, current))
    floor = floor_mass(data, first, bits)
    terminal_first, terminal_second = current.mass
    for zeros, remainder, a, b, c, d in current.states:
        if zeros == 0 and remainder > 0:
            terminal_first += a * 3139 + b * 1313
            terminal_second += c * 3139 + d * 1313
    assert current.depth == 0 and current.packed == (3139, 1313) and current.counts == 1
    assert [floor[0] + terminal_first, floor[1] + terminal_second] == data["mass_vector_numerator"]
    namespace = f"Universality.Certificates.MassChunks{name}"
    options = '''set_option maxHeartbeats 0
set_option maxRecDepth 100000
set_option exponentiation.threshold 10000
set_option Elab.async false

'''
    provenance = f'''/-! Exact checkpoint witnesses from supplementary/section5/certificates/{folder}.
word_base.json SHA256: {hashlib.sha256(raw).hexdigest()}
Packing width {bits} is fixed by original depth {depth}; all {depth + 1} states
are retained in source order. Numerical witnesses require kernel proofs. -/

'''
    directory = ROOT / "Universality" / "Certificates"
    outputs = []
    order = []

    def write(module, text):
        path = directory / (module + ".lean")
        path.write_text(text, encoding="utf-8")
        outputs.append({"module": module, "bytes": path.stat().st_size,
                        "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})

    segments = list(zip(checkpoints, checkpoints[1:]))
    batches = [segments[index:index + args.chunks_per_module]
               for index in range(0, len(segments), args.chunks_per_module)]
    proof_modules = []
    for batch_index, batch in enumerate(batches):
        suffix = f"{batch_index:02d}"
        data_module = f"Section5MassChunkData{name}{suffix}"
        proof_module = f"Section5MassChunkProof{name}{suffix}"
        if batch_index == 0:
            imports = ("import Universality.Certificates.Section5MassChunks\n"
                       f"import Universality.Certificates.Section5Input{name}\n\n")
        else:
            imports = "import Universality.Certificates.Section5MassChunks\n\n"
        content = imports + provenance + f"namespace {namespace}\n\n" + options
        if batch_index == 0:
            content += render_checkpoint("checkpoint0000", first, args.limb_bits, args.raw_literals)
        for _, (done, checkpoint) in batch:
            content += render_checkpoint(f"checkpoint{done:04d}", checkpoint, args.limb_bits, args.raw_literals)
        content += f"end {namespace}\n"
        write(data_module, content)
        order.append(data_module)
        content = f"import Universality.Certificates.{data_module}\n"
        if batch_index:
            content += f"import Universality.Certificates.Section5MassChunkData{name}{batch_index - 1:02d}\n"
        content += f"\nnamespace {namespace}\n\n" + options
        for (before, _), (after, _) in batch:
            content += f'''theorem transition{before:04d}_{after:04d} :
    runLexMassChunk {bits} {after - before} checkpoint{before:04d} = checkpoint{after:04d} := by
  decide +kernel

theorem values{before:04d}_{after:04d} :
    checkpoint{before:04d}.value {bits} = checkpoint{after:04d}.value {bits} :=
  runLexMassChunk_value_of_check {bits} {after - before}
    checkpoint{before:04d} checkpoint{after:04d} transition{before:04d}_{after:04d}

#print axioms transition{before:04d}_{after:04d}
'''
        content += f"\nend {namespace}\n"
        write(proof_module, content)
        order.append(proof_module)
        proof_modules.append(proof_module)

    initial_module = f"Section5MassChunkInitial{name}"
    content = f"import Universality.Certificates.Section5MassChunkData{name}00\n\nnamespace {namespace}\n\n" + options
    content += f'''def floorMass : ℕ × ℕ := ({floor[0]}, {floor[1]})

theorem initial_packed : checkpoint0000.packed = packedInitialVector (matrixPackingBase {depth}) {depth} := by
  decide +kernel

theorem initial_counts : checkpoint0000.packedCounts = (matrixPackingBase {depth} + 1) ^ {depth} := by
  decide +kernel

theorem initial_states : checkpoint0000.states = initialLexStates {depth} allocation{name}.rows := by
  decide +kernel

theorem initial_floor : initialFloorFromPackedBits {bits} {depth} allocation{name}.rows checkpoint0000.packed = floorMass := by
  decide +kernel

#print axioms initial_packed
#print axioms initial_counts
#print axioms initial_states
#print axioms initial_floor
end {namespace}
'''
    write(initial_module, content)
    order.insert(1, initial_module)
    content = "".join(f"import Universality.Certificates.{module}\n" for module in [initial_module, *proof_modules])
    content += "\n" + provenance + "namespace Universality.Certificates\n\n" + options
    content += f"open MassChunks{name}\n\n"
    expected_first, expected_second = data["mass_vector_numerator"]
    content += f"def allocation{name}InitialMass : ℕ × ℕ := ({expected_first}, {expected_second})\n\n"
    proof_chain = "\n    |>.trans ".join(f"values{before:04d}_{after:04d}" for (before, _), (after, _) in segments)
    # Parenthesized Eq.trans composition keeps all intermediate streams opaque.
    proof_chain = f"values{segments[0][0][0]:04d}_{segments[0][1][0]:04d}"
    for (before, _), (after, _) in segments[1:]:
        proof_chain = f"({proof_chain}).trans values{before:04d}_{after:04d}"
    content += f'''theorem allocation{name}_chunk_values :
    checkpoint0000.value {bits} = checkpoint{depth:04d}.value {bits} :=
  {proof_chain}

theorem allocation{name}_terminalMass :
    addMassPairs floorMass (addMassPairs checkpoint{depth:04d}.mass
      (sumMassPairs (checkpoint{depth:04d}.states.map terminalLexMass))) = allocation{name}InitialMass := by
  decide +kernel

theorem allocation{name}_initialMassEvaluation :
    initialMassEvaluation {depth} allocation{name}.rows = allocation{name}InitialMass :=
  initialMassEvaluation_of_chunk_values {depth} allocation{name}.rows
    checkpoint0000 checkpoint{depth:04d} floorMass allocation{name}InitialMass
    rfl initial_packed initial_counts initial_states rfl
    allocation{name}_chunk_values rfl initial_floor allocation{name}_terminalMass

#print axioms allocation{name}_chunk_values
#print axioms allocation{name}_terminalMass
#print axioms allocation{name}_initialMassEvaluation
end Universality.Certificates
'''
    final_module = f"Section5InitialMass{name}"
    write(final_module, content)
    order.append(final_module)
    manifest = {"name": name, "source_sha256": hashlib.sha256(raw).hexdigest(), "depth": depth,
                "packing_bits": bits, "chunk_steps": args.chunk_steps,
                "chunks_per_module": args.chunks_per_module, "states_per_checkpoint": depth + 1,
                "limb_bits": args.limb_bits, "raw_literals": args.raw_literals,
                "independent_data_from_batch": 1,
                "checkpoints": len(checkpoints), "modules": outputs, "check_order": order,
                "generated_witness_status": "Python replay matched source; all Lean equalities still require checks"}
    manifest_path = ROOT / "docs" / f"section5-certificate-chunks-{name}.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps({"manifest": str(manifest_path.relative_to(ROOT)), "source_bytes": sum(item["bytes"] for item in outputs),
                      "checkpoints": len(checkpoints), "modules": len(outputs), "check_order": order}), flush=True)


def decouple_existing_imports(name, first_batch):
    """Change only unused import headers of still-unchecked future modules."""
    manifest_path = ROOT / "docs" / f"section5-certificate-chunks-{name}.json"
    previous = manifest_path.read_bytes()
    manifest = json.loads(previous)
    backup = ROOT / "work" / f"section5-certificate-chunks-{name}-before-imports.json"
    if not backup.exists():
        backup.write_bytes(previous)
    changed = []
    for entry in manifest["modules"]:
        module = entry["module"]
        kind = next((kind for kind in ["Data", "Proof"] if module.startswith(f"Section5MassChunk{kind}{name}")), None)
        if kind is None:
            continue
        batch = int(module[-2:])
        if batch < first_batch:
            continue
        path = ROOT / "Universality" / "Certificates" / (module + ".lean")
        original = path.read_bytes()
        assert hashlib.sha256(original).hexdigest() == entry["sha256"]
        lines = original.splitlines(keepends=True)
        boundary = 0
        while boundary < len(lines) and (not lines[boundary].strip() or lines[boundary].startswith(b"import ")):
            boundary += 1
        body = b"".join(lines[boundary:])
        imports = (["Universality.Certificates.Section5MassChunks"] if kind == "Data" else
                   [f"Universality.Certificates.Section5MassChunkData{name}{batch:02d}",
                    f"Universality.Certificates.Section5MassChunkData{name}{batch - 1:02d}"])
        newline = b"\r\n" if b"\r\n" in original[:300] else b"\n"
        header = newline.join(("import " + item).encode() for item in imports) + newline + newline
        updated = header + body
        path.write_bytes(updated)
        changed.append({"module": module, "before_sha256": entry["sha256"],
                        "body_sha256": hashlib.sha256(body).hexdigest()})
        entry["sha256"] = hashlib.sha256(updated).hexdigest()
        entry["bytes"] = len(updated)
    manifest["independent_data_from_batch"] = first_batch
    manifest["import_header_revision"] = {"previous_manifest_sha256": hashlib.sha256(previous).hexdigest(),
                                          "changed": changed,
                                          "scope": "Only leading import headers changed; declaration bytes retained exactly."}
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps({"name": name, "changed_modules": len(changed), "independent_from_batch": first_batch}), flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", choices=NAMES, default="n424")
    parser.add_argument("--steps", type=int, default=2)
    parser.add_argument("--start", type=int, default=0, help="Trial only: start from an existing production checkpoint")
    parser.add_argument("--limb-bits", type=int, default=0)
    parser.add_argument("--tag", default="")
    parser.add_argument("--raw-literals", action="store_true")
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--chunk-steps", type=int, default=16)
    parser.add_argument("--chunks-per-module", type=int, default=4)
    parser.add_argument("--decouple-from", type=int)
    args = parser.parse_args()
    if args.decouple_from is not None:
        assert args.decouple_from >= 1
        decouple_existing_imports(NAMES[args.folder], args.decouple_from)
        return
    assert args.limb_bits == 0 or args.limb_bits >= 64
    assert not args.tag or args.tag.isalnum()
    started = time.monotonic()
    source = ROOT / "supplementary" / "section5" / "certificates" / args.folder / "word_base.json"
    raw = source.read_bytes()
    data = json.loads(raw)
    depth = data["candidate"]["n"]
    assert 0 < args.steps <= depth - args.start
    assert args.start >= 0
    bits = 6 * (depth + 1) + 12
    if args.full:
        assert args.chunk_steps > 0 and args.chunks_per_module > 0
        production(data, raw, args.folder, NAMES[args.folder], bits, args)
        return
    first = initial_checkpoint(data, bits)
    for _ in range(args.start):
        first = step_checkpoint(first, bits)
    last = first
    for _ in range(args.steps):
        last = step_checkpoint(last, bits)
    name = NAMES[args.folder]
    trial_name = name + args.tag
    content = f'''import Universality.Certificates.Section5MassChunks
import Universality.Certificates.Section5Input{name}

/-! Two bounded checkpoints from the original allocation data.
word_base.json SHA256: {hashlib.sha256(raw).hexdigest()}
The fixed packing width is determined by the original depth, never the
remaining depth.  Every literal is a witness checked below, not an axiom. -/

namespace Universality.Certificates.ChunkTrial{trial_name}

set_option maxHeartbeats 0
set_option maxRecDepth 100000
set_option exponentiation.threshold 10000
set_option Elab.async false

'''
    if args.start:
        manifest = json.loads((ROOT / "docs" / f"section5-certificate-chunks-{name}.json").read_text())
        assert args.start % manifest["chunk_steps"] == 0
        batch_index = (args.start - 1) // (manifest["chunk_steps"] * manifest["chunks_per_module"])
        content = (f"import Universality.Certificates.Section5MassChunkData{name}{batch_index:02d}\n" + content)
        content += f"def initialCheckpoint : LexMassCheckpoint := MassChunks{name}.checkpoint{args.start:04d}\n\n"
    else:
        content += render_checkpoint("initialCheckpoint", first, args.limb_bits, args.raw_literals)
    content += render_checkpoint("afterCheckpoint", last, args.limb_bits, args.raw_literals)
    if not args.start:
        content += f'''theorem initial_packed :
    initialCheckpoint.packed = packedInitialVector (matrixPackingBase {depth}) {depth} := by
  decide +kernel

theorem initial_counts :
    initialCheckpoint.packedCounts = (matrixPackingBase {depth} + 1) ^ {depth} := by
  decide +kernel

theorem initial_states :
    initialCheckpoint.states = initialLexStates {depth} allocation{name}.rows := by
  decide +kernel

'''
    content += f'''
theorem transition_checked : runLexMassChunk {bits} {args.steps} initialCheckpoint = afterCheckpoint := by
  decide +kernel

theorem value_checked : initialCheckpoint.value {bits} = afterCheckpoint.value {bits} :=
  runLexMassChunk_value_of_check {bits} {args.steps} initialCheckpoint afterCheckpoint transition_checked

#print axioms transition_checked
#print axioms value_checked
end Universality.Certificates.ChunkTrial{trial_name}
'''
    destination = ROOT / "Universality" / "Certificates" / f"Section5ChunkTrial{trial_name}.lean"
    destination.write_text(content, encoding="utf-8")
    print(json.dumps({"file": str(destination.relative_to(ROOT)), "bytes": destination.stat().st_size,
                      "depth": depth, "bits": bits, "steps": args.steps, "states": len(first.states),
                      "start": args.start,
                      "limb_bits": args.limb_bits,
                      "raw_literals": args.raw_literals,
                      "generation_seconds": round(time.monotonic() - started, 3)}), flush=True)


if __name__ == "__main__":
    main()
