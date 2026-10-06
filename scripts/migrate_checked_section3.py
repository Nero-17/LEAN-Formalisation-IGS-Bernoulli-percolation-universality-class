"""Migrate explicitly checked candidates; default is a read-only validation."""
from pathlib import Path
import json
import re
import sys
root=Path(__file__).resolve().parents[1]
spec_path = sys.argv[sys.argv.index('--spec') + 1] if '--spec' in sys.argv else 'scripts/section3_checked_migration.json'
spec=json.loads((root/spec_path).read_text())
modules=spec['modules']
replacements={'scratch.'+k.replace('/','.'): 'Universality.'+v.replace('/','.') for k,v in (spec['prior_imports'] | modules).items()}
prepared=[]
for source,target in modules.items():
    path=root/'scratch'/(source+'.lean')
    text=path.read_text(encoding='utf-8-sig')
    text=re.sub(r'^import (scratch[.][A-Za-z0-9_.]+)$',lambda m:'import '+replacements.get(m[1],m[1]),text,flags=re.M)
    assert 'import scratch.' not in text, source
    prepared.append((root/'Universality'/(target+'.lean'),text))
if '--apply' in sys.argv:
    for path,text in prepared:
        assert not path.exists(), str(path)
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(text,encoding='utf-8')
    for filename,lines in [('Universality.lean',['import Universality.'+v.replace('/','.') for v in modules.values()]),('Audit.lean',['#print axioms '+v for v in spec['audits']])]:
        path=root/filename
        text=path.read_text(encoding='utf-8-sig')
        path.write_text(text.rstrip()+'\n'+'\n'.join(line for line in lines if line not in text.splitlines())+'\n',encoding='utf-8')
    print('Applied',len(prepared),'checked candidates; full formal rebuild remains required.')
else:
    print('Validated migration plan:',len(prepared),'modules,',len(spec['audits']),'audit entries. Formal files unchanged.')
