from pathlib import Path
import json,re
r=Path(__file__).resolve().parents[1]
entries=json.loads((r/'scratch/infinite_root_pending_integration.json').read_text(encoding='utf-8'))[:4]
entries+=json.loads((r/'scratch/UniformRootGraph/LOCAL_LIMIT_RADIUS_MIGRATION.json').read_text(encoding='utf-8'))
mass=r/'scratch/physical_cluster_number_integration.json'
if mass.exists(): entries+=json.loads(mass.read_text(encoding='utf-8'))
geometry=json.loads((r/'scratch/r080_geometry_integration.json').read_text(encoding='utf-8'))
entries+=geometry['modules']
for e in entries:
    e['target']=e.get('target',e.get('destination'))
    e['audits']=e.get('audits',e.get('audit_names',[]))
mapping={e['source'][:-5].replace('/','.'):e['target'][:-5].replace('/','.') for e in entries}
# Scratch dependencies already migrated in prior verified snapshots are located
# by unique module basename, never by silently adding unverified sources.
byname={}
for p in (r/'Universality').rglob('*.lean'):byname.setdefault(p.stem,[]).append(str(p.relative_to(r))[:-5].replace('\\','.').replace('/','.'))
def rewrite(m):
    dep=m.group(1)
    if dep in mapping:return 'import '+mapping[dep]
    candidates=byname.get(dep.split('.')[-1],[])
    assert len(candidates)==1,(dep,candidates)
    return 'import '+candidates[0]
audits=[];modules=[]
for e in entries:
    body=(r/e['source']).read_text(encoding='utf-8-sig')
    body=re.sub(r'^import (scratch\.[\w.]+)\s*$',rewrite,body,flags=re.M)
    body=re.sub(r'^#print axioms \S+\s*\n?','',body,flags=re.M)
    body=body.replace('graph metrics admit a compatible complete','graph metrics have a compatible complete')
    assert not re.search(r'\b(?:sorry|admit|axiom|native_decide|sorryAx)\b',body),e['target']
    p=r/e['target']
    if p.exists(): assert p.read_text(encoding='utf-8-sig')==body,str(p)
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(body,encoding='utf-8')
    modules.append(e['target'][:-5].replace('/','.'));audits+=e['audits']
for filename,prefix,values in [('Universality.lean','import ',modules),('Audit.lean','#print axioms ',audits)]:
    p=r/filename;body=p.read_text(encoding='utf-8-sig');existing=set(body.splitlines())
    p.write_text(body.rstrip()+'\n'+''.join(prefix+v+'\n' for v in values if prefix+v not in existing),encoding='utf-8')
(r/'scripts/section3_ninth_migration.json').write_text(json.dumps({'entries':entries,'modules':modules,'audits':audits},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'new_modules':len(modules),'new_audits':len(audits),'mass_included':mass.exists()}))
