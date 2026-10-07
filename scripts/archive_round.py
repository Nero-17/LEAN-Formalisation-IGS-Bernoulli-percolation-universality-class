"""Package the single R071 report and reproducible source, excluding local caches."""
from pathlib import Path
import zipfile
import os

root = Path(__file__).resolve().parents[1]
destination = root.parent / 'universality_class_R071_2026-10-06_完整研究记录.zip'
excluded = {'.git', '.lake', '__pycache__', 'scratch', 'logs'}
with zipfile.ZipFile(destination, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
    for directory, directories, files in os.walk(root):
        directories[:] = sorted(name for name in directories if name not in excluded)
        for name in sorted(files):
            path = Path(directory) / name
            archive.write(path, str(path.relative_to(root)))
print(destination)
print(f'Bytes: {destination.stat().st_size}')
