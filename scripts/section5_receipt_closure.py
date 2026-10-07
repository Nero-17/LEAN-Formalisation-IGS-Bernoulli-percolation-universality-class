"""Read-only receipt classifier and replay selector. Never runs Lean or fabricates success.

snapshot_module is also a future build-wrapper hook: record it before and after
checking, require equality, and separately record output_artifacts on success.
External package transitive closure remains the pinned package baseline's scope.
"""
from pathlib import Path
import argparse
from datetime import datetime, timezone
import hashlib
import json
import re
import subprocess
from functools import lru_cache

ROOT = Path(__file__).resolve().parents[1]
LEAN_BIN = Path("C:/Users/lzysh/.elan/toolchains/leanprover--lean4---v4.32.1/bin")
PACKAGE_CACHE = Path("C:/Users/lzysh/Documents/Codex/lean32/packages")


def sha(path):
    if not path.is_file():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def uncomment(text):
    result, index, depth = [], 0, 0
    while index < len(text):
        pair = text[index:index + 2]
        if pair == "/-":
            depth += 1; index += 2
        elif depth and pair == "-/":
            depth -= 1; index += 2
        elif not depth and pair == "--":
            end = text.find("\n", index)
            index = len(text) if end < 0 else end
        else:
            result.append(text[index] if not depth or text[index] == "\n" else " ")
            index += 1
    if depth:
        raise ValueError("unclosed comment")
    return "".join(result)


def imports(path):
    result, depth = [], 0
    # Imports are restricted to the header. Fail rather than guessing unsupported syntax.
    with path.open(encoding="utf-8-sig") as handle:
        for line in handle:
            cleaned, index = [], 0
            while index < len(line):
                pair = line[index:index + 2]
                if pair == "/-":
                    depth += 1; index += 2
                elif depth and pair == "-/":
                    depth -= 1; index += 2
                elif not depth and pair == "--":
                    break
                else:
                    if not depth:
                        cleaned.append(line[index])
                    index += 1
            line = "".join(cleaned).strip()
            if not line or line == "prelude" or line == "module":
                continue
            match = re.fullmatch(r"(?:(?:public|private)\s+)?import\s+(.+)", line)
            if not match:
                if line.startswith(("import", "public import", "private import")):
                    raise ValueError(f"unsupported import syntax: {path}: {line}")
                break
            for name in match[1].split():
                if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*", name):
                    raise ValueError(f"unsupported import token {name!r}: {path}")
                result.append(name)
    return result


def local_closure(root, target):
    visited, active, order = set(), set(), []
    def visit(module):
        if module in active:
            raise ValueError(f"import cycle: {module}")
        if module in visited:
            return
        active.add(module)
        for name in imports(root / module):
            if name == "Universality" or name.startswith("Universality."):
                visit(name.replace(".", "/") + ".lean")
        active.remove(module); visited.add(module); order.append(module)
    visit(target)
    return order


def artifact_hashes(path):
    # LeanChecker can consume these extra parts when present; bind them too.
    return {str(candidate): sha(candidate) for candidate in
            [path, Path(str(path) + ".server"), Path(str(path) + ".private")]}


def output_artifacts(root, module):
    return artifact_hashes(root / ".lake/build/lib/lean" / Path(module).with_suffix(".olean"))


@lru_cache(maxsize=1)
def compiler_version():
    return subprocess.check_output([str(LEAN_BIN / "lean.exe"), "--version"], text=True).strip()


def package_search_paths():
    # Match check.ps1's actual PowerShell enumeration, rather than assume Python order.
    command = "Get-ChildItem -LiteralPath '" + str(PACKAGE_CACHE).replace("'", "''") + "' -Directory | ForEach-Object { $_.FullName }"
    output = subprocess.check_output(["pwsh", "-NoProfile", "-Command", command], text=True)
    return [Path(line) / ".lake/build/lib/lean" for line in output.splitlines() if line]


def snapshot_module(root, module):
    root = Path(root)
    order = local_closure(root, module)
    for relative in order:
        if relative != module and not (root / ".lake/build/lib/lean" / Path(relative).with_suffix(".olean")).is_file():
            raise FileNotFoundError(f"missing local imported object: {relative}")
    search = [root / ".lake/build/lib/lean"] + package_search_paths()
    external = sorted({name for relative in order for name in imports(root / relative)
                       if not (name == "Universality" or name.startswith("Universality."))})
    external_objects = {}
    for name in external:
        relative = Path(name.replace(".", "/") + ".olean")
        candidates = [p / relative for p in search + [LEAN_BIN.parent / "lib/lean"] if (p / relative).exists()]
        if not candidates:
            raise FileNotFoundError(f"unresolved external import: {name}")
        external_objects[name] = {"resolved": str(candidates[0]), "artifacts": artifact_hashes(candidates[0]),
                                  "other_candidates": [str(p) for p in candidates[1:]]}
    return {"schema": 1, "module": module, "source_sha256": sha(root / module),
            "local_imports": [{"module": relative, "source_sha256": sha(root / relative),
                               "artifacts": output_artifacts(root, relative)} for relative in order if relative != module],
            "external_direct_imports": external_objects,
            "compiler_sha256": sha(LEAN_BIN / "lean.exe"),
            "check_script_sha256": sha(root / "scripts/check.ps1"),
            "compiler_version": compiler_version(),
            "search_path": [str(p) for p in search],
            "package_manifest_sha256": sha(root / "lake-manifest.json"),
            "scope": "Complete local closure; direct external objects. External transitive closure relies on pinned baseline."}


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def receipt_time(entry):
    value = entry.get("finished") or entry.get("finished_at_utc") or entry.get("checked_at_utc")
    return datetime.fromisoformat(value.replace("Z", "+00:00")) if value else None


def receipt_module(entry):
    name = entry["module"]
    return name if name.endswith(".lean") else name.replace(".", "/") + ".lean"


def evidence_reference(origin, entry):
    # Immutable identity inside the original append-only/history file. Never
    # rewrite a historical compile as a new successful execution.
    canonical = json.dumps(entry, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return {"receipt_file": "docs/" + origin, "entry_sha256": hashlib.sha256(canonical).hexdigest(),
            "original_module": entry["module"], "source_sha256": entry.get("source_sha256"),
            "exit_code": entry.get("exit_code"), "started": entry.get("started") or entry.get("started_at_utc"),
            "finished": entry.get("finished") or entry.get("finished_at_utc") or entry.get("checked_at_utc"),
            "source_unchanged_during_check": entry.get("source_unchanged_during_check"),
            "dependencies_unchanged_during_check": entry.get("dependencies_unchanged_during_check"),
            "recorded_olean_sha256": entry.get("olean_sha256"),
            "recorded_output_artifacts": entry.get("output_artifacts"),
            "log_path": entry.get("log"),
            "embedded_output_sha256": hashlib.sha256(entry["output"].encode("utf-8")).hexdigest() if "output" in entry else None,
            "recorded_at_utc": entry.get("recorded_at_utc"),
            "has_dependency_snapshots": bool(entry.get("snapshot_before")),
            "scope": "Reference to genuine historical execution; null means not recorded, not verified."}


def classify(root, target):
    receipts = []
    for filename in ["section5-certificate-kernel-checks.json", "build-results.json", "section5-symbolic-build-results.json",
                     "section5-core-build-results.json", "section5-baseline-build-results.json"]:
        path = root / "docs" / filename
        if path.exists():
            receipts.extend((filename, entry) for entry in read_json(path))
    for filename in ["section5-geometry-integration-receipt.json",
                     "section5-physical-integration-receipt.json",
                     "section5-arithmetic-integration-receipt.json"]:
        integration = root / "docs" / filename
        if integration.exists():
            integration_data = read_json(integration)
            receipts.extend((filename, entry) for entry in integration_data.get("builds", []))
            receipts.extend((filename, entry) for entry in integration_data.get("local_checks", []))
            bridge = integration_data.get("local_bridge_check")
            if isinstance(bridge, dict) and "module" in bridge:
                receipts.append((filename, bridge))
    result = []
    all_sources = [path.relative_to(root).as_posix() for path in root.glob("Universality/**/*.lean")]
    by_module = {}
    for origin, entry in receipts:
        by_module.setdefault(receipt_module(entry), []).append((origin, entry))
    for module in local_closure(root, target):
        current = sha(root / module)
        matches = []
        for origin, entry in by_module.get(module, []):
            if entry.get("exit_code") == 0 and entry.get("source_sha256") == current and entry.get("source_unchanged_during_check", True) and entry.get("dependencies_unchanged_during_check", True) and (
                    not entry.get("snapshot_before") or entry.get("snapshot_before") == entry.get("snapshot_after")):
                matches.append((origin, entry))
        objects = output_artifacts(root, module)
        object_exists = next(iter(objects.values())) is not None
        strong = [entry for _, entry in matches if object_exists and entry.get("snapshot_before") and
                  entry.get("snapshot_before") == entry.get("snapshot_after") == snapshot_module(root, module) and
                  entry.get("output_artifacts") == objects]
        notes = []
        if not strong:
            recorded_strong = [entry for _, entry in matches if entry.get("snapshot_before")]
            if recorded_strong:
                latest_strong = max(recorded_strong, key=lambda entry: receipt_time(entry) or datetime.min.replace(tzinfo=timezone.utc))
                if latest_strong.get("output_artifacts") != objects:
                    notes.append({"kind": "recorded_artifact_set_differs", "detail": "A previously bound olean/private/server output set differs from current objects."})
                try:
                    current_snapshot = snapshot_module(root, module)
                except (ValueError, FileNotFoundError) as error:
                    current_snapshot = {"snapshot_error": str(error)}
                if latest_strong["snapshot_before"] != current_snapshot:
                    notes.append({"kind": "recorded_dependency_snapshot_differs", "detail": "Previously bound dependency, external object, compiler or environment hashes differ; inspect exact snapshots."})
        dated = [(receipt_time(entry), entry) for _, entry in matches if receipt_time(entry)]
        if dated and not strong:
            finished, latest = max(dated, key=lambda item: item[0])
            object_path = Path(next(iter(objects)))
            if object_path.exists() and object_path.stat().st_mtime > finished.timestamp() + 2:
                notes.append({"kind": "object_written_after_historical_success",
                              "detail": "Timestamp evidence only: inspect later receipts before considering replay."})
            if latest.get("olean_sha256") and latest["olean_sha256"] != next(iter(objects.values())):
                notes.append({"kind": "recorded_output_hash_differs", "detail": "Find a later genuine compile receipt or consider exact-object replay."})
            for name in imports(root / module):
                if name == "Universality" or name.startswith("Universality."):
                    dependency = name.replace(".", "/") + ".lean"
                    prior = [(receipt_time(entry), entry) for _, entry in by_module.get(dependency, [])
                             if entry.get("exit_code") == 0 and receipt_time(entry) and receipt_time(entry) <= finished]
                    if prior:
                        _, previous = max(prior, key=lambda item: item[0])
                        if previous.get("source_sha256") != sha(root / dependency):
                            notes.append({"kind": "dependency_source_hash_changed_since_prior_receipt", "dependency": dependency,
                                          "detail": "Inspect source diff: byte differences alone may be newline-only, not substantive."})
        status = "dependency_bound_success" if strong else (
            "historical_success_with_specific_changes_to_review" if matches and object_exists and notes else
            "historical_success_retained" if matches and object_exists else "source_compile_needed")
        module_name = module[:-5].replace("/", ".")
        has_submodules = any(path.startswith(module[:-5] + "/") for path in all_sources)
        result.append({"module": module, "source_sha256": current, "current_artifacts": objects,
                       "status": status, "matching_receipt_origins": sorted({origin for origin, _ in matches}),
                       "historical_evidence": [evidence_reference(origin, entry) for origin, entry in matches],
                       "historical_dependency_notes": notes,
                       "suggested_replay": None if not notes or not object_exists or has_submodules else
                       "leanchecker " + module_name,
                       "replay_warning": "Candidate only after reviewing concrete changes. Missing legacy hash fields alone do not require replay. Set recorded LEAN_PATH; avoid prefix-wide parallel selection."})
    return {"target": target, "created_utc": datetime.now(timezone.utc).isoformat(), "modules": result,
            "scope": "Selector only: no compilation or replay executed. Legacy success is not promoted to closure verification."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", help="Repository-relative .lean target")
    parser.add_argument("--snapshot", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = snapshot_module(ROOT, args.target) if args.snapshot else classify(ROOT, args.target)
    text = json.dumps(result, indent=2)
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text)
