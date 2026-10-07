"""Restore omitted generated checkpoint data, with byte-for-byte manifest checks.

The archive retains every proof, source JSON, manifest and generation routine.
Only the large, pure-data Section5MassChunkData*.lean copies are reconstructed.
This does not replace a Lean proof: it restores precisely the source bytes
whose hashes occur in the archived manifests and compilation receipts.

The destination must be a separate, empty directory. Existing files are never
overwritten, including the live repository's already checked Lean sources.
The output uses the original Windows CRLF bytes on every operating system.
"""

from datetime import datetime
from pathlib import Path
import argparse
import hashlib
import json
import sys
import time

from section5_certificate_chunks import (
    NAMES, initial_checkpoint, render_checkpoint, step_checkpoint,
)

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    result = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            result.update(block)
    return result.hexdigest()


def restore_one(name, folder, output):
    started = time.monotonic()
    manifest_path = ROOT / "docs" / f"section5-certificate-chunks-{name}.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    source_path = ROOT / "supplementary" / "section5" / "certificates" / folder / "word_base.json"
    raw = source_path.read_bytes()
    source_hash = hashlib.sha256(raw).hexdigest()
    if source_hash != manifest["source_sha256"]:
        raise ValueError(f"{name}: original JSON hash differs from manifest")
    data = json.loads(raw)
    depth = data["candidate"]["n"]
    bits = 6 * (depth + 1) + 12
    if (manifest["name"], manifest["depth"], manifest["packing_bits"],
            manifest["states_per_checkpoint"]) != (name, depth, bits, depth + 1):
        raise ValueError(f"{name}: inconsistent depth, width or state count")
    steps = manifest["chunk_steps"]
    per_module = manifest["chunks_per_module"]
    if steps <= 0 or per_module <= 0:
        raise ValueError(f"{name}: invalid chunk shape")
    entries = [entry for entry in manifest["modules"]
               if entry["module"].startswith(f"Section5MassChunkData{name}")]
    expected_checkpoints = (depth + steps - 1) // steps + 1
    expected_modules = (expected_checkpoints - 2 + per_module) // per_module
    if manifest["checkpoints"] != expected_checkpoints or len(entries) != expected_modules:
        raise ValueError(f"{name}: incomplete checkpoint/module manifest")

    # The original Base19 manifest predates import decoupling. Base661 records
    # independent_data_from_batch=2, preserving its already checked batch01.
    # The other two manifests explicitly record independent_data_from_batch=1.
    independent_from = manifest.get("independent_data_from_batch")
    if independent_from is not None and independent_from < 1:
        raise ValueError(f"{name}: invalid historical import layout")
    namespace = f"Universality.Certificates.MassChunks{name}"
    options = ("set_option maxHeartbeats 0\n"
               "set_option maxRecDepth 100000\n"
               "set_option exponentiation.threshold 10000\n"
               "set_option Elab.async false\n\n")
    provenance = (
        f"/-! Exact checkpoint witnesses from supplementary/section5/certificates/{folder}.\n"
        f"word_base.json SHA256: {source_hash}\n"
        f"Packing width {bits} is fixed by original depth {depth}; all {depth + 1} states\n"
        "are retained in source order. Numerical witnesses require kernel proofs. -/\n\n")
    directory = output / "Universality" / "Certificates"
    directory.mkdir(parents=True, exist_ok=True)
    current = initial_checkpoint(data, bits)
    processed = 0
    restored = []
    for batch, entry in enumerate(entries):
        module = f"Section5MassChunkData{name}{batch:02d}"
        if entry["module"] != module:
            raise ValueError(f"{name}: unexpected data-module name/order")
        if batch == 0:
            imports = ("import Universality.Certificates.Section5MassChunks\n"
                       f"import Universality.Certificates.Section5Input{name}\n\n")
        elif independent_from is not None and batch >= independent_from:
            imports = "import Universality.Certificates.Section5MassChunks\n\n"
        else:
            imports = f"import Universality.Certificates.Section5MassChunkData{name}{batch - 1:02d}\n\n"
        parts = [imports, provenance, f"namespace {namespace}\n\n", options]
        if batch == 0:
            parts.append(render_checkpoint("checkpoint0000", current,
                                           manifest["limb_bits"], manifest["raw_literals"]))
        for _ in range(per_module):
            if processed == depth:
                break
            finish = min(processed + steps, depth)
            while processed < finish:
                current = step_checkpoint(current, bits)
                processed += 1
            parts.append(render_checkpoint(f"checkpoint{processed:04d}", current,
                                           manifest["limb_bits"], manifest["raw_literals"]))
        parts.append(f"end {namespace}\n")
        payload = "".join(parts).replace("\n", "\r\n").encode("utf-8")
        actual_hash = hashlib.sha256(payload).hexdigest()
        if actual_hash != entry["sha256"] or len(payload) != entry["bytes"]:
            raise ValueError(f"{module}: generated bytes do not match archived manifest "
                             f"(SHA256 {actual_hash}, bytes {len(payload)})")
        destination = directory / (module + ".lean")
        with destination.open("xb") as stream:
            stream.write(payload)
        written_hash = digest(destination)
        if written_hash != entry["sha256"]:
            raise ValueError(f"{module}: saved bytes failed independent readback")
        restored.append({"module": module, "path": destination.relative_to(output).as_posix(),
                         "bytes": len(payload), "source_sha256": entry["sha256"],
                         "reconstructed_sha256": written_hash,
                         "manifest_sha256_match": True})
        print(f"RESTORED {module} {len(payload)} bytes SHA256={written_hash}", flush=True)
        del payload, parts
    if processed != depth or current.depth != 0:
        raise ValueError(f"{name}: incomplete reconstructed chain")
    return {"name": name, "source_sha256": source_hash,
            "manifest_sha256": digest(manifest_path), "checkpoints": expected_checkpoints,
            "independent_data_from_batch": independent_from,
            "elapsed_seconds": round(time.monotonic() - started, 3), "modules": restored}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", required=True, type=Path,
                        help="separate empty directory; existing files are never overwritten")
    parser.add_argument("--name", action="append", choices=list(NAMES.values()),
                        help="restore only this seed (repeatable); default restores all four")
    args = parser.parse_args()
    output = args.output_dir.resolve()
    if output == ROOT.resolve() or output == (ROOT / "Universality").resolve():
        parser.error("output must be separate from the repository's checked source tree")
    if output.exists() and (not output.is_dir() or any(output.iterdir())):
        parser.error("output directory must be absent or empty")
    output.mkdir(parents=True, exist_ok=True)
    selected = set(args.name or NAMES.values())
    started = datetime.now().astimezone().isoformat(timespec="seconds")
    timer = time.monotonic()
    results = [restore_one(name, folder, output) for folder, name in NAMES.items() if name in selected]
    report = {"status": "pass",
              "scope": "Pure generated data source restoration, not a new Lean compilation or proof",
              "started": started, "finished": datetime.now().astimezone().isoformat(timespec="seconds"),
              "elapsed_seconds": round(time.monotonic() - timer, 3),
              "output_directory": str(output), "newline_encoding": "UTF-8 with CRLF",
              "restore_script_sha256": digest(Path(__file__)),
              "generator_sha256": digest(ROOT / "scripts" / "section5_certificate_chunks.py"),
              "file_count": sum(len(item["modules"]) for item in results),
              "files": [entry for item in results for entry in item["modules"]],
              "bytes": sum(entry["bytes"] for item in results for entry in item["modules"]),
              "manifests": [{"name": item["name"],
                              "path": f"docs/section5-certificate-chunks-{item['name']}.json",
                              "sha256": item["manifest_sha256"]} for item in results],
              "source_inputs": [{"name": item["name"],
                                  "path": f"supplementary/section5/certificates/{folder}/word_base.json",
                                  "sha256": item["source_sha256"]}
                                 for item in results for folder, name in NAMES.items() if name == item["name"]],
              "results": results}
    with (output / "section5-chunk-data-restoration.json").open("x", encoding="utf-8") as stream:
        json.dump(report, stream, indent=2)
        stream.write("\n")
    print(json.dumps({key: report[key] for key in ["status", "file_count", "bytes", "elapsed_seconds"]}), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
