"""Propose exact component witnesses; Lean independently checks every row."""
from collections import deque
from pathlib import Path

root = Path(__file__).resolve().parents[1]
destination = root / 'scratch' / 'CentralCertificates'
destination.mkdir(parents=True, exist_ok=True)
edges = [(0, 2), (2, 1), (0, 3), (3, 1), (2, 4), (4, 3), (2, 5), (5, 3), (4, 5)]


def vector(values):
    return '![' + ', '.join(map(str, values)) + ']'


def component(configuration, source):
    reached = {source}
    ranks, parents = [0] * 6, [0] * 6
    queue = deque([source])
    while queue:
        vertex = queue.popleft()
        for edge, (first, second) in enumerate(edges):
            if not configuration >> edge & 1:
                continue
            neighbor = second if vertex == first else first if vertex == second else None
            if neighbor is not None and neighbor not in reached:
                reached.add(neighbor)
                ranks[neighbor] = ranks[vertex] + 1
                parents[neighbor] = edge
                queue.append(neighbor)
    mask = sum(1 << vertex for vertex in reached)
    return reached, f'⟨{mask}, {vector(ranks)}, {vector(parents)}⟩'


batch_names = []
crossing_totals = [0] * 10
internal_totals = [0] * 10
for batch in range(8):
    name = f'centralWheatstoneRows{batch:02d}'
    batch_names.append(name)
    rows, crossing, internal = [], [0] * 10, [0] * 10
    for configuration in range(batch * 64, (batch + 1) * 64):
        components = [component(configuration, vertex) for vertex in range(6)]
        rows.append(f'  ⟨{configuration}, ![' + ', '.join(certificate for _, certificate in components) + ']⟩')
        size = configuration.bit_count()
        crossing[size] += int(1 in components[0][0])
        internal[size] += sum(0 not in reached and 1 not in reached and vertex == min(reached)
                              for vertex, (reached, _) in enumerate(components))
    crossing_totals = [x + y for x, y in zip(crossing_totals, crossing)]
    internal_totals = [x + y for x, y in zip(internal_totals, internal)]
    text = f'''import scratch.CentralWheatstone
import scratch.FullComponentCrossing

namespace Universality
open FiniteNetwork
set_option maxHeartbeats 0
set_option maxRecDepth 100000

def {name} : List (FullComponentRow 6 9) := [
{','.join(chr(10) + row for row in rows).lstrip() }]

theorem {name}_valid :
    {name}.all (fun row => decide (row.Valid centralWheatstoneNetwork)) = true := by
  decide +kernel

theorem {name}_crossing (size : Fin 10) :
    ({name}.map fun row => (row.toComponentRow centralWheatstoneNetwork).crossingBySize
      centralWheatstoneNetwork size).sum = {vector(crossing)} size := by
  have h : ∀ size : Fin 10, ({name}.map fun row =>
      (row.toComponentRow centralWheatstoneNetwork).crossingBySize centralWheatstoneNetwork size).sum =
      {vector(crossing)} size := by decide +kernel
  exact h size

theorem {name}_internal (size : Fin 10) :
    ({name}.map fun row => if openCount row.configuration = size.val then
      row.internalCount centralWheatstoneNetwork else 0).sum = {vector(internal)} size := by
  have h : ∀ size : Fin 10, ({name}.map fun row => if openCount row.configuration = size.val then
      row.internalCount centralWheatstoneNetwork else 0).sum = {vector(internal)} size := by decide +kernel
  exact h size

end Universality
'''
    (destination / f'Batch{batch:02d}.lean').write_text(text, encoding='utf-8')

imports = '\n'.join(f'import scratch.CentralCertificates.Batch{batch:02d}' for batch in range(8))
append_expression = ' ++\n  '.join(batch_names)
valid_proofs = ', '.join(name + '_valid' for name in batch_names)
crossing_proofs = ', '.join(name + '_crossing' for name in batch_names)
internal_proofs = ', '.join(name + '_internal' for name in batch_names)
aggregate = f'''{imports}

namespace Universality
open FiniteNetwork
set_option maxHeartbeats 0
set_option maxRecDepth 100000

def centralWheatstoneClusterRows : List (FullComponentRow 6 9) :=
  {append_expression}

theorem centralWheatstoneClusterRows_indices :
    centralWheatstoneClusterRows.map FullComponentRow.index = List.finRange (2 ^ 9) := by
  decide +kernel

theorem centralWheatstoneClusterRows_valid :
    ∀ row ∈ centralWheatstoneClusterRows, row.Valid centralWheatstoneNetwork := by
  have h : centralWheatstoneClusterRows.all (fun row => decide (row.Valid centralWheatstoneNetwork)) = true := by
    simp only [centralWheatstoneClusterRows, List.all_append, {valid_proofs}]
    rfl
  simpa only [List.all_eq_true, decide_eq_true_eq] using h

theorem centralWheatstone_crossing_counts (size : Fin 10) :
    centralWheatstoneNetwork.crossingCountBySize size = {vector(crossing_totals)} size := by
  rw [← certified_full_crossingCountBySize centralWheatstoneNetwork centralWheatstoneClusterRows
    centralWheatstoneClusterRows_indices centralWheatstoneClusterRows_valid]
  simp only [centralWheatstoneClusterRows, List.map_append, List.sum_append, {crossing_proofs}]
  fin_cases size <;> rfl

theorem centralWheatstone_internal_cluster_counts (size : Fin 10) :
    centralWheatstoneNetwork.internalClusterCountByOpenSize size = {vector(internal_totals)} size := by
  rw [← certified_internalClusterCountByOpenSize centralWheatstoneNetwork centralWheatstoneClusterRows
    centralWheatstoneClusterRows_indices centralWheatstoneClusterRows_valid]
  simp only [centralWheatstoneClusterRows, List.map_append, List.sum_append, {internal_proofs}]
  fin_cases size <;> rfl

end Universality
'''
(root / 'scratch' / 'CentralWheatstoneCounts.lean').write_text(aggregate, encoding='utf-8')
print({'crossing_by_open_size': crossing_totals, 'internal_clusters_by_open_size': internal_totals,
       'status': 'generated witnesses; kernel verification still required'})
