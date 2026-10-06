"""Package and verify the single Section 3 round archive, without runtime caches."""
from pathlib import Path
import hashlib
import json
import os
import zipfile

root = Path(__file__).resolve().parents[1]
state = json.loads((root / 'SECTION3_ROUND_STATE.json').read_text(encoding='utf-8-sig'))
round_name = state['round']
destination = root.parent / f'universality_class_{round_name}_2026-10-06_完整研究记录.zip'
audit = json.loads((root / 'docs/source-audit.json').read_text(encoding='utf-8-sig'))
if not audit['ok']:
    raise SystemExit('Source audit must pass before packaging.')
for item in audit['sources']:
    if hashlib.sha256((root / item['module']).read_bytes()).hexdigest() != item['source_sha256']:
        raise SystemExit('Stale audit: ' + item['module'])
excluded = {'.git', '.lake', '__pycache__', 'scratch', 'logs'}
with zipfile.ZipFile(destination, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
    for directory, directories, files in os.walk(root):
        directories[:] = sorted(name for name in directories if name not in excluded)
        for name in sorted(files):
            path = Path(directory) / name
            archive.write(path, path.relative_to(root).as_posix())
with zipfile.ZipFile(destination) as archive:
    assert archive.testzip() is None
    assert len(archive.namelist()) == len(set(archive.namelist()))
    for item in audit['sources']:
        assert hashlib.sha256(archive.read(item['module'])).hexdigest() == item['source_sha256']
    assert f'docs/{round_name}_完整研究记录.md' in archive.namelist()
print(json.dumps({'archive': str(destination), 'bytes': destination.stat().st_size,
    'sha256': hashlib.sha256(destination.read_bytes()).hexdigest(),
    'verified_modules': audit['module_count'], 'round': round_name,
    'status': state['status']}, ensure_ascii=False, indent=2))
