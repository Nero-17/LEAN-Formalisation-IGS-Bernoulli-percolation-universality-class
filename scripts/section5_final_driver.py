"""Final incremental closure driver. Planning is default; execution is explicit.

Historical receipts remain historical. This driver never fabricates a compiler
receipt and never invokes leanchecker or retries old numerical checks on its own.
"""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from section5_receipt_closure import ROOT, classify, imports, sha, output_artifacts, artifact_hashes, package_search_paths, LEAN_BIN, snapshot_module, local_closure
from section5_final_axiom_report import parse

AUDIT = "Section5FinalKernelAudit.lean"


def environment_fingerprint():
    order = local_closure(ROOT, AUDIT)
    search = [ROOT / ".lake/build/lib/lean"] + package_search_paths()
    external = sorted({name for relative in order for name in imports(ROOT / relative)
                       if not (name == "Universality" or name.startswith("Universality."))})
    objects = {}
    for name in external:
        relative = Path(name.replace(".", "/") + ".olean")
        candidates = [folder / relative for folder in search + [LEAN_BIN.parent / "lib/lean"] if (folder / relative).exists()]
        if not candidates:
            raise FileNotFoundError(f"Unresolved external import: {name}")
        objects[name] = {"resolved": str(candidates[0]), "artifacts": artifact_hashes(candidates[0]),
                         "other_candidates": [str(path) for path in candidates[1:]]}
    return {"compiler": sha(LEAN_BIN / "lean.exe"), "check_script": sha(ROOT / "scripts/check.ps1"),
            "manifest": sha(ROOT / "lake-manifest.json"), "search_path": [str(path) for path in search],
            "external_direct_imports": objects,
            "scope": "Direct external imports and compiler/build configuration; transitive package baseline remains separately pinned."}


def make_plan(classification, decisions):
    entries = []
    rebuild = set()
    environment = environment_fingerprint()
    closure_state = {item["module"]: {key: item[key] for key in ["module", "source_sha256", "current_artifacts"]}
                     for item in classification["modules"]}
    for item in classification["modules"]:
        module = item["module"]
        dependencies = [name.replace(".", "/") + ".lean" for name in imports(ROOT / module)
                        if name == "Universality" or name.startswith("Universality.")]
        changed_dependencies = [name for name in dependencies if name in rebuild]
        reasons = list(item["historical_dependency_notes"])
        if changed_dependencies and item["status"] != "source_compile_needed":
            reasons.append({"kind": "dependency_selected_for_source_compilation", "dependencies": changed_dependencies,
                            "detail": "Review whether its change is substantive before retaining this historical object."})
        action = "compile" if item["status"] == "source_compile_needed" or module == AUDIT else (
            "review" if reasons else "retain_history")
        context = {"local_closure": [closure_state[name] for name in local_closure(ROOT, module)],
                   "environment": environment}
        context_hash = hashlib.sha256(json.dumps(context, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
        decision = decisions.get(module)
        if decision is not None:
            if decision.get("source_sha256") != item["source_sha256"] or not decision.get("reason", "").strip():
                raise ValueError(f"Decision is not bound to current source and a written reason: {module}")
            if decision.get("current_artifacts") is not None and decision["current_artifacts"] != item["current_artifacts"]:
                raise ValueError(f"Decision object hashes no longer match: {module}")
            if decision.get("action") not in {"compile", "retain_history"}:
                raise ValueError(f"Invalid decision action: {module}")
            if decision["action"] == "retain_history" and (item["status"] == "source_compile_needed" or module == AUDIT):
                raise ValueError(f"Cannot retain missing evidence or skip executing final audit source: {module}")
            if decision["action"] == "retain_history" and reasons and decision.get("review_context_sha256") != context_hash:
                raise ValueError(f"Retention decision does not bind the current reviewed closure/environment: {module}")
            action = decision["action"]
        if action == "compile":
            rebuild.add(module)
        entries.append({**item, "action": action, "review_reasons": reasons, "review_context_sha256": context_hash, "explicit_decision": decision})
    unknown = set(decisions) - {entry["module"] for entry in entries}
    if unknown:
        raise ValueError(f"Decisions mention modules outside this closure: {sorted(unknown)}")
    blockers = []
    for manifest_path in sorted((ROOT / "docs").glob("section5-certificate-repair-chunks-*.json")):
        manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
        missing = ["Universality/Certificates/" + item["module"] + ".lean" for item in manifest["modules"]
                   if "Universality/Certificates/" + item["module"] + ".lean" not in closure_state]
        if missing:
            blockers.append({"kind": "bounded_repair_not_connected_to_final_imports",
                             "manifest": manifest_path.relative_to(ROOT).as_posix(), "missing_modules": missing,
                             "detail": "Wait for checked bounded-repair bridges. Do not execute an obsolete monolithic mass endpoint."})
    return {"created_utc": datetime.now(timezone.utc).isoformat(), "target": AUDIT,
            "scope": "Execution plan only. Retained historical success is not fresh compilation or upgraded hash evidence.",
            "modules": entries, "environment": environment, "execution_blockers": blockers}


def execute(plan, result_path):
    if plan.get("execution_blockers"):
        raise ValueError(f"Final import topology is not ready: {plan['execution_blockers']}")
    pending = [entry["module"] for entry in plan["modules"] if entry["action"] == "review"]
    if pending:
        raise ValueError(f"Unresolved specific dependency/object changes; inspect and supply hash-bound decisions: {pending}")
    if environment_fingerprint() != plan["environment"]:
        raise ValueError("Compiler/build/external environment changed after planning")
    # Check the entire frozen plan before starting. No source or object mutation is
    # hidden by choosing a later receipt after the human reviewed the plan.
    for entry in plan["modules"]:
        if sha(ROOT / entry["module"]) != entry["source_sha256"] or output_artifacts(ROOT, entry["module"]) != entry["current_artifacts"]:
            raise ValueError(f"Plan changed before execution: {entry['module']}")
    outcome = {"started_utc": datetime.now(timezone.utc).isoformat(), "status": "running", "entries": []}
    def save():
        result_path.write_text(json.dumps(outcome, indent=2), encoding="utf-8")
    save()
    fresh_outputs = {}
    for entry in plan["modules"]:
        module = entry["module"]
        if sha(ROOT / module) != entry["source_sha256"]:
            raise ValueError(f"Source changed during final execution: {module}")
        if entry["action"] == "retain_history":
            if output_artifacts(ROOT, module) != entry["current_artifacts"]:
                raise ValueError(f"Historical object changed during final execution: {module}")
            outcome["entries"].append({"module": module, "action": "retained_historical_evidence",
                                       "historical_evidence": entry["historical_evidence"],
                                       "explicit_decision": entry["explicit_decision"]})
            save()
            continue
        history_path = ROOT / "docs/section5-certificate-kernel-checks.json"
        previous_history = json.loads(history_path.read_text(encoding="utf-8")) if history_path.exists() else []
        previous_module_entries = [record for record in previous_history if record["module"] == module]
        invocation_started = datetime.now(timezone.utc).replace(microsecond=0)
        command = [sys.executable, str(ROOT / "scripts/section5_certificate_check.py"), module]
        process = subprocess.run(command, cwd=ROOT)
        outcome["entries"].append({"module": module, "action": "source_compiler_invoked", "exit_code": process.returncode,
                                   "receipt_file": "docs/section5-certificate-kernel-checks.json"})
        save()
        if process.returncode:
            outcome["status"] = "failed"; save()
            raise RuntimeError(f"Actual compiler/wrapper failed: {module}")
        history = json.loads((ROOT / "docs/section5-certificate-kernel-checks.json").read_text(encoding="utf-8"))
        module_entries = [record for record in history if record["module"] == module]
        if module_entries[:len(previous_module_entries)] != previous_module_entries or len(module_entries) != len(previous_module_entries) + 1:
            raise ValueError(f"Expected exactly one new immutable receipt from this invocation: {module}")
        fresh = module_entries[-1]
        if not (invocation_started <= datetime.fromisoformat(fresh["started"]) <= datetime.fromisoformat(fresh["finished"]) <= datetime.now(timezone.utc)):
            raise ValueError(f"Fresh receipt time is outside this invocation: {module}")
        if (fresh["source_sha256"] != entry["source_sha256"] or fresh["exit_code"] != 0 or
                not fresh.get("source_unchanged_during_check") or not fresh.get("dependencies_unchanged_during_check") or
                fresh.get("snapshot_before") != fresh.get("snapshot_after")):
            raise ValueError(f"New successful receipt is not bound to this stable source/dependency check: {module}")
        fresh_outputs[module] = fresh["output_artifacts"]
        if fresh_outputs[module] != output_artifacts(ROOT, module):
            raise ValueError(f"Newly compiled object already differs from its receipt: {module}")
        if module == AUDIT:
            receipt = fresh
            final_audit_snapshot = fresh["snapshot_after"]
            if receipt["source_sha256"] != entry["source_sha256"] or receipt["exit_code"] != 0:
                raise ValueError("Final audit receipt does not match this successful execution")
            log = result_path.with_suffix(".axioms.log")
            log.write_text(receipt["output"], encoding="utf-8")
            report = parse(log, receipt["exit_code"])
            result_path.with_suffix(".axioms.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
            if report["status"] != "dependency_audit_pass":
                outcome["status"] = "axiom_dependency_review_required"; save()
                raise ValueError("Unexpected GS dependency requires explicit mathematical review")
    for entry in plan["modules"]:
        if sha(ROOT / entry["module"]) != entry["source_sha256"]:
            raise ValueError(f"Source changed before final acceptance: {entry['module']}")
        if entry["action"] == "retain_history" and output_artifacts(ROOT, entry["module"]) != entry["current_artifacts"]:
            raise ValueError(f"Retained object changed before final acceptance: {entry['module']}")
    for module, recorded_outputs in fresh_outputs.items():
        if output_artifacts(ROOT, module) != recorded_outputs:
            raise ValueError(f"Newly compiled object changed before final acceptance: {module}")
    if environment_fingerprint() != plan["environment"]:
        raise ValueError("Compiler/build/external environment changed before final acceptance")
    if final_audit_snapshot != snapshot_module(ROOT, AUDIT):
        raise ValueError("Final audit dependency snapshot no longer matches current closure")
    outcome["status"] = "completed_with_retained_history_and_actual_new_checks"
    outcome["finished_utc"] = datetime.now(timezone.utc).isoformat()
    save()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--decisions", type=Path, help="JSON mapping module to source_sha256, action, and reason")
    parser.add_argument("--plan", type=Path, default=ROOT / "docs/section5-final-execution-plan.json")
    parser.add_argument("--result", type=Path, default=ROOT / "docs/section5-final-execution-result.json")
    parser.add_argument("--fresh", action="store_true", help="Explicitly select source rebuilding of the entire local closure; still plan-only unless --execute")
    parser.add_argument("--execute", action="store_true", help="Explicitly run selected source checks after plan review")
    args = parser.parse_args()
    decisions = json.loads(args.decisions.read_text(encoding="utf-8-sig")) if args.decisions else {}
    if args.fresh and decisions:
        parser.error("--fresh and historical-retention decisions cannot be combined")
    plan = make_plan(classify(ROOT, AUDIT), decisions)
    if args.fresh:
        for entry in plan["modules"]:
            entry["action"] = "compile"
        plan["mode"] = "explicit_fresh_source_rebuild"
    else:
        plan["mode"] = "incremental_with_transparent_historical_retention"
    args.plan.write_text(json.dumps(plan, indent=2), encoding="utf-8")
    from collections import Counter
    print(json.dumps(dict(Counter(item["action"] for item in plan["modules"]))))
    if args.execute:
        execute(plan, args.result)


if __name__ == "__main__":
    main()
