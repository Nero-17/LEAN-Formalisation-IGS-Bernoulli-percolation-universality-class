"""Run fixed-certificate Lean checks sequentially and retain exact evidence.

This is only a build/logging wrapper.  Proofs are checked by the pinned Lean
kernel through scripts/check.ps1; Python supplies no mathematical oracle.
"""
from pathlib import Path
from datetime import datetime
import argparse
import hashlib
import json
import subprocess
import sys
import time
import os
import msvcrt
import traceback
from section5_receipt_closure import snapshot_module, output_artifacts

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "docs" / "section5-certificate-kernel-checks.json"
LOCK = ROOT / "work" / "section5-kernel-checks.lock"
RUNS = ROOT / "docs" / "section5-kernel-runs"


def read_history():
    return json.loads(REPORT.read_text(encoding="utf-8")) if REPORT.exists() else []


def append_receipt(entry):
    """Serialize concurrent short-check/mass-check receipt updates."""
    LOCK.parent.mkdir(exist_ok=True)
    with LOCK.open("a+b") as lock:
        if lock.tell() == 0:
            lock.write(b"0")
            lock.flush()
        lock.seek(0)
        msvcrt.locking(lock.fileno(), msvcrt.LK_LOCK, 1)
        try:
            history = read_history()
            history.append(entry)
            temporary = REPORT.with_suffix(f".{os.getpid()}.tmp")
            temporary.write_text(json.dumps(history, indent=2, ensure_ascii=False), encoding="utf-8")
            os.replace(temporary, REPORT)
        finally:
            lock.seek(0)
            msvcrt.locking(lock.fileno(), msvcrt.LK_UNLCK, 1)


def save_run(path, record):
    """Persist a run journal before attempting any later, fallible audit step."""
    temporary = path.with_suffix(f".{os.getpid()}.tmp")
    with temporary.open("w", encoding="utf-8", newline="\n") as output:
        json.dump(record, output, indent=2, ensure_ascii=False)
        output.write("\n")
        output.flush()
        os.fsync(output.fileno())
    os.replace(temporary, path)


def checked_receipt(entry, relative, source_hash):
    """An explicitly failed or incomplete audit must never satisfy --skip-verified."""
    return (entry.get("module") == relative.as_posix() and
            entry.get("source_sha256") == source_hash and entry.get("exit_code") == 0 and
            entry.get("source_unchanged_during_check") is True and
            entry.get("dependencies_unchanged_during_check") is True and
            bool(entry.get("snapshot_before")) and
            entry.get("snapshot_before") == entry.get("snapshot_after") and
            entry.get("status", "pass") == "pass")


def run_module(relative, *, profile=False, threads=1):
    source = ROOT / relative
    source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    started = datetime.now().astimezone().isoformat(timespec="seconds")
    run_id = datetime.now().strftime("%Y%m%dT%H%M%S%f") + f"-{os.getpid()}-{relative.stem}"
    RUNS.mkdir(parents=True, exist_ok=True)
    run_path = RUNS / (run_id + ".json")
    log_path = RUNS / (run_id + ".log")
    command = ["pwsh", "-NoProfile", "-File", str(ROOT / "scripts" / "check.ps1"),
               "-Module", str(relative)]
    if profile:
        command.append("-Profile")
    if threads:
        command.extend(["-Threads", str(threads)])
    record = {"schema": 1, "status": "before_snapshot_pending", "run_id": run_id,
              "module": relative.as_posix(), "source_sha256": source_hash,
              "started": started, "command": command, "cwd": str(ROOT),
              "raw_output_path": log_path.relative_to(ROOT).as_posix(),
              "process_exit_code": None, "wrapper_exit_code": None,
              "scope": "Incomplete journal until status pass; a process exit alone is not a strong proof receipt."}
    save_run(run_path, record)
    try:
        snapshot_before = snapshot_module(ROOT, relative.as_posix())
    except Exception:
        record.update(status="before_snapshot_failed", wrapper_exit_code=1,
                      error=traceback.format_exc())
        save_run(run_path, record)
        print(record["error"], file=sys.stderr, flush=True)
        return 1
    record.update(status="ready_to_start", snapshot_before=snapshot_before)
    save_run(run_path, record)
    start_clock = time.monotonic()
    print(f"START {relative.as_posix()} {started} run={run_id}", flush=True)
    process = None
    output_bytes = bytearray()
    with log_path.open("xb") as raw_log:
        try:
            process = subprocess.Popen(command, cwd=ROOT, stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT)
            record.update(status="running", process_id=process.pid)
            save_run(run_path, record)
            for line in process.stdout:
                raw_log.write(line)
                raw_log.flush()
                output_bytes.extend(line)
                print(line.decode("utf-8", errors="replace"), end="", flush=True)
            returncode = process.wait()
        except BaseException:
            record.update(status="process_interrupted", error=traceback.format_exc())
            if process is not None and isinstance(sys.exception(), KeyboardInterrupt):
                process.terminate()
                remaining, _ = process.communicate()
                if remaining:
                    raw_log.write(remaining)
                    output_bytes.extend(remaining)
                record["process_exit_code"] = process.returncode
            elif process is not None:
                record["process_exit_code"] = process.poll()
            raw_log.flush()
            os.fsync(raw_log.fileno())
            record["elapsed_seconds"] = round(time.monotonic() - start_clock, 3)
            record["raw_output_sha256"] = hashlib.sha256(output_bytes).hexdigest()
            save_run(run_path, record)
            raise
        raw_log.flush()
        os.fsync(raw_log.fileno())
    elapsed = time.monotonic() - start_clock
    output = output_bytes.decode("utf-8", errors="replace")
    record.update(status="process_exited_audit_pending", process_exit_code=returncode,
                  process_finished=datetime.now().astimezone().isoformat(timespec="seconds"),
                  elapsed_seconds=round(elapsed, 3),
                  raw_output_sha256=hashlib.sha256(output_bytes).hexdigest(), output=output)
    # The real process status and byte-exact output are durable BEFORE snapshot_after.
    save_run(run_path, record)
    try:
        unchanged = source_hash == hashlib.sha256(source.read_bytes()).hexdigest()
        snapshot_after = snapshot_module(ROOT, relative.as_posix())
        dependencies_unchanged = snapshot_before == snapshot_after
        artifacts = output_artifacts(ROOT, relative.as_posix())
    except Exception:
        record.update(status="after_snapshot_failed", wrapper_exit_code=1,
                      error=traceback.format_exc())
        save_run(run_path, record)
        print(record["error"], file=sys.stderr, flush=True)
        print(f"INCOMPLETE {relative.name} process_exit={returncode}; after-snapshot failed; "
              f"durable journal={run_path.relative_to(ROOT).as_posix()}", flush=True)
        return 1
    wrapper_exit = returncode or (0 if unchanged and dependencies_unchanged else 1)
    entry = {"module": relative.as_posix(), "source_sha256": source_hash,
             "started": started, "finished": datetime.now().astimezone().isoformat(timespec="seconds"),
             "elapsed_seconds": round(elapsed, 3), "exit_code": returncode,
             "source_unchanged_during_check": unchanged,
             "dependencies_unchanged_during_check": dependencies_unchanged,
             "snapshot_before": snapshot_before, "snapshot_after": snapshot_after,
             "output_artifacts": artifacts, "output": output,
             "status": "pass" if wrapper_exit == 0 else "validation_failed",
             "wrapper_exit_code": wrapper_exit, "run_journal": run_path.relative_to(ROOT).as_posix(),
             "raw_output_path": log_path.relative_to(ROOT).as_posix(),
             "raw_output_sha256": record["raw_output_sha256"]}
    record.update(status="receipt_persistence_pending", receipt=entry,
                  wrapper_exit_code=wrapper_exit)
    save_run(run_path, record)
    append_receipt(entry)
    record["status"] = entry["status"]
    save_run(run_path, record)
    print(f"FINISH {relative.name} EXIT {returncode} {elapsed:.3f}s source_unchanged={unchanged} "
          f"dependencies_unchanged={dependencies_unchanged}", flush=True)
    return wrapper_exit


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", action="store_true", help="record Lean's per-declaration timings")
    parser.add_argument("--threads", type=int, default=1, help="Lean worker count; default one for numeric checks")
    parser.add_argument("--skip-verified", action="store_true", help="skip matching successful source receipts; not a dependency audit")
    parser.add_argument("modules", nargs="+", help="Section5 module basename or repository .lean path")
    args = parser.parse_args()
    for requested in args.modules:
        relative = (Path(requested) if requested.endswith(".lean") else
                    Path("Universality") / "Certificates" / (requested + ".lean"))
        source = ROOT / relative
        source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
        object_path = ROOT / ".lake" / "build" / "lib" / "lean" / relative.with_suffix(".olean")
        if args.skip_verified and object_path.exists() and any(
                checked_receipt(entry, relative, source_hash) for entry in read_history()):
            print(f"SKIP verified current source {relative.as_posix()}", flush=True)
            continue
        result = run_module(relative, profile=args.profile, threads=args.threads)
        if result:
            return result
    return 0


if __name__ == "__main__":
    sys.exit(main())
