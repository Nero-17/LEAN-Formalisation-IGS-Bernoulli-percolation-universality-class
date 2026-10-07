"""Read-only witness/source audit; never substitutes for kernel transition checks."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
FOLDERS = {"Base19": "n424", "Base661": "n936", "Base739": "n952", "Shifted19": "transcendental"}
sys.set_int_max_str_digits(0)


def normalize_small_raw(text):
    return re.sub(r"\(nat_lit (0x[0-9a-f]+)\)", lambda match: str(int(match[1], 16)), text)


def natural(text):
    tokens = re.findall(r"Nat\.shiftLeft|nat_lit|0x[0-9a-f]+|[0-9]+|[()+]", text)
    index = 0
    def read():
        nonlocal index
        token = tokens[index]; index += 1
        if token != "(":
            return int(token, 16 if token.startswith("0x") else 10)
        operator = tokens[index]; index += 1
        if operator == "nat_lit":
            value = read()
        else:
            assert operator == "Nat.shiftLeft"
            left, shift = read(), read()
            assert tokens[index] == "+"; index += 1
            value = (left << shift) + read()
        assert tokens[index] == ")"; index += 1
        return value
    value = read()
    assert index == len(tokens)
    return value


def pair(text):
    text = text.strip()
    assert text.startswith("(") and text.endswith(")")
    return tuple(natural(part) for part in text[1:-1].split(","))


def review(name):
    manifest = json.loads((ROOT / f"docs/section5-certificate-chunks-{name}.json").read_text(encoding="utf-8-sig"))
    source = (ROOT / f"supplementary/section5/certificates/{FOLDERS[name]}/word_base.json").read_bytes()
    assert hashlib.sha256(source).hexdigest() == manifest["source_sha256"], "source hash"
    data = json.loads(source)
    depth = data["candidate"]["n"]
    bits = 6 * (depth + 1) + 12
    assert manifest["depth"] == depth and manifest["packing_bits"] == bits
    checkpoints, transitions, texts, owners, module_imports = {}, [], {}, {}, {}
    entries = list(manifest["modules"])
    overlay_review = None
    if name == "Base661" and (ROOT / "docs/section5-proof66112-split-overlay.json").exists():
        # The only permitted manifest exception is anchored in the pre-existing
        # restoration receipt and original proof hash, not in new self-reported hashes.
        from section5_certificate_proof_split import validate_overlay, MODULE, LEAVES
        overlay_review = validate_overlay(ROOT)
        overlay = json.loads((ROOT / overlay_review["overlay_path"]).read_text(encoding="utf-8"))
        positions = [index for index, entry in enumerate(entries) if entry["module"] == MODULE]
        assert len(positions) == 1
        assembly = dict(overlay["assembly"], module=MODULE)
        entries[positions[0]:positions[0] + 1] = [assembly] + overlay["leaves"]
    for entry in entries:
        raw = (ROOT / "Universality/Certificates" / (entry["module"] + ".lean")).read_bytes()
        assert len(raw) == entry["bytes"] and hashlib.sha256(raw).hexdigest() == entry["sha256"], entry["module"]
        text = raw.decode("utf-8-sig")
        # Large data batches are inspected one at a time, never retained together.
        if "MassChunkData" not in entry["module"]:
            texts[entry["module"]] = text
        module_imports[entry["module"]] = re.findall(
            r"^import Universality\.Certificates\.([A-Za-z0-9_]+)\s*$", text, re.M)
        assert not re.search(r"\b(sorry|admit|axiom|native_decide|unsafe)\b", text), "forbidden token"
        for index, remaining, body in re.findall(
                r"def checkpoint(\d+) : LexMassCheckpoint where\s+depth := (\d+)(.*?)(?=\ndef |\nend )", text, re.S):
            # Avoid expanding megabit packed literals into decimal strings.
            body = body[body.index("states :="):]
            states = [tuple(natural(part.strip(" \u27e8\u27e9")) for part in state.split(","))
                      for state in re.findall(r"\u27e8([^\n]+)\u27e9\u27e9", body)]
            assert all(len(state) == 6 for state in states)
            mass = pair(re.search(r"mass := ([^\n]+)", body)[1])
            assert len(states) == depth + 1 and int(remaining) == depth - int(index)
            assert int(index) not in checkpoints
            checkpoints[int(index)] = (states, mass) if int(index) in (0, depth) else None
            owners[int(index)] = entry["module"]
        transitions.extend(tuple(map(int, match)) for match in re.findall(
            r"runLexMassChunk (\d+) (\d+) checkpoint(\d+) = checkpoint(\d+) := by\s+decide \+kernel", text))
    expected = list(range(0, depth, manifest["chunk_steps"])) + [depth]
    assert sorted(checkpoints) == expected and manifest["checkpoints"] == len(expected)
    pairs = list(zip(expected, expected[1:]))
    assert transitions == [(bits, last - first, first, last) for first, last in pairs]
    def available(module, seen=None):
        seen = set() if seen is None else seen
        if module in seen:
            return seen
        seen.add(module)
        for imported in module_imports.get(module, []):
            available(imported, seen)
        return seen
    for module, text in texts.items():
        if "MassChunkProof" in module:
            visible = available(module)
            assert all(owners[int(index)] in visible for index in re.findall(r"checkpoint(\d+)", text)), "missing checkpoint import"
    assert checkpoints[0][0] == [(zeros, remainder, 1, 0, 0, 1) for zeros, remainder in enumerate(data["lex_remainders"])]
    assert checkpoints[0][1] == (0, 0)
    final = texts[f"Section5InitialMass{name}"]
    final_visible = available(f"Section5InitialMass{name}")
    assert all(module in final_visible for module in texts if "MassChunkProof" in module), "missing final proof import"
    chain = final.split(f"theorem allocation{name}_chunk_values")[1].split(f"theorem allocation{name}_terminalMass")[0]
    assert [tuple(map(int, match)) for match in re.findall(r"values(\d+)_(\d+)", chain)] == pairs
    initial = texts[f"Section5MassChunkInitial{name}"]
    floor = pair(re.search(r"def floorMass[^\n]*:= ([^\n]+)", initial)[1])
    terminal = list(checkpoints[depth][1])
    for zeros, remainder, a, b, c, d in checkpoints[depth][0]:
        if zeros == 0 and remainder > 0:
            terminal[0] += a * 3139 + b * 1313
            terminal[1] += c * 3139 + d * 1313
    assert [floor[index] + terminal[index] for index in range(2)] == data["mass_vector_numerator"]
    target = re.search(rf"def allocation{name}InitialMass[^\n]*:= ([^\n]+)", final)
    assert pair(target[1]) == tuple(data["mass_vector_numerator"])
    assert f"initialMassEvaluation_of_chunk_values {depth} allocation{name}.rows" in final
    assert "rfl initial_packed initial_counts initial_states rfl" in final
    assert f"allocation{name}_chunk_values rfl initial_floor allocation{name}_terminalMass" in final
    return {"name": name, "source_sha256": manifest["source_sha256"], "modules": len(entries), "proof_layout_overlay": overlay_review,
            "checkpoints": len(checkpoints), "transitions": len(transitions), "status": "source_audit_pass",
            "scope": "Hashes, coverage, state initialization, assembly syntax, and literal terminal sum only; not kernel transition verification."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("names", nargs="+", choices=list(FOLDERS))
    args = parser.parse_args()
    print(json.dumps([review(name) for name in args.names], indent=2))
