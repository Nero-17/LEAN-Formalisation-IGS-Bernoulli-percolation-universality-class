"""Generate exact crossing histograms to be independently checked in Lean."""
from pathlib import Path
import runpy
root=Path(__file__).resolve().parents[1]
edges=[(2,1),(0,3),(2,3),(0,4),(4,2),(0,5),(5,2),(4,5),(3,6),(6,1),(3,7),(7,1),(6,7)]
for batch in range(64):
    counts=[0]*14
    for index in range(batch*128,(batch+1)*128):
        reached={0}
        while True:
            previous=set(reached)
            for edge,(u,v) in enumerate(edges):
                if (index>>edge)&1 and (u in reached or v in reached): reached.update((u,v))
            if reached==previous: break
        if 1 in reached: counts[index.bit_count()]+=1
    name=f'oppositeRows{batch:02d}'
    text=f'''import Universality.Certificates.Opposite.Batch{batch:02d}
import Universality.Percolation.CertifiedReliability

namespace Universality
open FiniteNetwork

def {name}Crossing : Fin 14 → ℕ := ![{','.join(map(str,counts))}]

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
theorem {name}_crossing : ∀ size : Fin 14,
    ({name}.map fun row => row.crossingBySize oppositeWheatstoneNetwork size.val).sum =
      {name}Crossing size := by
  decide

end Universality
'''
    (root/'Universality'/'Certificates'/'Opposite'/f'Crossing{batch:02d}.lean').write_text(text,encoding='utf-8')
print('Generated 64 histogram witness modules.')
