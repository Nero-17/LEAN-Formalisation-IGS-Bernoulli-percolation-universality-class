"""Audit project source coverage against successful Lean build records.

This is a reproducibility check, not a substitute for Lean's kernel. Run after
build.ps1 (and after any supplemental build with -ReuseVerified).
"""
from pathlib import Path
import hashlib
import json
import re
from datetime import datetime

root = Path(__file__).resolve().parents[1]
imports = re.compile(r"^import (Universality(?:\.[A-Za-z0-9_]+)*)\s*$", re.M)
forbidden = re.compile(r"\b(?:sorry|admit|axiom|native_decide|sorryAx)\b")
visited = set()
order = []


def visit(module):
    if module in visited:
        return
    visited.add(module)
    source = (root / module).read_text(encoding="utf-8-sig")
    for dependency in imports.findall(source):
        visit(dependency.replace(".", "/") + ".lean")
    order.append(module)


visit("Audit.lean")
manifest = {entry["module"]: entry for entry in json.loads(
    (root / "docs/build-results.json").read_text(encoding="utf-8-sig"))}
errors = []
# Interrupted builds may recover only checks proven complete by the original
# fail-fast sequential log. Keep that exact log prefix as audit evidence.
recovered = [entry for entry in manifest.values() if entry.get("recovered_from_successful_sequential_check")]
if recovered:
    evidence_path = root / "docs/build-resume-evidence.json"
    evidence = json.loads(evidence_path.read_text(encoding="utf-8-sig"))
    log_path = root / "logs/section3-continuation-build.log"
    if not log_path.exists():
        log_path = root / "build-evidence/section3-continuation-build.log"
    prefix = log_path.read_bytes()[:evidence["interrupted_log_byte_length"]]
    if hashlib.sha256(prefix).hexdigest() != evidence["interrupted_log_sha256"]:
        errors.append("Interrupted-build evidence log prefix changed")
    completed = {entry["module"]: entry for entry in evidence["recovered_modules"]}
    starts = [line.removeprefix("Checking ") for line in prefix.decode("utf-8-sig").splitlines() if line.startswith("Checking ")]
    if set(completed) != set(starts[:-1]) or evidence["interrupted_module_not_counted"] != starts[-1]:
        errors.append("Recovered modules do not match completed sequential checks")
    for entry in recovered:
        original = completed.get(entry["module"], {})
        same_fields = {k: v for k, v in original.items() if k != "object_written_at_utc"} == {k: v for k, v in entry.items() if k != "object_written_at_utc"}
        same_time = datetime.fromisoformat(original["object_written_at_utc"]) == datetime.fromisoformat(entry["object_written_at_utc"])
        if not same_fields or not same_time:
            errors.append("Recovered build record changed: " + entry["module"])
checked = []
for module in order:
    source = (root / module).read_bytes()
    digest = hashlib.sha256(source).hexdigest()
    entry = manifest.get(module)
    if not entry:
        errors.append(f"Missing successful build record: {module}")
    elif entry.get("exit_code") != 0 or entry.get("source_sha256") != digest:
        errors.append(f"Failed or stale build record: {module}")
    text = source.decode("utf-8-sig")
    if forbidden.search(text):
        errors.append(f"Forbidden proof placeholder or native shortcut in {module}")
    if "trace_state" in text or "debug.skipKernelTC" in text:
        errors.append(f"Debug setting in {module}")
    checked.append({"module": module, "source_sha256": digest})

all_modules = {str(path.relative_to(root)).replace("\\", "/")
               for path in (root / "Universality").rglob("*.lean")}
canonical_modules = {module.casefold(): module for module in all_modules}
for module in visited:
    canonical = canonical_modules.get(module.casefold(), module)
    if canonical != module:
        errors.append("Import path case differs from actual source file: " + module + " versus " + canonical)
unreachable = sorted(all_modules - visited)
if unreachable:
    errors.append("Source modules outside Audit import closure: " + ", ".join(unreachable))

result = {
    "ok": not errors,
    "module_count": len(order),
    "certificate_batch_count": sum("/Opposite/Batch" in p or "/Opposite/Crossing" in p or "/CentralWheatstoneCertificates/Batch" in p for p in order),
    "milestone_axiom_audit_count": (root / "Audit.lean").read_text(encoding="utf-8-sig").count("#print axioms"),
    "errors": errors,
    "sources": checked,
}
(root / "docs/source-audit.json").write_text(
    json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
summary = {key: value for key, value in result.items() if key not in {"sources", "errors"}}
summary["error_count"] = len(errors)
summary["first_errors"] = errors[:10]
print(json.dumps(summary, ensure_ascii=False, indent=2))
raise SystemExit(0 if result["ok"] else 1)
