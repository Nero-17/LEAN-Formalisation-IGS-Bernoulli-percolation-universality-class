"""Update the single Section 2 round ZIP; never overwrite R071's archive."""
from pathlib import Path
import json
import os
import zipfile

root = Path(__file__).resolve().parents[1]
state = json.loads((root / 'SECTION2_ROUND_STATE.json').read_text(encoding='utf-8-sig'))
destination = root.parent / f"universality_class_{state['round']}_2026-10-06_完整研究记录.zip"
excluded = {'.git', '.lake', '__pycache__', 'scratch', 'logs'}
with zipfile.ZipFile(destination, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
    for directory, directories, files in os.walk(root):
        directories[:] = sorted(name for name in directories if name not in excluded)
        for name in sorted(files):
            path = Path(directory) / name
            archive.write(path, str(path.relative_to(root)))
with zipfile.ZipFile(destination) as archive:
    assert archive.testzip() is None
    assert len(archive.namelist()) == len(set(archive.namelist()))
    assert f"docs/{state['round']}_完整研究记录.md" in archive.namelist()
print(destination)
print(f'Bytes: {destination.stat().st_size}')
