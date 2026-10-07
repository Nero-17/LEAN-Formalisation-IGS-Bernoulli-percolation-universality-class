"""Run the original integer-only verifier without rewriting supplementary inputs."""
from pathlib import Path
import runpy
import json
from datetime import datetime, timezone

root = Path(__file__).resolve().parents[1]
certificates = root / 'supplementary' / 'section5' / 'certificates'
verify = runpy.run_path(str(certificates / 'verify.py'))['verify']
results = [verify(certificates / folder, base, depth, scale_offset=offset)
           for folder, base, depth, offset in
           [('n424', 19, 424, 0), ('n936', 661, 936, 0),
            ('n952', 739, 952, 0), ('transcendental', 19, 424, 480)]]
target = root / 'logs' / 'section5-independent-integer-verification.json'
target.parent.mkdir(exist_ok=True)
target.write_text(json.dumps({'checked_at_utc': datetime.now(timezone.utc).isoformat(),
                              'scope': 'Python arithmetic support; not a substitute for Lean proof',
                              'results': results}, indent=2), encoding='utf8')
print(str(target))
