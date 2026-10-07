"""Build the complete import closure and execute the project-wide axiom audit.

Run under `lake env python scripts/build.py`, or set LEAN_PATH and pass --lean.
The default compiles every project module. --incremental reuses only objects
bound to unchanged sources, compiler, search path and dependency object hashes.
--check-only verifies an existing local manifest without claiming compilation.
"""
from pathlib import Path
import argparse, hashlib, json, os, re, shutil, subprocess, time

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / '.lake/unified-build.json'

def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()

def imports(path):
    # All project import declarations are single, unqualified import lines.
    # Read only the header: certificate literal files can be tens of MB.
    result = []
    with path.open(encoding='utf-8-sig') as stream:
        for line in stream:
            match = re.fullmatch(r'import\s+(Universality[\w.]*)\s*', line)
            if match:
                result.append(match[1].replace('.', '/') + '.lean')
            elif line.strip() and not line.startswith('import '):
                break
    return result

def closure(target='Audit.lean'):
    seen, active, result = set(), set(), []
    def visit(module):
        if module in active:
            raise ValueError('Import cycle: ' + module)
        if module in seen:
            return
        active.add(module)
        if not (ROOT / module).is_file():
            raise FileNotFoundError(module + ': restore generated certificate data first')
        for dependency in imports(ROOT / module):
            visit(dependency)
        active.remove(module)
        seen.add(module)
        result.append(module)
    visit(target)
    return result

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lean', default=shutil.which('lean'))
    parser.add_argument('--incremental', action='store_true')
    parser.add_argument('--check-only', action='store_true')
    args = parser.parse_args()
    if not args.lean:
        parser.error('Lean not found; use lake env or --lean')
    lean = Path(args.lean).resolve()
    environment = {'compiler_sha256': sha(lean),
                   'lake_manifest_sha256': sha(ROOT / 'lake-manifest.json'),
                   'search_path': os.environ.get('LEAN_PATH', '')}
    previous = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}
    records, built, reused = {}, 0, 0
    logs = ROOT / 'logs'
    logs.mkdir(exist_ok=True)
    project_objects = ROOT / '.lake/build/lib/lean'
    environment_for_lean = dict(os.environ)
    environment_for_lean['LEAN_PATH'] = str(project_objects) + os.pathsep + environment['search_path']
    for module in closure():
        obj = project_objects / Path(module).with_suffix('.olean')
        entry = {'source_sha256': sha(ROOT / module),
                 'dependency_objects': {d: records[d]['olean_sha256'] for d in imports(ROOT / module)}}
        old = previous.get('modules', {}).get(module, {})
        valid = (previous.get('environment') == environment and
                 all(old.get(k) == v for k, v in entry.items()) and
                 obj.exists() and old.get('olean_sha256') == sha(obj))
        if args.check_only:
            if not valid:
                raise RuntimeError('Unverified or changed object: ' + module)
            reused += 1
        elif args.incremental and valid and module != 'Audit.lean':
            reused += 1
        else:
            obj.parent.mkdir(parents=True, exist_ok=True)
            log = logs / (module.replace('/', '_') + '.log')
            print('Checking', module, flush=True)
            with log.open('wb') as output:
                result = subprocess.run([str(lean), '-R', str(ROOT), '-o', str(obj), module],
                                        cwd=ROOT, env=environment_for_lean, stdout=output, stderr=subprocess.STDOUT)
            if result.returncode:
                raise RuntimeError(f'{module} failed; see {log}')
            if 'PROJECT_FINAL_KERNEL_AUDIT_OK' not in log.read_text(encoding='utf-8', errors='replace') and module == 'Audit.lean':
                raise RuntimeError('Final audit marker absent')
            built += 1
        entry['olean_sha256'] = sha(obj)
        records[module] = entry
        if not args.check_only:
            MANIFEST.write_text(json.dumps({'environment': environment, 'modules': records}, indent=2))
    print(json.dumps({'modules': len(records), 'compiled': built, 'reused': reused,
                      'mode': 'integrity_only' if args.check_only else 'build_and_audit'}))

if __name__ == '__main__':
    main()
