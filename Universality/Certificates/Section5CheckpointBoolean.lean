import Universality.Certificates.Section5MassChunks

namespace Universality.Certificates

def kernelPrefixBoolean (first second : KernelPrefix) : Bool :=
  first.upperLeft == second.upperLeft && first.upperRight == second.upperRight &&
    first.lowerLeft == second.lowerLeft && first.lowerRight == second.lowerRight

theorem kernelPrefixBoolean_iff (first second : KernelPrefix) :
    kernelPrefixBoolean first second = true ↔ first = second := by
  cases first
  cases second
  simp [kernelPrefixBoolean, and_assoc]

def lexMassStateBoolean (first second : LexMassState) : Bool :=
  first.remainingZeros == second.remainingZeros && first.remainder == second.remainder &&
    kernelPrefixBoolean first.accumulated second.accumulated

theorem lexMassStateBoolean_iff (first second : LexMassState) :
    lexMassStateBoolean first second = true ↔ first = second := by
  cases first
  cases second
  simp [lexMassStateBoolean, kernelPrefixBoolean_iff, and_assoc]

def lexMassStatesBoolean : List LexMassState → List LexMassState → Bool
  | [], [] => true
  | first :: rest, second :: remaining =>
      lexMassStateBoolean first second && lexMassStatesBoolean rest remaining
  | _, _ => false

theorem lexMassStatesBoolean_iff (first second : List LexMassState) :
    lexMassStatesBoolean first second = true ↔ first = second := by
  induction first generalizing second with
  | nil => cases second <;> simp [lexMassStatesBoolean]
  | cons first rest ih =>
      cases second <;> simp [lexMassStatesBoolean, lexMassStateBoolean_iff, ih]

def lexMassCheckpointBoolean (first second : LexMassCheckpoint) : Bool :=
  first.depth == second.depth && first.packed.1 == second.packed.1 &&
    first.packed.2 == second.packed.2 && first.packedCounts == second.packedCounts &&
    lexMassStatesBoolean first.states second.states &&
    first.mass.1 == second.mass.1 && first.mass.2 == second.mass.2

theorem lexMassCheckpointBoolean_iff (first second : LexMassCheckpoint) :
    lexMassCheckpointBoolean first second = true ↔ first = second := by
  rcases first with ⟨depth, ⟨upper, lower⟩, counts, states, ⟨firstMass, secondMass⟩⟩
  rcases second with ⟨otherDepth, ⟨otherUpper, otherLower⟩, otherCounts, otherStates,
    ⟨otherFirstMass, otherSecondMass⟩⟩
  simp [lexMassCheckpointBoolean, lexMassStatesBoolean_iff, and_assoc]

theorem runLexMassChunk_eq_of_boolean (bits steps : ℕ)
    (first last : LexMassCheckpoint)
    (checked : lexMassCheckpointBoolean (runLexMassChunk bits steps first) last = true) :
    runLexMassChunk bits steps first = last :=
  (lexMassCheckpointBoolean_iff _ _).mp checked

#print axioms runLexMassChunk_eq_of_boolean

end Universality.Certificates
