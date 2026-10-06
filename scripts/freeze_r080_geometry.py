from pathlib import Path
import re, json, hashlib
root=Path(__file__).resolve().parents[1]
source=Path('C:/Users/lzysh/Documents/Codex/2026-10-06/new-chat/work/universality-section4')
seen=set(); order=[]
def visit(module):
    if module in seen:return
    seen.add(module)
    path=Path(module.replace('.', '/')+'.lean')
    body=(source/path).read_text(encoding='utf-8-sig')
    for dep in re.findall(r'^import (Universality\.[\w.]+)\s*$',body,re.M): visit(dep)
    order.append((module,path,body))
visit('Universality.Geometry.GenerationHausdorffDimension')
entries=[]; audits=[]; shared=[]
for module,path,body in order:
    if (root/path).exists():
        assert (root/path).read_text(encoding='utf-8-sig')==body, str(path)
        shared.append(module);continue
    frozen=root/'scratch/R080Geometry'/path
    frozen.parent.mkdir(parents=True,exist_ok=True)
    frozen.write_bytes((source/path).read_bytes())
    names=re.findall(r'^#print axioms (\S+)\s*$',body,re.M)
    audits+=names
    entries.append({'module':module,'source':str(frozen.relative_to(root)).replace('\\','/'),'target':str(path).replace('\\','/'),'source_sha256':hashlib.sha256(frozen.read_bytes()).hexdigest(),'audit_names':names})
manifest={'source_repo':str(source),'source_commit':'919e8735cc28374000c6ca9554ebb0a6887e751f','source_git_status':'clean (read-only git status verified 2026-10-06)','base_dependency_count':len(shared),'base_dependencies_identical':shared,'modules':entries,'audits':audits,'planned_transformation':'Remove inline #print axioms lines and append them to central Audit.lean; no mathematical changes. Recompile all new sources locally.'}
(root/'scratch/r080_geometry_integration.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'closure':len(order),'shared_identical':len(shared),'new_modules':len(entries),'audits':len(audits)}))
