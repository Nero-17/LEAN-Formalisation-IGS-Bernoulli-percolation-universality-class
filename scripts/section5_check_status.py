"""Report fixed-certificate checks against the current source bytes.

This reads compiler receipts; it does not evaluate mathematical claims or
replace a dependency-closure build. In-progress and stale checks stay open.
"""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAGES = (
    "Input", "Rows", "Disjoint", "PacketCapacity", "Data", "Counts",
    "Groups", "Length", "Responses", "Moments", "InitialMass", "Mass",
)
KEYS = ("Base19", "Base661", "Base739", "Shifted19")


def main():
    receipts = json.loads((ROOT / "docs/section5-certificate-kernel-checks.json")
                          .read_text(encoding="utf-8-sig"))
    records = []
    for key in KEYS:
        for stage in STAGES:
            module = f"Universality/Certificates/Section5{stage}{key}.lean"
            source = ROOT / module
            if not source.exists():
                continue
            digest = hashlib.sha256(source.read_bytes()).hexdigest()
            matching = [entry for entry in receipts if entry["module"] == module
                        and entry["source_sha256"] == digest]
            latest = matching[-1] if matching else None
            object_file = ROOT / ".lake/build/lib/lean" / Path(module).with_suffix(".olean")
            passed = bool(latest and latest["exit_code"] == 0
                          and latest["source_unchanged_during_check"]
                          and object_file.exists())
            records.append({"seed": key, "stage": stage, "module": module,
                            "source_sha256": digest, "current_source_passed": passed,
                            "last_matching_receipt": latest["finished"] if latest else None,
                            "elapsed_seconds": latest["elapsed_seconds"] if latest else None})
    report = {"checked_at_utc": datetime.now(timezone.utc).isoformat(),
              "scope": "Current source receipts only; not a dependency-closure or axiom audit.",
              "records": records}
    (ROOT / "docs/section5-certificate-status.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for key in KEYS:
        group = [entry for entry in records if entry["seed"] == key]
        passed = [entry["stage"] for entry in group if entry["current_source_passed"]]
        pending = [entry["stage"] for entry in group if not entry["current_source_passed"]]
        print(f"{key}: passed={','.join(passed) or 'none'}; open={','.join(pending) or 'none'}")


if __name__ == "__main__":
    main()
