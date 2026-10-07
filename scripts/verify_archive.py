"""Check the delivered ZIP against the successful source audit, without extraction."""
from pathlib import Path
import hashlib
import json
import zipfile

root = Path(__file__).resolve().parents[1]
archive_path = root.parent / "universality_class_R071_2026-10-06_完整研究记录.zip"
errors = []
with zipfile.ZipFile(archive_path) as archive:
    names = archive.namelist()
    if len(names) != len(set(names)):
        errors.append("Duplicate archive entries")
    bad = archive.testzip()
    if bad:
        errors.append("CRC failure: " + bad)
    for name in names:
        parts = Path(name).parts
        if any(part in {".lake", ".git", "scratch", "logs"} for part in parts):
            errors.append("Excluded runtime content: " + name)
        if name.startswith(("/", "\\")) or ".." in parts:
            errors.append("Invalid relative archive path: " + name)
    audit = json.loads(archive.read("docs/source-audit.json").decode("utf-8-sig"))
    if not audit["ok"]:
        errors.append("Packaged source audit did not pass")
    for item in audit["sources"]:
        actual = hashlib.sha256(archive.read(item["module"])).hexdigest()
        if actual != item["source_sha256"]:
            errors.append("Packaged source differs from checked source: " + item["module"])
    reports = [name for name in names if name.endswith("R071_完整研究记录.md")]
    if len(reports) != 1:
        errors.append("Expected exactly one authoritative round report")
    state = json.loads(archive.read("ROUND_STATE.json").decode("utf-8-sig"))
    if state["archive_file_id"] != "1ZJnVn-1C6MNLFzYfGkekj728D8siwE91":
        errors.append("Unexpected archive identity")
print(json.dumps({
    "ok": not errors,
    "archive": str(archive_path),
    "bytes": archive_path.stat().st_size,
    "sha256": hashlib.sha256(archive_path.read_bytes()).hexdigest(),
    "file_count": len(names),
    "verified_source_count": audit["module_count"],
    "round_status": state["status"],
    "errors": errors,
}, ensure_ascii=False, indent=2))
raise SystemExit(0 if not errors else 1)
