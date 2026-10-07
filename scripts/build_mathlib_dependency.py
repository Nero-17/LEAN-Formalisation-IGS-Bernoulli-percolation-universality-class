"""Compile missing pinned mathlib dependencies without changing their sources."""
from pathlib import Path
import argparse
import os
import re
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('module')
parser.add_argument('--cache', default='C:/Users/lzysh/Documents/Codex/lean32/packages')
parser.add_argument('--lean', default='C:/Users/lzysh/.elan/toolchains/leanprover--lean4---v4.32.1/bin/lean.exe')
args = parser.parse_args()
cache = Path(args.cache)
root = cache / 'mathlib'
env = os.environ.copy()
env['LEAN_PATH'] = os.pathsep.join(str(p / '.lake/build/lib/lean') for p in cache.iterdir() if p.is_dir())
visited = set()

def build(module):
    relative = Path(*module.split('.'))
    output = root / '.lake/build/lib/lean' / relative.with_suffix('.olean')
    if output.exists() or module in visited:
        return
    visited.add(module)
    source = root / relative.with_suffix('.lean')
    if not source.exists():
        raise RuntimeError(f'Missing source: {source}')
    for line in source.read_text(encoding='utf-8-sig').splitlines():
        match = re.match(r'^(?:(?:public|private|meta)\s+)*import\s+(Mathlib[.\w]*)\s*$', line)
        if match:
            build(match.group(1))
    output.parent.mkdir(parents=True, exist_ok=True)
    print(f'Compiling pinned dependency {module}', flush=True)
    # Match the elaboration options in the pinned mathlib lakefile.
    command = [args.lean, '-DautoImplicit=false', '-DmaxSynthPendingDepth=3',
               '-o', str(output), str(relative.with_suffix('.lean'))]
    while True:
        result = subprocess.run(command, cwd=root, env=env, text=True,
                                encoding='utf-8', errors='replace', capture_output=True)
        diagnostic = result.stdout + result.stderr
        if result.returncode == 0:
            print(diagnostic, end='', flush=True)
            break
        # Cached direct imports can still lack a transitive object file.
        missing = re.search(r"of module (Mathlib[.\w]*) does not exist", diagnostic)
        if missing and missing.group(1) not in visited:
            print(f'Repairing missing transitive dependency {missing.group(1)}', flush=True)
            build(missing.group(1))
            continue
        print(diagnostic, end='', flush=True)
        raise subprocess.CalledProcessError(result.returncode, command)

build(args.module)
