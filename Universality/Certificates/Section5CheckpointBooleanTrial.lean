import Universality.Certificates.Section5CheckpointBoolean
import Universality.Certificates.Section5MassChunkDataBase1905

/-! A controlled repeat of the already checked 368-to-384 segment. Only the
decidable comparison is changed; both checkpoint values and all 16 steps
are exactly the production witnesses. -/

namespace Universality.Certificates
open MassChunksBase19

set_option maxHeartbeats 0
set_option maxRecDepth 100000
set_option exponentiation.threshold 10000
set_option Elab.async false

theorem checkpointBooleanTrial :
    runLexMassChunk 2562 16 checkpoint0368 = checkpoint0384 :=
  runLexMassChunk_eq_of_boolean 2562 16 checkpoint0368 checkpoint0384 (by decide +kernel)

#print axioms checkpointBooleanTrial
end Universality.Certificates
