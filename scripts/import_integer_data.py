"""Import fixed manuscript integers as Lean literals; no proof is imported."""
from pathlib import Path
import hashlib
import json
import sys

sys.set_int_max_str_digits(0)
project = Path(__file__).resolve().parents[1]
source = project.parent / 'overleaf-universality' / 'certificates'
destination = project / 'Universality' / 'Certificates' / 'Data'
destination.mkdir(parents=True, exist_ok=True)
manifest = []
for folder, name, offset in [
    ('n424', 'Base19', 0), ('n936', 'Base661', 0),
    ('n952', 'Base739', 0), ('transcendental', 'Shifted19', 480),
]:
    path = source / folder / 'word_base.json'
    content = path.read_bytes()
    data = json.loads(content)
    candidate = data['candidate']
    literals = ',\n    '.join(str(x) for x in data['Nz'])
    text = f'''import Universality.Certificates.IntegerMoments

/-! Fixed integer data imported from manuscript certificates/{folder}/word_base.json.
SHA256: {hashlib.sha256(content).hexdigest()}
The theorem below is checked by Lean; this generator supplies no proof oracle. -/

namespace Universality.Certificates

def certificate{name} : IntegerMomentCertificate where
  depth := {candidate['n']}
  base := {candidate['s']}
  scaleOffset := {offset}
  zeroTotals := [
    {literals}]

set_option maxHeartbeats 0 in
set_option maxRecDepth 100000 in
set_option exponentiation.threshold 4096 in
theorem certificate{name}_integer_moments : certificate{name}.valid := by
  decide

end Universality.Certificates
'''
    target = destination / f'{name}.lean'
    target.write_text(text, encoding='utf-8')
    manifest.append({'source':str(path), 'sha256':hashlib.sha256(content).hexdigest(),
                     'lean':str(target.relative_to(project)), 'entries':len(data['Nz'])})
(project / 'docs' / 'certificate-inputs.json').write_text(
    json.dumps(manifest, indent=2, ensure_ascii=False), encoding='utf-8')
print(json.dumps(manifest, ensure_ascii=False, indent=2))
