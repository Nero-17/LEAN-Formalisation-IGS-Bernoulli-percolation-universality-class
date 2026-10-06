from pathlib import Path
p=Path('scratch/CyclicPhysicalClass.lean');t=p.read_text(encoding='utf-8-sig')
first='(word (initial ++ middle :: suffix) last)';second='(word (suffix ++ last :: initial) middle)'
addition=f'''
variable (initial suffix : List Rule) (middle last : Rule)
variable [Nonempty {first}.network.InteriorVertex] [NeZero {first}.edges]
variable [Nonempty {second}.network.InteriorVertex] [NeZero {second}.edges]

theorem cyclic_block_word_physical_exponent_class
    (hinitial : ∀ rule ∈ initial, rule.TerminalSymmetric) (hmiddle : middle.TerminalSymmetric)
    (hsuffix : ∀ rule ∈ suffix, rule.TerminalSymmetric) (hlast : last.TerminalSymmetric)
    (hforward : {first}.Classical) (hbackward : {second}.Classical)
    (p : ℝ) (hp : 0 < p) (hp' : p < 1)
    (hfixed : {first}.network.reliability p = p) :
    SameCriticalExponentUniversalityClass {first} {second}
      hforward.edges_gt_one hbackward.edges_gt_one p ((word suffix last).network.reliability p) := by
  have hfactor := hfixed
  rw [← (wordAppendEquivalence initial middle suffix last).reliability] at hfactor
  obtain ⟨hpositive, hless, _, _⟩ := cyclic_factor_interior (word initial middle) (word suffix last) p hp hp' hfactor
  apply (hforward.same_critical_exponent_class_iff_dimensions hbackward p ((word suffix last).network.reliability p)
    hp hp' hfixed hpositive hless (cyclic_block_word_fixed_point initial suffix middle last p hfixed)).mpr
  exact cyclic_block_word_three_growth_values initial suffix middle last hinitial hmiddle hsuffix hlast p hp hp' hfixed
'''
t=t.replace('\nend\nend Universality.Rule',addition+'\nend\nend Universality.Rule');p.write_text(t,encoding='utf-8')
