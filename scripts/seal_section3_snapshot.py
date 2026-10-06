"""Record post-build source/object/dependency integrity without claiming a new build."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,re
r=Path(__file__).resolve().parents[1]
audit=json.loads((r/'docs/source-audit.json').read_text(encoding='utf-8-sig'))
assert audit['ok'], 'Run successful complete build and verify_snapshot first'
manifest={e['module']:e for e in json.loads((r/'docs/build-results.json').read_text(encoding='utf-8-sig'))}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
entries={}
for checked in audit['sources']:
    name=checked['module'];source=r/name
    assert sha(source)==checked['source_sha256']==manifest[name]['source_sha256'],name
    obj=r/'.lake/build/lib/lean'/Path(name).with_suffix('.olean')
    assert obj.is_file(),str(obj)
    deps=[d.replace('.','/')+'.lean' for d in re.findall(r'^import (Universality(?:\.[A-Za-z0-9_]+)*)\s*$',source.read_text(encoding='utf-8-sig'),re.M)]
    for dep in deps:
        assert dep in entries,(name,dep)
        depobj=r/'.lake/build/lib/lean'/Path(dep).with_suffix('.olean')
        assert obj.stat().st_mtime_ns>=depobj.stat().st_mtime_ns,('stale object',name,dep)
    entries[name]={'source_sha256':sha(source),'object_sha256':sha(obj),'project_imports':deps,'dependency_fingerprints':{d:entries[d]['fingerprint'] for d in deps}}
    entries[name]['fingerprint']=hashlib.sha256(json.dumps(entries[name],sort_keys=True).encode()).hexdigest()
lean=Path('C:/Users/lzysh/.elan/toolchains/leanprover--lean4---v4.32.1/bin/lean.exe')
out={'sealed_at_utc':datetime.now(timezone.utc).isoformat(),'status':'post-build integrity seal; not a new compilation receipt','module_count':len(entries),'lean_binary_sha256':sha(lean),'environment':json.loads((r/'docs/build-metadata.json').read_text(encoding='utf-8-sig')),'modules':entries}
(r/'docs/section3-final-integrity.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'module_count':len(entries),'sealed_at_utc':out['sealed_at_utc'],'root_fingerprint':entries['Audit.lean']['fingerprint']}))
