"""Read-only comparison of the frozen target with the current local manuscript."""
from pathlib import Path
import difflib
import hashlib
import json
import subprocess

root = Path(__file__).resolve().parents[1]
manuscript = root.parent / 'overleaf-universality'
frozen = (root / 'docs/section3-20261006.tex').read_text(encoding='utf-8-sig')
current = (manuscript / 'main.tex').read_text(encoding='utf-8-sig')
git_prefix = ['git', '-c', 'safe.directory=' + manuscript.as_posix(), '-C', str(manuscript)]
head = subprocess.check_output(git_prefix + ['rev-parse', 'HEAD'], text=True).strip()
baseline = subprocess.check_output(git_prefix + ['show',
    'fccfba64fd345f8b0cbaafd94abec48420c0c6fa:main.tex'], text=True, encoding='utf-8')
def section(text):
    begin = text.index(frozen.splitlines()[0])
    end = text.find('\\section{', begin + 1)
    return text[begin:end].strip()
diff = ''.join(difflib.unified_diff(frozen.strip().splitlines(True),
    section(current).splitlines(True), fromfile='frozen-section3', tofile='current-section3'))
result = {'current_manuscript_commit': head,
    'frozen_sha256': hashlib.sha256((root / 'docs/section3-20261006.tex').read_bytes()).hexdigest(),
    'frozen_equals_recorded_baseline_section3': frozen.strip() == section(baseline),
    'frozen_equals_current_section3': frozen.strip() == section(current),
    'conditional_mass_part_unchanged': frozen[frozen.index('\\begin{lemma}\\label{lem:conditional-mass-moments}'):frozen.index('\\begin{lemma}\\label{lem:conditional-mass-local-limit}')] in current,
    'diff': diff}
(root / 'docs/section3-source-comparison.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({key: value for key, value in result.items() if key != 'diff'}, indent=2))
