"""Assemble Lean proofs from independently checked component batches."""
from pathlib import Path
root=Path(__file__).resolve().parents[1]
names=[f'oppositeRows{i:02d}' for i in range(64)]
imports='\n'.join(f'import Universality.Certificates.Opposite.Batch{i:02d}' for i in range(64))
counts=[[30336,14912,6848],[20064,15520,13120],[10032,3472,15136]]
states=['connected','both','single']
table='\n'.join(f'  | .{s}, .{t} => {counts[i][j]}' for i,s in enumerate(states) for j,t in enumerate(states))
valid=',\n    '.join(n+'_valid' for n in names)
condition=',\n    '.join(n+'_counts.1' for n in names)
conditional=',\n    '.join(n+'_counts.2' for n in names)
tables=', '.join(n+'Counts' for n in names)
text=f'''{imports}

namespace Universality
open FiniteNetwork

def oppositeComponentRows : List (ComponentRow 8 13) :=
  {' ++\n  '.join(names)}

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
theorem oppositeComponentRows_indices :
    oppositeComponentRows.map ComponentRow.index = List.finRange (2 ^ 13) := by
  decide

theorem oppositeComponentRows_valid :
    ∀ row ∈ oppositeComponentRows, row.Valid oppositeWheatstoneNetwork := by
  have h : oppositeComponentRows.all (fun row => decide (row.Valid oppositeWheatstoneNetwork)) = true := by
    simp only [oppositeComponentRows, List.all_append,
    {valid}]
    rfl
  simpa only [List.all_eq_true, decide_eq_true_eq] using h

def oppositeWheatstoneCountTable : LiveState → LiveState → ℕ
{table}

set_option maxHeartbeats 2000000 in
theorem oppositeWheatstone_exact_counts :
    (∀ σ, oppositeWheatstoneNetwork.conditioningCount σ = 4096) ∧
    (∀ σ τ, oppositeWheatstoneNetwork.conditionalCount σ τ = oppositeWheatstoneCountTable σ τ) := by
  constructor
  · intro σ
    rw [← certified_conditioningCount oppositeWheatstoneNetwork oppositeComponentRows
      oppositeComponentRows_indices oppositeComponentRows_valid]
    simp only [oppositeComponentRows, List.map_append, List.sum_append,
    {condition}]
    cases σ <;> rfl
  · intro σ τ
    rw [← certified_conditionalCount oppositeWheatstoneNetwork oppositeComponentRows
      oppositeComponentRows_indices oppositeComponentRows_valid]
    simp only [oppositeComponentRows, List.map_append, List.sum_append,
    {conditional}]
    cases σ <;> cases τ <;> rfl

theorem oppositeWheatstone_fair_mass (σ τ : LiveState) :
    oppositeWheatstoneNetwork.fairMassMatrix σ τ = (oppositeWheatstoneCountTable σ τ : ℚ) / 4096 := by
  simp [fairMassMatrix, oppositeWheatstone_exact_counts.1, oppositeWheatstone_exact_counts.2]

theorem oppositeWheatstone_fair_block :
    fairMassBlock oppositeWheatstoneNetwork = oppositeWheatstoneBlock := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [fairMassBlock, oppositeWheatstone_fair_mass, oppositeWheatstoneCountTable,
      oppositeWheatstoneBlock]

end Universality
'''
(root/'Universality'/'Percolation'/'OppositeWheatstoneCounts.lean').write_text(text,encoding='utf-8')
print('Generated aggregate counts proof; compilation remains required.')
