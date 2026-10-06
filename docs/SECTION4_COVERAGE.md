# Section 4: independent feasibility and dependency map

Inspected on 2026-10-06. Source: the current Overleaf manuscript, Section 4,
"The six exponentials theorem and common scales". Labels are used instead of
theorem numbers because the manuscript is being edited concurrently.

GitHub baseline: `de5c6e9c2d6f025665f20a5ee2c54ba373f28741`.
Independent local branch: `codex/section4-independent`.
Lean 4.32.1; mathlib `520045ab14e26149ee970e2e617ca04b09bde5d6`.

The other Codex chat, "universality class 2", is actively completing Section 3
in a different checkout. Its newer uncommitted and local-only results are not
dependencies of this branch. Its reported R077 checkpoint is newer than the
current GitHub baseline. No file in that checkout is modified here.

## Independence boundary

The logarithmic and algebraic part of Section 4 can be developed without the
local limit theorem, infinite-root construction, or the physical beta, delta
and eta exponents. Graph specialisations can import specific established
Section 2 finite-graph, response and spectral modules, rather than the project
root. Initially, conclusions must concern equality of the three actual growth
dimensions. The final translation to equality of physically defined critical
exponents still uses the Section 3 exponent/dimension equivalence; that bridge
must not be silently assumed or renamed as a definition.

## Current certified probe

`Universality/Arithmetic/ScaleBlocking.lean` imports only
`Mathlib.Analysis.SpecialFunctions.Log.Basic` and proves:

* `Universality.Section4.normalized_log_pow`: positive integral blocking leaves
  the ratio of multiplier and scale logarithms unchanged.
* `Universality.Section4.aligned_log_dimensions_iff`: when positive blocking
  powers of the scales agree, equality of their normalized logarithms is
  equivalent to equality of the corresponding multiplier powers.

Both declarations were accepted by Lean with axiom output exactly
`propext`, `Classical.choice`, `Quot.sound`. There is no `sorry`, `admit`,
`native_decide`, added mathematical axiom, or assumed exponent theorem.
This certifies the logarithmic part of `prop:iterated-response`; it does not
yet formalise the actual iterated graph-response identities.

## Statement-by-statement map

| Manuscript item | Starting point | Remaining obligation |
| --- | --- | --- |
| `thm:six-exponentials` | No proof found in the project or pinned mathlib sources | Major external transcendence theorem. Prove it separately for unconditional closure; an explicitly parameterised implication is only conditional progress. |
| `lem:algebraicity` | Actual reliability/counting polynomials and critical spectral formulas already exist | Prove nonzero fixed-point polynomial, algebraicity of its root, rational response evaluations and eigenvalues; connect to actual graph quantities. |
| `def:commensurate` | Existing `Universality/Arithmetic/Commensurability.lean` | Definition and rational-log equivalence already proved. Avoid duplicating them. |
| `thm:dimension-rank` | Real logarithm algebra, rational linear independence, finite-dimensional span APIs | Derive the rank obstruction from a precise six-exponentials input; prove the primitive common integer base and the rank-two scale restriction. Complete without that input only after six exponentials itself is formalised. |
| `ex:wheatstone-arithmetic` | Exact Wheatstone counts and multipliers, integer prime factorization | Rational independence from the valuations at 13, 5 and 2; connect to the scale theorem. |
| `prop:iterated-response` / `lem:aligned-class` | Actual response composition and generation results; new two-lemma logarithmic probe | Prove all actual graph iterate identities and specialize the new arithmetic theorem coordinatewise. |
| `lem:fixed-point-polynomial-structure` | Actual polynomial endpoint identities, classical graph symmetry | Integer quotient and endpoint values; full degree via cycle-matroid beta invariant or a replacement proof; the parity argument for two-edge cuts; nonconstant reduction at every prime. No ready-made Crapo beta-invariant result was found by the bounded source search. |
| `thm:irreducible-commensurability` | Gauss/minimal-polynomial APIs, positive 2x2 block, strict pivotal bound | The unramified lifting/integer-valuation step, constant-multiplier contradiction, quadratic conjugation and logarithmic independence; then the six-exponentials-dependent conclusion. Ordinary Hensel over Z_p alone does not supply the stated finite unramified extension construction. |
| Transcendence of pivotal dimension | The preceding no-integer-power assertion would prove irrationality | Gelfond--Schneider not found in pinned mathlib; an unconditional transcendence claim needs that theorem formalised as well. |
| `cor:diamond-commensurability` | Exact diamond critical probability, block trace/determinant and formulas | Irreducibility and the nonsquare norm 209 argument over Q(sqrt 5), then the general arithmetic criterion. |

The necessary ingredients above have not all been proved in this branch.
In particular, the existence of a source file called Hensel or Unramified does
not establish the required bridge between their APIs.

## Recommended development order

1. Algebraicity and exact logarithmic blocking, with actual Section 2 responses.
2. Rational linear independence, primitive common bases and explicit examples.
3. Polynomial degree/parity and quadratic conjugation lemmas.
4. The p-adic lifting and fixed-point multiplier argument.
5. Close the external transcendence dependencies and the physical-exponent
   bridge, or report precisely which final results remain conditional.

No completion percentage is assigned: one small kernel-checked probe does not
measure the difficulty of the missing transcendence and local-field proofs.
No claim is made that Section 4 has been formalised in full.
