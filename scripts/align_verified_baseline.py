"""Restore exact verified baseline bytes after Windows checkout newline conversion.

No mathematical text may differ. Every source must match the saved successful
build hash at the source path, and removing CR bytes must make both copies equal.
"""
from pathlib import Path
import hashlib
import json

root = Path(__file__).resolve().parents[1]
source = Path('C:/Users/lzysh/Documents/Codex/2026-09-13/new-chat/work/universality-lean')
manifest = json.loads((root/'docs/section5-baseline-build-results.json').read_text(encoding='utf-8-sig'))
digest = lambda data: hashlib.sha256(data).hexdigest()
replacements = []
for entry in manifest:
    target = root/entry['module']
    current = target.read_bytes()
    if digest(current) == entry['source_sha256']:
        continue
    candidates = [current.replace(b'\r\n', b'\n'), current.replace(b'\r', b''),
                  (source/entry['module']).read_bytes()]
    verified = next((data for data in candidates if digest(data) == entry['source_sha256']), None)
    assert entry['exit_code'] == 0
    assert verified is not None, entry['module']
    assert current.replace(b'\r', b'') == verified.replace(b'\r', b''), entry['module']
    replacements.append((target, verified, {'module': entry['module'],
        'checkout_sha256': digest(current), 'verified_sha256': digest(verified),
        'change': 'CR newline bytes only; exact baseline source hash restored'}))
for target, verified, _ in replacements:
    target.write_bytes(verified)
(root/'docs/section5-baseline-byte-alignment.json').write_text(
    json.dumps({'count': len(replacements), 'source': str(source),
                'entries': [entry for _, _, entry in replacements]}, indent=2), encoding='utf8')
print(f'Restored exact verified bytes for {len(replacements)} baseline sources; mathematical text unchanged.')
