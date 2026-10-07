# Section 5 formalisation

The implementation builds actual finite two-terminal networks, then proves
their responses from exact allocation certificates. It does not replace the
network observables with the desired numerical values.

## Main interfaces

`Universality/Section5.lean` is the checked combined public entry point,
including the actual construction, all four complete numerical seeds,
the specified infinite family and physical results. `Universality.lean`
imports it and has also passed the final assembly check.
`Universality/Section5/Seed19.lean` is the first checked concrete
entry point: its full numerical certificate and actual rule have passed.
`SeedShifted19.lean` is also checked, including its full mass certificate,
actual rule, transcendental dimensions, and rational-span conclusions.
`Seed739.lean` and `PhysicalSeed739.lean` are checked as well. The actual
19 and 739 rules have the same four physical critical exponents and
incommensurate scales, with a ten-boundary audit using standard logical
axioms only; see `section5-seed739-verification.json`.
`Universality/Section5/SeedCertificates.lean` and `CertifiedConsequences.lean`
have passed. Base661 has all 59 initial stream transitions, all 30 signed
repair chunks, and the original complete mass identity checked. All three
original scale logarithms are rationally independent. The family with
scales `(19*661^k)^100` has pairwise incommensurate, unbounded scales,
Hausdorff dimension 58/25, threshold 1/2, and the same four physical
critical exponents.

| Manuscript component | Lean interface |
| --- | --- |
| Heterogeneous Wheatstone construction | `wheatstoneRule`, `WheatstoneExpression.rule` |
| Classical graph structure and exact distance | `Graph/Section5Classical`, `Graph/Section5Distance` |
| Reliability, thermal and three-state mass responses | `WheatstoneResponse`, `WheatstoneThermal`, `WheatstoneMass` |
| Actual lexicographic leaf allocation | `allocationDecoration`, `allocatedExpression` |
| Exact finite identities and actual graph consequences | `ExactAllocationCertificate` |
| Complete integer mass certificate | `CompressedAllocation.mass_certificate` |
| Three independent actual scale logarithms | `exactCertificates_three_rules` |
| Infinite family and actual finite-generation growth limits | `exactCertificates_infinite_growth_family` |
| Scales tend to infinity | `compositionFamily_scales_tendsto_atTop` |
| Actual compact metric completion and Hausdorff dimension | `RuleResponses.hausdorff_dimension`, `ExactAllocationCertificate.hausdorff_dimension` |
| Shifted actual dimensions, transcendence and rational span | `ExactAllocationCertificate.shifted_dimensions*` |
| Conditional four-exponentials obstruction | `Classical.incommensurate_physicalClass_obstructs_fourExponentials`, `common_irrational_dimension_obstructs_four_exponentials` |
| Actual physical critical exponents and threshold | `RuleResponses.hasCriticalExponents`, `RuleResponses.physical_infinite_cluster_positive_iff` |

The four data sets are `(depth, base, offset) = (424,19,0), (936,661,0),
(952,739,0), (424,19,480)`. Their certificate targets give actual distances `base^100 + offset`,
edge counts `base^232`, thermal multipliers `base^70`, and mass eigenvalues
`base^219` on the original positive vector `(55,46,23)`. All four
original numerical certificate obligations are now closed.

The mass checker preserves ordered products. With integer matrices
`K = [[22,18],[5,18]]` and `J = [[9,12],[3,6]]`, its target is

```
(16 (2K+J)^depth + sum_word allocation(word) P_word (2K+J-16I)) (55,23)
  = 16^(depth+1) base^219 (55,23).
```

The initial sum uses a proved no-carry integer packing and a descending
stream. The stream retains the current packed coefficient row and the
remaining lexicographic states, rather than a full quadratic table. Packet
corrections and the baseline have separate exact evaluators. Python emits
literal data; Lean proves the finite checks and their mathematical meaning.

`Section5BitExtraction` proves that a shift-and-mask version of the entire
evaluator equals the original division-and-remainder version. Concrete
checks may use this equality without changing their mathematical endpoint.
The production `Section5MassChunks` module proves composition of independently
checked stream segments; its intermediate states are data to verify, not
assumptions about the answer.

The full Base19 chain has passed: 27 successive segments, the packed initial
vector, binomial counts, all 425 ordered states, the floor contribution, and
the terminal sum. The original initial-mass equality and the separate signed
repair then imply the original integer mass identity. `Section5Seed19Audit`
checks the resulting actual classical rule and its Hausdorff dimension 58/25.
The corresponding full shifted chain has also passed. `Section5ShiftedSeedAudit`
checks the actual Hausdorff dimension's transcendence and the dimensions'
rational span ranks 1, and 2 after adjoining 1.
The Base739 chain has passed all 60 stream transitions and its original
initial-mass endpoint. `Section5MassRepairChunks` combines 30 consecutive
signed-packet chunks; exact flattening, the baseline, the total, and all
chunk equalities are separately checked. The resulting `Section5MassBase739`
proves the original complete mass identity. The corresponding complete
Base661 checks have also passed.

The final four Base661 transitions are stored in four separate proof modules.
Their original eight public declarations are preserved byte for byte; the
original batch module imports the four leaves. A separately checked overlay
binds this layout to the original proof source and historical manifest.
Original checkpoint data, JSON inputs and restoration manifests are unchanged.
The source auditors check this explicit transformation as well as full segment
coverage. All four leaves have their own actual strong Lean kernel
receipts; the original batch aggregate and initial-mass endpoint also pass.

## Verification

The project pins Lean 4.32.1 and mathlib commit
`520045ab14e26149ee970e2e617ca04b09bde5d6`. The existing Windows scripts accept
explicit `-LeanBin` and `-PackageCache` overrides.
The Python receipt/driver tools use the `LEAN_BIN` and `PACKAGE_CACHE`
paths in `scripts/section5_receipt_closure.py`; configure those and the
matching defaults in `scripts/check.ps1` when using another machine.
The Python driver does not accept the PowerShell override flags.

```powershell
python scripts/section5_final_driver.py --decisions docs/section5-final-history-decisions.json
```

This command writes a plan without running Lean. Review any changed source,
object, or dependency evidence and update the context-bound decisions before
adding `--execute`. The selective driver retains genuine successful historical
checks and runs the final declaration audit from source. It does not silently
turn incomplete historical evidence into a fresh compilation receipt.
During assembly, `execution_blockers` prevents execution while a required
repair-chunk module remains absent from the final public import closure.
Wait for the checked repair bridges before executing either build mode.

For a full independent build from a freshly extracted archive, first follow
`RESTORE_GENERATED_DATA.md` to restore the 44 omitted data files into a separate
empty directory, verify their exact hashes, and copy the missing files into the
extracted project. Keep all other archived certificate sources unchanged. Then:

```powershell
python scripts/section5_final_driver.py --fresh --plan docs/fresh-plan.json --result docs/fresh-result.json
```

Add `--execute` when ready to compile the entire import closure. This is an
expensive, single-threaded numerical verification; planning alone proves
nothing. It requires the pinned Lean and mathlib runtime described above.
Neither workflow requires running the certificate generators again. In
particular, the older monolithic mass generator must not overwrite the checked
stream and repair-chunk assembly. The original JSON inputs and all generators
remain archived for provenance and development.

The capacity generator separates literal inputs, row bounds, support
disjointness, packet checks and final assembly, preserving the public
`allocationBase19`, `allocationBase661`, `allocationBase739` and
`allocationShifted19` interfaces. Put recursion-depth options before large
literal definitions; placing them after the definition does not protect its
compiler pass.

Run fixed checks in dependency order with the logging wrapper, for example:

```powershell
python scripts/section5_certificate_check.py --profile --threads 1 Section5InputBase661 Section5RowsBase661 Section5DisjointBase661 Section5PacketCapacityBase661 Section5DataBase661
```

The wrapper records compiler exits, wall-clock durations and source hashes
in `docs/section5-certificate-kernel-checks.json`. New receipts also bind the
complete local import sources and objects before and after checking, the
compiler, search path, package manifest, and output object hashes. Historical
failures and the limited evidence of earlier receipts remain in that log;
missing historical dependency evidence is not synthesized. Generating
a file, a successful Python replay, or a small evaluator benchmark does not
establish its Lean theorem.

New invocations also save a durable run journal and the original output bytes
under `docs/section5-kernel-runs/`. The actual process exit is recorded before
the final dependency snapshot is attempted. A failed or incomplete snapshot
does not become a successful strong receipt, even if the compiler returned zero.

`python scripts/section5_check_status.py` compares these receipts with the
current source hashes and reports which concrete stages still lack a matching
successful check. This status report is separate from the final import-closure
and axiom audits.

`decide +kernel` invokes ordinary Lean kernel validation; it is separate
from the unused native decision path. No `sorry` or `native_decide` is used.
Only transcendence uses the explicitly accepted Gelfond–Schneider external
interface. The rational-span, scale-independence, graph and certificate
proofs use standard Lean logical axioms only. `FourExponentialsReal` is a
proposition supplied as a hypothesis, not an additional axiom.

## Scope and evidence

Actual finite-generation ambient, conditional-mass and pivotal growth limits
are covered. The ambient ratio is also proved to be the Hausdorff dimension
of the actual compact completion of the rescaled generation graph metrics.
The 25 required geometry modules were frozen from the R080 workspace and
independently compiled here; exact source and object evidence is retained in
`section5-geometry-integration-receipt.json`.

Section 3 has proved the actual infinite-root law and the four observable
critical exponents. Its 112 newly required modules have been frozen and
recompiled here. `PhysicalExponents`, `PhysicalSeed19`, and `PhysicalShifted19`
have passed, with 29 audited boundaries using only standard logical axioms.
For Base19 the actual exponents are beta = 13/70, nu = 10/7, delta = 219/13,
and eta = -3/50. The eta statement concerns fixed macroscopic distance
windows. Base19 and shifted19 both have actual infinite-cluster threshold 1/2;
Base739 has also passed its separate physical threshold audit. The final
assembly proves the same actual exponents and threshold for Base661 and
the specified infinite family. It does not identify the shifted rule
with the original rules' four rational physical exponents.
`ClassFourExponentials` proves the discussion's general class result,
deriving algebraic responses from classical finite rules internally. The
module and its independent three-boundary audit have passed. Its
four-exponentials conjecture is an explicit hypothesis; the irrationality to
transcendence consequence uses only the accepted Gelfond–Schneider interface.

The round archive preserves all proofs, original JSON inputs, and an exact
restoration recipe for 44 large generated data modules. The full restoration
was executed and all 453,477,561 bytes matched the checked sources by SHA256.
See the archive's `RESTORE_GENERATED_DATA.md` and `GENERATED_DATA.json` before
building from an extracted archive. The local workspace already contains
these data files. Restoration reconstructs source; it does not replace Lean
checking.

The current record is `docs/R079_完整研究记录.md`. Independent review boundaries
and compiler evidence are in `section5-review.md`,
`section5-independent-kernel-review.md`, and
`section5-certificate-evaluation-review.md`. Core and symbolic dependency
closure snapshots are retained in the corresponding `section5-*-build-*.json`
files. The completed concrete build is recorded in
`section5-final-execution-plan.json`, `section5-final-execution-result.json`,
and its `.axioms.log` / `.axioms.json` companions; these are separate from
the earlier symbolic milestones.

The final incremental driver completed 906 modules. It retains genuine historical evidence and runs the missing modules from source; this is not a claim that every module was freshly rebuilt.
The actual top-level kernel dependency output covers 905 project-origin modules and 8543 serialized declarations, including private and generated declarations. All dependencies pass the standard-axiom / accepted-transcendence-interface policy. Final source, object and environment snapshots agree.
