from pathlib import Path
import re,json,sys
r=Path(__file__).resolve().parents[1]
entries=json.loads((r/sys.argv[1]).read_text(encoding='utf-8'))
if len(sys.argv)>2:entries=entries[int(sys.argv[2]):int(sys.argv[3])]
mapping={e['source'][:-5].replace('/','.'):e['target'][:-5].replace('/','.') for e in entries}
byname={}
for p in (r/'Universality').rglob('*.lean'):byname.setdefault(p.stem,[]).append(str(p.relative_to(r))[:-5].replace('\\','.').replace('/','.'))
def rewrite(m):
    dep=m.group(1)
    if dep in mapping:return 'import '+mapping[dep]
    found=byname.get(dep.split('.')[-1],[]);assert len(found)==1,(dep,found)
    return 'import '+found[0]
for e in entries:
    body=(r/e['source']).read_text(encoding='utf-8-sig')
    body=re.sub(r'^import (scratch\.[\w.]+)\s*$',rewrite,body,flags=re.M)
    assert not re.search(r'\b(?:sorry|admit|axiom|native_decide|sorryAx)\b',body)
    p=r/e['target'];assert not p.exists(),str(p)
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(body,encoding='utf-8')
for filename,prefix,items in [('Universality.lean','import ',list(mapping.values())),('Audit.lean','#print axioms ',[a for e in entries for a in e['audits']])]:
    p=r/filename;s=p.read_text(encoding='utf-8-sig');existing=set(s.splitlines())
    p.write_text(s.rstrip()+'\n'+''.join(prefix+x+'\n' for x in items if prefix+x not in existing),encoding='utf-8')
print({'migrated_modules':len(entries),'audits':sum(len(e['audits']) for e in entries)})
