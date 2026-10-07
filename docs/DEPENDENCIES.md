# Logical dependencies

Lean's standard logical axioms are `propext`, `Classical.choice` and `Quot.sound`.
Exactly two additional mathematical axiom declarations are accepted:

| Input | Lean declaration | Source |
|---|---|---|
| Six exponentials theorem | `Universality.External.six_exponentials` | [SixExponentials.lean](../Universality/Arithmetic/SixExponentials.lean) |
| Gelfond–Schneider theorem | `Universality.External.gelfond_schneider_real` | [GelfondSchneider.lean](../Universality/Arithmetic/GelfondSchneider.lean) |

These are established external theorems, not conjectural mathematical assumptions;
their proofs have not been formalised in this repository. The audit permits them
explicitly and records the actual axiom dependencies of each project declaration.

`FourExponentialsReal` is a proposition supplied as an explicit theorem hypothesis.
It is not an axiom and is not used to assert unconditional four-exponentials results.

`Audit.lean` rejects every other axiom dependency, including `sorryAx`. It selects
declarations by their source module, not only by their namespace, and includes
serialized private/generated kernel declarations. Compiler-only entries are
counted separately and are not counted as mathematical proofs.
