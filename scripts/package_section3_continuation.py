"""Archive this ongoing round once, retaining honest build status and full source."""
from pathlib import Path
import hashlib
import json
import os
import zipfile

root = Path(__file__).resolve().parents[1]
state = json.loads((root / 'SECTION3_CONTINUATION_STATE.json').read_text(encoding='utf-8-sig'))
destination = root.parent / f"universality_class_{state['round']}_2026-10-06_完整研究记录.zip"
excluded = {'.git', '.lake', '__pycache__', 'scratch', 'logs'}
with zipfile.ZipFile(destination, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
    for directory, directories, files in os.walk(root):
        directories[:] = sorted(name for name in directories if name not in excluded)
        for name in sorted(files):
            path = Path(directory) / name
            archive.write(path, path.relative_to(root).as_posix())
    for log in ('section3-continuation-build.log',):
        path = root / 'logs' / log
        if path.exists():
            archive.write(path, 'build-evidence/' + log)
with zipfile.ZipFile(destination) as archive:
    assert archive.testzip() is None
    assert len(archive.namelist()) == len(set(archive.namelist()))
    assert f"docs/{state['round']}_完整研究记录.md" in archive.namelist()
print(json.dumps({'archive': str(destination), 'bytes': destination.stat().st_size,
    'sha256': hashlib.sha256(destination.read_bytes()).hexdigest(),
    'round': state['round'], 'status': state['status']}, ensure_ascii=False, indent=2))
