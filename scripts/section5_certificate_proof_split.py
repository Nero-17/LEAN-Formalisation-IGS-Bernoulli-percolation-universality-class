"""Exact source-layout overlay for the interrupted Base661 proof batch 12.

The four original numerical equality proofs are copied byte for byte.  This
tool never changes the immutable checkpoint manifests, data or generators,
and source-layout validation is not a Lean proof or a recovered exit status.
"""
from pathlib import Path
from datetime import datetime
import argparse
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
MODULE = "Section5MassChunkProofBase66112"
SOURCE = Path("Universality/Certificates") / (MODULE + ".lean")
BACKUP = Path("docs/section5-proof-split-original") / (MODULE + ".lean")
OVERLAY = Path("docs/section5-proof66112-split-overlay.json")
MANIFEST = Path("docs/section5-certificate-chunks-Base661.json")
RESTORATION = Path("docs/section5-chunk-data-restoration.json")
ORIGINAL_SHA256 = "9294ea6a8d1581d96f85723e0cad2b4a23383b1a94014263a4fbe5ec4d43829a"
MANIFEST_SHA256 = "e0304de27d12fd47910934807ead804cb93ade25c2da52fe6098e2fa9b837e0d"
RESTORATION_SHA256 = "f2c24365447987ff8a71d2cf674e94283cf492306f26894d07f610c22f2d9101"
TRANSITIONS = ["0768_0784", "0784_0800", "0800_0816", "0816_0832"]
LEAVES = [MODULE + suffix for suffix in "ABCD"]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def file_digest(path):
    result = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            result.update(block)
    return result.hexdigest()


def immutable_files(root):
    """Anchor unchanged files in the actual, previously archived restoration receipt."""
    require(file_digest(root / RESTORATION) == RESTORATION_SHA256,
            "historical restoration receipt changed")
    restoration = json.loads((root / RESTORATION).read_text(encoding="utf-8"))
    require(restoration["status"] == "pass", "restoration receipt is not a pass")
    records = [{"path": RESTORATION.as_posix(), "sha256": RESTORATION_SHA256}]
    records += [{"path": item["path"], "sha256": item["sha256"]}
                for item in restoration["manifests"] + restoration["source_inputs"]]
    records += [{"path": item["path"], "sha256": item["source_sha256"]}
                for item in restoration["files"]]
    records += [
        {"path": "scripts/section5_certificate_chunks.py", "sha256": restoration["generator_sha256"]},
        {"path": "scripts/restore_section5_chunk_data.py", "sha256": restoration["restore_script_sha256"]}]
    require(len(restoration["files"]) == 44, "expected all 44 unchanged data files")
    require(any(item["path"] == MANIFEST.as_posix() and item["sha256"] == MANIFEST_SHA256
                for item in records), "Base661 manifest lacks historical anchor")
    for item in records:
        require(file_digest(root / item["path"]) == item["sha256"],
                "immutable source changed: " + item["path"])
    return records


def split_original(original):
    require(len(original) == 1737 and digest(original) == ORIGINAL_SHA256,
            "original Proof12 bytes do not match archived manifest")
    matches = list(re.finditer(rb"(?m)^theorem transition([0-9]{4}_[0-9]{4}) :", original))
    require([match.group(1).decode() for match in matches] == TRANSITIONS,
            "unexpected original transition declarations")
    footer_start = original.rindex(b"\r\nend Universality.Certificates.MassChunksBase661\r\n")
    header, footer = original[:matches[0].start()], original[footer_start:]
    blocks = [original[match.start():(matches[index + 1].start() if index < 3 else footer_start)]
              for index, match in enumerate(matches)]
    require(header + b"".join(blocks) + footer == original, "split does not exactly cover old source")
    names = re.findall(rb"(?m)^theorem ([A-Za-z0-9_]+) :", original)
    expected = [name.encode() for transition in TRANSITIONS
                for name in ("transition" + transition, "values" + transition)]
    require(names == expected, "eight original public declarations are not exact")
    return header, blocks, footer


def expected_assembly():
    return b"".join(("import Universality.Certificates." + leaf + "\r\n").encode()
                    for leaf in LEAVES)


def leaf_records(header, blocks, footer):
    offset = len(header)
    records = []
    for leaf, transition, block in zip(LEAVES, TRANSITIONS, blocks):
        content = header + block + footer
        records.append({"module": leaf,
                        "path": (Path("Universality/Certificates") / (leaf + ".lean")).as_posix(),
                        "bytes": len(content), "sha256": digest(content),
                        "original_body_start_byte": offset, "original_body_end_byte": offset + len(block),
                        "body_sha256": digest(block),
                        "declarations": ["transition" + transition, "values" + transition]})
        offset += len(block)
    return records


def prepare(root):
    require(not (root / OVERLAY).exists(), "overlay already exists; use validation only")
    original = (root / SOURCE).read_bytes()
    header, blocks, footer = split_original(original)
    frozen = immutable_files(root)
    manifest = json.loads((root / MANIFEST).read_text(encoding="utf-8"))
    entry = [item for item in manifest["modules"] if item["module"] == MODULE]
    require(len(entry) == 1 and entry[0]["sha256"] == ORIGINAL_SHA256 and entry[0]["bytes"] == 1737,
            "archived manifest does not bind original Proof12")
    require(not (root / BACKUP).exists(), "backup already exists")
    leaves = leaf_records(header, blocks, footer)
    require(all(not (root / item["path"]).exists() for item in leaves), "leaf source already exists")
    (root / BACKUP).parent.mkdir(parents=True, exist_ok=True)
    with (root / BACKUP).open("xb") as output:
        output.write(original)
    for item, block in zip(leaves, blocks):
        with (root / item["path"]).open("xb") as output:
            output.write(header + block + footer)
    assembly = expected_assembly()
    (root / SOURCE).write_bytes(assembly)
    overlay = {
        "schema": 1, "status": "exact_source_layout_only_pending_kernel_checks",
        "prepared_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "reason": "Old batch had no successful object/receipt after a snapshot_after subprocess error; do not infer its Lean exit code.",
        "original_manifest": {"path": MANIFEST.as_posix(), "sha256": MANIFEST_SHA256},
        "historical_restoration_receipt": {"path": RESTORATION.as_posix(), "sha256": RESTORATION_SHA256},
        "original_source": {"path": SOURCE.as_posix(), "backup_path": BACKUP.as_posix(),
                            "bytes": len(original), "sha256": ORIGINAL_SHA256},
        "header_sha256": digest(header), "footer_sha256": digest(footer),
        "leaves": leaves,
        "assembly": {"path": SOURCE.as_posix(), "bytes": len(assembly), "sha256": digest(assembly),
                     "imports": ["Universality.Certificates." + leaf for leaf in LEAVES]},
        "unchanged_files": frozen,
        "declaration_coverage": "Exactly the original eight declarations, once each, with byte-identical bodies, header/options/namespace and footer.",
        "proof_scope": "Every new transition still requires its own actual Lean kernel check; no historical successful exit is synthesized."}
    with (root / OVERLAY).open("x", encoding="utf-8", newline="\n") as output:
        json.dump(overlay, output, indent=2)
        output.write("\n")
    return validate_overlay(root)


def validate_overlay(root=ROOT):
    root = Path(root)
    overlay = json.loads((root / OVERLAY).read_text(encoding="utf-8"))
    require(overlay["schema"] == 1, "unsupported proof split schema")
    frozen = immutable_files(root)
    require(overlay["unchanged_files"] == frozen, "immutable file list changed")
    require(overlay["original_manifest"] == {"path": MANIFEST.as_posix(), "sha256": MANIFEST_SHA256},
            "unrecognized manifest exception")
    require(overlay["historical_restoration_receipt"] ==
            {"path": RESTORATION.as_posix(), "sha256": RESTORATION_SHA256}, "historical anchor changed")
    require(overlay["original_source"] == {"path": SOURCE.as_posix(), "backup_path": BACKUP.as_posix(),
                                          "bytes": 1737, "sha256": ORIGINAL_SHA256},
            "unrecognized original source exception")
    manifest = json.loads((root / MANIFEST).read_text(encoding="utf-8"))
    original_entry = [item for item in manifest["modules"] if item["module"] == MODULE]
    require(len(original_entry) == 1 and original_entry[0]["sha256"] == ORIGINAL_SHA256 and
            original_entry[0]["bytes"] == 1737, "old manifest entry changed")
    original = (root / BACKUP).read_bytes()
    header, blocks, footer = split_original(original)
    require(overlay["header_sha256"] == digest(header) and overlay["footer_sha256"] == digest(footer),
            "original header/options/namespace or footer changed")
    expected_leaves = leaf_records(header, blocks, footer)
    require(overlay["leaves"] == expected_leaves, "leaf mapping, exact body bytes or coverage changed")
    for item, block in zip(expected_leaves, blocks):
        require((root / item["path"]).read_bytes() == header + block + footer,
                "leaf differs from exact original declaration slice: " + item["path"])
    assembly = expected_assembly()
    require((root / SOURCE).read_bytes() == assembly, "aggregate must contain only the four exact imports")
    require(overlay["assembly"] == {"path": SOURCE.as_posix(), "bytes": len(assembly),
                                    "sha256": digest(assembly),
                                    "imports": ["Universality.Certificates." + leaf for leaf in LEAVES]},
            "aggregate metadata differs from exact four imports")
    return {"status": "pass", "scope": "source-layout equivalence only; no Lean exit inferred",
            "overlay_path": OVERLAY.as_posix(), "overlay_sha256": file_digest(root / OVERLAY),
            "original_source_sha256": ORIGINAL_SHA256, "original_manifest_sha256": MANIFEST_SHA256,
            "assembly_sha256": digest(assembly), "leaf_modules": LEAVES,
            "leaf_source_sha256": {item["module"]: item["sha256"] for item in expected_leaves},
            "declarations": [name for item in expected_leaves for name in item["declarations"]],
            "immutable_files_checked": len(frozen), "data_files_checked": 44}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--prepare", action="store_true", help="Perform the one explicitly authorized source split")
    arguments = parser.parse_args()
    print(json.dumps(prepare(ROOT) if arguments.prepare else validate_overlay(ROOT), indent=2))
