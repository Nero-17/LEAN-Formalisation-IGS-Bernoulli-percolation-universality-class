"""Propose component certificates. Lean checks every edge and decreasing rank."""
from collections import deque
from pathlib import Path

root = Path(__file__).resolve().parents[1]
networks = {
    'diamond': [(0, 2), (2, 1), (0, 3), (3, 1)],
    'wheatstone': [(0, 2), (2, 1), (0, 3), (3, 1), (2, 3)],
}

def vector(values):
    return '![' + ', '.join(map(str, values)) + ']'

lines = ['import Universality.Percolation.CertifiedClusterCounts',
         'import Universality.Examples.Diamond',
         'import Universality.Percolation.Wheatstone', '',
         'namespace Universality', 'open FiniteNetwork',
         'set_option maxHeartbeats 0', 'set_option maxRecDepth 100000', '']
for name, edges in networks.items():
    lines += [f'def {name}ClusterRows : List (FullComponentRow 4 {len(edges)}) := [']
    for configuration in range(2 ** len(edges)):
        certificates = []
        for vertex in range(4):
            visited = {vertex}
            ranks, parents = [0] * 4, [0] * 4
            queue = deque([vertex])
            while queue:
                current = queue.popleft()
                for edge, (first, second) in enumerate(edges):
                    if not (configuration >> edge & 1):
                        continue
                    if current not in (first, second):
                        continue
                    neighbor = second if current == first else first
                    if neighbor not in visited:
                        visited.add(neighbor)
                        ranks[neighbor] = ranks[current] + 1
                        parents[neighbor] = edge
                        queue.append(neighbor)
            mask = sum(1 << v for v in visited)
            certificates.append(f'⟨{mask}, {vector(ranks)}, {vector(parents)}⟩')
        suffix = ',' if configuration < 2 ** len(edges) - 1 else ']'
        lines.append(f'  ⟨{configuration}, ![' + ', '.join(certificates) + ']⟩' + suffix)
    lines += ['', f'theorem {name}ClusterRows_indices :',
              f'    {name}ClusterRows.map FullComponentRow.index = List.finRange (2 ^ {len(edges)}) := by',
              '  decide +kernel', '', f'theorem {name}ClusterRows_valid :',
              f'    ∀ row ∈ {name}ClusterRows, row.Valid {name}Network := by',
              '  decide +kernel', '']
lines += ['end Universality', '']
(root / 'Universality/Examples/ClusterCountCertificates.lean').write_text('\n'.join(lines), encoding='utf-8')
print('Wrote checked-table proposals for diamond and Wheatstone.')
