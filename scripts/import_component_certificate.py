"""Generate witnesses only; every certificate is checked by the Lean kernel."""
from collections import deque
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "Universality" / "Certificates" / "Opposite"
DEST.mkdir(parents=True, exist_ok=True)
EDGES = [(2,1),(0,3),(2,3),(0,4),(4,2),(0,5),(5,2),(4,5),
         (3,6),(6,1),(3,7),(7,1),(6,7)]

def component(index, root):
    rank, parent = [0]*8, [0]*8
    seen, queue = {root}, deque([root])
    while queue:
        vertex = queue.popleft()
        for edge, (first, second) in enumerate(EDGES):
            if not (index >> edge) & 1:
                continue
            neighbor = second if vertex == first else first if vertex == second else None
            if neighbor is not None and neighbor not in seen:
                seen.add(neighbor)
                rank[neighbor] = rank[vertex]+1
                parent[neighbor] = edge
                queue.append(neighbor)
    return sum(1 << vertex for vertex in seen), rank, parent

def vec(values):
    return "![" + ",".join(map(str,values)) + "]"

def cert(data):
    mask, rank, parent = data
    return "⟨" + str(mask) + ", " + vec(rank) + ", " + vec(parent) + "⟩"

batch_size = 128
manifest = []
for batch in range(8192 // batch_size):
    begin, end = batch*batch_size, (batch+1)*batch_size
    name = f"Batch{batch:02d}"
    definition = f"oppositeRows{batch:02d}"
    rows, totals = [], [[0]*3 for _ in range(3)]
    conditions = [0]*3
    for index in range(begin,end):
        source, target = component(index,0), component(index,1)
        rows.append(f"  ⟨{index}, {cert(source)}, {cert(target)}⟩")
        crossing = bool(source[0] & 2)
        for state in ([0] if crossing else [1,2]):
            conditions[state] += 1
            active = source[0] | (target[0] if state==1 else 0)
            for edge,(first,second) in enumerate(EDGES):
                ends = ((active>>first)&1) + ((active>>second)&1)
                if ends==2:
                    totals[state][0 if (index>>edge)&1 else 1] += 1
                elif ends==1:
                    totals[state][2] += 1
    table = "fun σ τ => match σ, τ with\n" + "\n".join(
        f"    | .{s}, .{t} => {totals[i][j]}"
        for i,s in enumerate(['connected','both','single'])
        for j,t in enumerate(['connected','both','single']))
    text = f'''import Universality.Percolation.CertifiedCounts
import Universality.Percolation.OppositeWheatstone

namespace Universality
open FiniteNetwork

def {definition} : List (ComponentRow 8 13) := [
{',\n'.join(rows)}]

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
set_option cbv.maxSteps 1000000000 in
theorem {definition}_valid :
    {definition}.all (fun row => decide (row.Valid oppositeWheatstoneNetwork)) = true := by
  decide

def {definition}Counts : LiveState → LiveState → ℕ :=
  {table}

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
set_option cbv.maxSteps 1000000000 in
theorem {definition}_counts :
    (∀ σ, ({definition}.map fun row => if row.condition oppositeWheatstoneNetwork σ then 1 else 0).sum =
      (match σ with | .connected => {conditions[0]} | .both => {conditions[1]} | .single => {conditions[2]})) ∧
    (∀ σ τ, ({definition}.map fun row => row.count oppositeWheatstoneNetwork σ τ).sum =
      {definition}Counts σ τ) := by
  decide

end Universality
'''
    (DEST/f"{name}.lean").write_text(text,encoding='utf-8')
    manifest.append(dict(batch=batch,begin=begin,end=end,conditions=conditions,counts=totals))
(ROOT/'docs'/'opposite-certificate-batches.json').write_text(json.dumps(manifest,indent=2))
print(f"Generated {len(manifest)} independent certificate batches.")

