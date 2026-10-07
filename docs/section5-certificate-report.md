# Section 5 allocation certificate formalisation

This is the certificate agent's work record within project round R079, which
started on 6 October 2026 at 21:59:09 Asia/Shanghai.  The parent agent maintains
the single authoritative Drive report; this file documents implementation and
verification details for the certificate modules.

The current kernel-checked certificate endpoints are:

| Allocation | Depth | Base | Distance offset | Capacity, distance, volume, thermal | Repaired mass |
| --- | ---: | ---: | ---: | --- | --- |
| `allocationBase19` | 424 | 19 | 0 | Complete | Complete |
| `allocationBase661` | 936 | 661 | 0 | Complete | Checking |
| `allocationBase739` | 952 | 739 | 0 | Complete | Complete |
| `allocationShifted19` | 424 | 19 | 480 | Complete | Complete |

“Complete” here means a successful Lean kernel check of the actual natural
allocation and its full ordered signed repair, where applicable. Generated
data or successful Python calculations alone do not establish an endpoint.

The public integration API is uniform across the four allocation names in
the table. The suffixes `_capacityValid` and `_capacity` certify the compressed
check and its pointwise natural-allocation bound; `_length`, `_volume_nat`
and `_thermal_nat` give the three exact scalar identities; `_mass` gives
the integer matrix eigenvector identity. The complete propositions match
the fields of `Section5.ExactAllocationCertificate` in
`Universality/Section5/CertificateRealisation.lean`. The current status table
applies to these theorem endpoints; a source declaration awaiting compilation
is not counted as proved.

## Input provenance

All allocation values come from the eight original JSON files under
`supplementary/section5/certificates/{n424,n936,n952,transcendental}`.  The
source directory's README identifies the Overleaf source commit
`1b194c68cc1b1cefc73c0126c192c0e59a464b5b`.  Exact SHA-256 values are embedded
in each generated `Section5Input*.lean` file and recorded in
`docs/section5-certificate-inputs.json`.  Generators import the original
integer floors, remainders and signed correction coefficients; they do not
generate or optimise allocations.

## Kernel-checked generic results

The following modules have each completed `scripts/check.ps1` with exit 0:

- `Section5Packets`: exact uniqueness of packet layer, paired prefix and
  tail; signed scalar cancellation; coefficient/slack capacity implication;
  noncommutative ordered matrix repair with the factor `18^layer`.
- `Section5Allocation`: the exact original initial allocation, including
  lexicographic rank at a fixed zero count; a kernel-efficient binomial
  recurrence; generic floor/remainder slack bounds and exceptional packet
  capacity obligations.
- `Section5CorrectedAllocation`: a deterministic parser of packet supports;
  the actual final natural-valued allocation; total capacity from disjoint
  supports and the complete packet checks.  The conversion from signed
  integers to naturals is proved using nonnegativity.
- `Section5CapacityCertificate`: a decidable certificate format and the
  per-word capacity theorem for every word of the required length.
- `Section5Sums`: reindexing packet corrections against every binary word,
  full-allocation preservation of all zero-count scalar moments, and exact
  ordered matrix mass repair of the full allocation.
- `Section5BinomialTable`: linear-length checks of literal binomial tables,
  proved equal to `Nat.choose` at every index, including out-of-range zeroes.
- `Section5Distance`: packets do not alter the all-zero word; the exact
  distance contribution is the final initial-allocation row.
- `Section5MomentCertificate`: actual-allocation volume and thermal formulas
  follow from verified group counts and the earlier integer moment data.

The separate reviewer supplied the checked `Section5InitialSums` module:
fixed-zero word counts, exact lex ranks, prefix counts, the scalar grouped
sum, and the noncommutative initial mass sum with its compressed lex-prefix
recurrence.

No module uses `sorry`, new mathematical axioms, `native_decide`, or a native
execution oracle.  Large literal checks use Lean's `decide +kernel`: the
Lean 4.32.1 implementation directly asks the kernel to check the ordinary
`of_decide_eq_true` proof and caches a checked auxiliary lemma.  This is the
kernel option, not the distinct native option.

## Concrete checks and current limitations

The full base-19 capacity certificate using the original slack formula
completed with exit 0.  Auxiliary slacks were subsequently strengthened by
allowing a possible remainder increment in both first-letter classes.  This
changes no floor, remainder, packet coefficient, or actual allocation.
An earlier regenerated base-19 module also completed with exit 0 at about
00:17 on 7 October 2026 Asia/Shanghai.  Its concrete endpoints are
`allocationBase19_capacityValid` and `allocationBase19_capacity`.

A direct quadratic pairwise signature check caused an out-of-memory failure
when multiple large checks were running.  `Section5LinearChecks` replaces
that decision with an ordinary kernel check that packet indices are exactly
`List.range`, and derives pairwise distinctness from `List.nodup_range`.
This generic module completed with exit 0; after the replacement the complete
base-19 check took approximately one minute.  Subsequent large checks are
run with one Lean worker per queue and measured limits on concurrent queues.
This was a verification resource failure, not a
false certificate or weakened mathematical condition.

Further checked optimizations preserve the same mathematical obligations:
`Section5RowChecks` traverses rows and slack values together;
`Section5PacketChecks` traverses the packet list with a Boolean short-circuit
slack test; `Section5FastRank` carries suffix counts while computing exact
lexicographic rank; and `Section5GroupChecks` traverses floor rows, binomial
counts and moment totals together.  Each Boolean checker has a proved
soundness theorem yielding the original proposition.  The current base-19
row/slack and disjoint-support check passed again at about 00:51 on
7 October.  The generated packet proofs were then switched to the faster
exceptional checker. Both the complete current base-19 and base-661
capacity modules have subsequently passed, with source-hash receipts.

Profiling the larger literal declaration exposed a distinct build failure:
the recursion-depth setting had originally appeared after the data
definition, and Lean's compiler reached its default depth on the 937-row
input.  Settings now precede the literal declaration.  The corrected
base-661 input module passed in 29.657 seconds.  Generated capacity files
are split into `Input`, `Rows`, `Disjoint`, `PacketCapacity`, and final
`Data` modules, retaining the same public constants and theorem names.
This preserves checked intermediate results and makes the remaining cost
measurable.  The numeric build wrapper uses one Lean worker and records
source hashes, timestamps, exit codes and optional profiles in
`docs/section5-certificate-kernel-checks.json`.

The complete current base-661 capacity proof passed on 7 October at 01:13:39
Asia/Shanghai.  The profiled component runtimes were 15.969 seconds for rows,
14.079 seconds for disjoint support, 48.203 seconds for all packets and
20.297 seconds for the final assembly.  The packet stage used the proved
closed zero-count formula and exact fast lexicographic rank; its kernel
checking time was approximately 30.1 seconds.  The resulting endpoint is
`allocationBase661_capacityValid`, and `allocationBase661_capacity` applies
to every length-936 binary word.  This closes leaf feasibility for that
actual allocation, not merely for its compressed scalar totals.

The independent `section5_certificate_sourcecheck.py` audit parsed the emitted
Lean literals and compared all floors, remainders, layer indices, tail bits,
tail lengths and coefficients against the JSON.  All four matched exactly;
the output is `docs/section5-certificate-sourcecheck.json`.  The stronger
slacks retain exactly 4, 12, 20 and 4 exceptional words, respectively.

`Section5Moments*.lean` use literal binomial tables and exact group-total
checks. All four current allocations have passed their complete capacity,
distance, volume and thermal checks, including integer and natural-number
forms for the actual allocations. The last scalar aggregate,
`Section5MomentsShifted19`, passed at 02:59:07 Asia/Shanghai on 7 October.
The shifted distance includes its exact offset 480. The remaining concrete
obligation is the full base-661 mass identity.

Concrete specialization originally made Lean attempt expensive reduction
inside the enormous binary-word sums. Checked symbolic specialization
lemmas now rewrite the allocation, depth and base before inserting literals.
This preserves the exact statements and lets the resulting volume/thermal
endpoint proofs check in milliseconds. Counts, grouped totals, distance
and response endpoints are separate modules, with unchanged public names.

The full numerical mass identities for base-19, base-739 and shifted-19 have
now been kernel-checked; only base-661's full mass identity remains open. The efficient evaluator and
its complete semantic connection are proved:
`Section5MatrixEvaluation` proves no-carry extraction of grouped vectors and
binomial counts from packed natural numbers, and exact inverse recurrence
for descending from depth `n` to depth `n-1`.  Its determinant is
`306*B^2 + 180*B + 18`.  `Section5MatrixStream` defines the descending
lexicographic evaluator; `Section5MatrixStreamCorrect.initialMassEvaluation_correct`
identifies its result with the actual ordered initial-allocation matrix sum.
`Section5MassCertificate.CompressedAllocation.mass_certificate` combines
that result with all signed packet repairs and the baseline numerator to
prove the actual allocation eigenvector equation.

The depth-952 initial sum has approximately 450,000 vector recurrence states
and 448,294 complete lex cylinders.  A literal table of all large intermediate
vectors would be hundreds of MB.  The packed root at depth 952 was genuinely
kernel-checked in a separate benchmark in 32.46 seconds, with only `propext`
in its axiom report.  This benchmark does not check the full lexicographic
sum.  The independent Python replay of the new full stream matched the
depth-424 source initial mass in 18.407 seconds.  The original supplemental
Python verifier succeeds for all four inputs; these runs are computational
evidence and are not claimed as Lean proofs.

The generated `Section5InitialMass*.lean` files require the complete stream
to equal the original `mass_vector_numerator` literal.  The separate
`Section5Mass*.lean` files then check baseline plus initial sum plus packet
repair against the final target and instantiate the generic actual-mass
theorem.  These concrete numerical files have been generated, but no success
is claimed for an input until its actual kernel checks finish. The base-19
final packet check passed at 02:31:58 on 7 October in 58.297 seconds, with
30.8 seconds of kernel checking. Thus `allocationBase19_mass` proves the
actual corrected allocation's eigenvector identity, using only standard
Lean foundations. Together with its previously checked capacity, distance,
volume and thermal endpoints, all base-19 certificate premises are closed.
Its receipt binds the local dependency source/object closure, compiler,
search path and output hashes before and after the check. Earlier receipts
retain their original weaker scope and require separate closure auditing.

The first standalone base-661 packet-repair calculation was cancelled for
resources after approximately 626 seconds, without a numerical result.
The parent task measured its Lean process at approximately 4.135 GB resident
memory while total host usage reached 90%. The exact owned queue was stopped,
and fresh parent process inspection confirmed both its Lean and PowerShell
processes had exited. The queued base-739 repair had not started. This is
recorded in `section5-certificate-repair-resource-cancellation.json` as a
resource cancellation, not a false arithmetic identity.

The replacement keeps the same evaluator and final target, but divides each
original packet list into 30 consecutive blocks of at most 32 packets. Each
block requires an independent kernel check of its proposed signed pair. A separate check
requires the blocks' exact ordered flattening to equal the complete actual
packet list; the baseline and total arithmetic are checked separately. The
kernel-checked `Section5MassRepairChunks` theorem combines these obligations
back into the original `massEvaluationWithInitial` equality. The two new
manifests are `section5-certificate-repair-chunks-Base661.json` and
`section5-certificate-repair-chunks-Base739.json`. Both sets of all 30 block
checks, ordered flattening, baseline, total and final repair assembly have
now passed. The base-661 repair assembly completed in 14.406 seconds and
depends only on `propext`. Modules were started one at a time with fresh
host-memory checks, avoiding the cancelled monolithic computation's retained
arithmetic state. Both bounded final bridge sources were emitted only after
every relevant successful receipt matched current sources, dependency
snapshots and output objects. The final actual-mass assembly still separately
requires the complete initial-stream theorem; that obligation is complete
for base-739 and remains in progress for base-661.

The independent source audit also compares both binomial tables against
`math.comb` and all initial mass target literals against the JSON values.
After both bounded bridge sources stabilized, the strengthened audit passed
all four inputs at 05:31:43 Asia/Shanghai. It exactly matches the complete
depth/base/target types and the final capacity, original initial-sum and
signed-repair premises, and binds each bounded repair-data source hash.
Earlier source-audit reports are preserved as original UTF-8 text with their
SHA-256 values in `section5-certificate-sourcecheck-history.json`. This
source-correspondence check does not replace the separate repair source
audit or successful Lean receipts.

Two full depth-424 mass evaluations, first using division/modulo extraction
and then its proved equivalent bit extraction, were stopped without a
result after approximately 7–8 and 6–7 minutes. The host was under measured
memory pressure. These aborted evaluations do not disprove any certificate.
The bit evaluator's equivalence and the complete checkpoint-composition
theorem are kernel-checked for all inputs.

The first exact two-depth checkpoint pilot passed in 363.953 seconds on
7 October at about 02:01:47 Asia/Shanghai. It includes the actual initial
packed vector, binomial packing, all 425 initial states, and both exact
transitions. Python only generates proposed witnesses. The Lean kernel
checks every equality; the transition and value invariant depend only on
`propext`. Profiling isolated 333 seconds of numeral elaboration and only
7.16 seconds of kernel checking. A second pilot using balanced 4096-bit
literal limbs passed in 33.578 seconds, with elaboration reduced to 5.91
seconds and kernel checking unchanged at 7.02 seconds. The original pilot
is preserved. Neither pilot alone proves the full mass formula: all later
transitions, floor contribution, and terminal sum still require checks.

A sixteen-depth pilot also passed in 71.938 seconds, with 5.47 seconds for
the transition itself. Its raw megabit literal tokens still required 42.7
seconds of elaboration. Production witnesses therefore use balanced
4096-bit limbs containing Lean's ordinary `nat_lit` syntax. They are
unchanged natural numbers, with no additional trusted evaluator. Four
separate sixteen-depth transition proofs are checked per module, with
asynchronous elaboration disabled. Shared data modules contain no transition
assumptions, and proof modules do not import earlier proof modules.

The complete depth-424 witness chain has 28 checkpoints, including every
one of the 425 states at each checkpoint, and 27 adjacent transition checks.
The root vector, binomial packing, actual initial state list and complete
floor contribution have already passed in a separate module. The witness
generator independently recomputes the floor plus accumulated contributions
plus the exact terminal sum against the source mass vector. This generator
assertion is an implementation check; only the Lean equalities establish
the theorem. The final assembly composes value invariants with `Eq.trans`
and supplies all hypotheses of `initialMassEvaluation_of_chunk_values`.
At 02:27:37 Asia/Shanghai on 7 October, all 27 transitions and the final
original-evaluator theorem `allocationBase19_initialMassEvaluation` passed
with exit 0. Its only axioms are the standard Lean foundations `propext`,
`Classical.choice`, and `Quot.sound`. The separate terminal numerical check
uses no axioms. This closes the complete initial ordered sum for base-19;
the final packet-repair eigenvector identity is checked separately.
All four complete witness chains have now been generated and independently
reviewed against their original input data. The shifted-19 mass queue began
at 03:01:14 after a read-only host memory check measured 56%, below the parent
task's 75% gate. All 27 transitions and the original initial evaluator passed,
followed by the final repaired mass identity at 03:21:33. The final module took
60.110 seconds, including 28.5 seconds of kernel checking. Its endpoint
`allocationShifted19_mass` depends only on `propext`, `Classical.choice` and
`Quot.sound`; its strong receipt binds unchanged sources and dependencies.
Thus both depth-424 allocations now satisfy every certificate premise,
including the shifted allocation's distance offset 480. Base-661 checking
is in progress. The complete base-739 mass queue began at 03:25:55, after
the shifted seed's integration checks released their slot and a read-only
host memory measurement was 73%, within the 75% gate for three concurrent
single-worker queues. At 04:31:44, all 60 base-739 transitions and the
original `allocationBase739_initialMassEvaluation` theorem had passed. The
latter took 18.688 seconds and uses only the standard logical axioms. The
queue then reached its obsolete monolithic final-repair module; that exact
queue was cancelled at 04:31:54 before any final mass result, preserving the
completed initial chain. At that checkpoint its final mass theorem still
awaited the bounded packet-repair checks and their exact assembly; the
subsequent successful check is recorded below. Generated witnesses alone
are not proofs.

At 04:39 Asia/Shanghai, the base-739 final repaired mass theorem
`allocationBase739_mass` also passed, in 17.156 seconds. All 30 signed packet
chunks, the exact original packet-list concatenation, baseline and total
checks had already passed, followed by the repair assembly in 17.297 seconds.
Before emitting the final bridge, the generator required every repair module's
successful receipt to match its current source, dependency snapshot and
output objects. The final actual-allocation theorem uses only `propext`,
`Classical.choice` and `Quot.sound`; the repair bridge itself uses only
`propext`. Thus base-19, base-739 and shifted-19 now have every certificate
endpoint. Base-661 remains in progress. Its 44th of 59 transitions passed
in proof batch 10, taking 1452.156 seconds for that batch. The old sequential
queue was then stopped during the next short data module; no completed proof
was discarded. After all remaining data modules passed independently, the
remaining proof batches were partitioned into disjoint queues 11/12 and
13/14, starting at 04:48:57 and 04:49:09 with measured host-memory loads of
65% and 72%. No proof source, literal, import or obligation was changed.
The old process tree was independently confirmed absent before restarting;
`section5-certificate-queue-boundaries.json` records the exact boundaries.

The independent base-661 proof batches 11 and 13 subsequently passed in
1760.844 and 2151.093 seconds. This brings its completed initial-mass
transitions to 52 of 59. The last two independent batches, 12 and 14, started
at 05:30:39 and 05:30:51 Asia/Shanghai on 7 October, with measured host-memory
loads of 68% and 75%. They retain the same source and exact equality
obligations. The final initial-mass and mass assembly will wait until these
seven transitions and the coordinated final generic-dependency rechecks
have actually completed.

Batch 14 passed at 05:43:16 in 744.906 seconds, with unchanged source and
dependency snapshots. Its three transition lemmas use only `propext`.
This brought the total to 55 of 59 completed transitions. The released slot
was handed to the coordinated short-helper rechecks. The remaining batch 12
was interrupted as described below; no additional transition is counted.

The old batch-12 wrapper exited with a traceback while obtaining its
`snapshot_after`: its PowerShell package-enumeration subprocess returned
3221226091. The complete actual traceback is preserved in
`section5-proof66112-interruption.log`. It contains no reliable Lean exit
code. At 22:21 UTC the parent independently confirmed that the module had no
`.olean` object, and no successful receipt exists. This is an incomplete
run, not evidence that the mathematical equality is false or true.

Recovery retains the four original sixteen-step equalities but puts each in
its own module, `Section5MassChunkProofBase66112A` through `12D`. The old
`Section5MassChunkProofBase66112` becomes a four-import aggregate, preserving
all eight original public theorem names and the unchanged final initial-mass
assembly. The full original 1737-byte source is saved under
`docs/section5-proof-split-original`; its SHA-256 remains
`9294ea6a8d1581d96f85723e0cad2b4a23383b1a94014263a4fbe5ec4d43829a`,
as independently anchored by the previously archived manifest and restoration
receipt. `section5-proof66112-split-overlay.json` records the exact source
slices, leaf hashes and aggregate imports. The strict overlay checker requires
byte-identical declaration bodies, options, namespace and footer, one-to-one
coverage of all eight names, and unchanged original manifests, all 44 data
files and both reconstruction scripts. It permits this single declared
packaging exception without changing the original manifest. All four new
numerical leaves still require actual kernel checks.

The numeric wrapper now saves the actual pre-run snapshot and run identity,
streams byte-exact compiler output to a flushed log, and durably saves the
real process return code before attempting the post-run snapshot. Failure of
the latter leaves an explicitly incomplete journal and cannot become a strong
successful receipt. Historical receipts are retained unchanged. This change
addresses evidence loss; it does not alter any Lean proposition or arithmetic.

Large witness batches after the first are independent data modules, and
each proof batch imports the two adjacent data batches it actually uses.
This limits imported state data during checking. The already checked
base-19 chain remains unchanged. For the active base-661 queue, only batches
02 onward were changed, because batches 00/01 had already started. An
independent byte comparison verified all 26 changes affect import headers
only, preserving every declaration, numeral, proof and ordering. All final
assembly modules still import every required proof batch.

A controlled Boolean-comparison repeat of the already verified 368-to-384
segment also passed, but did not improve runtime: 83.1 seconds of kernel
checking, compared with 66.6 seconds for its earlier direct equality check.
The conjectured comparison overhead is therefore not established by this
experiment, and production retains the direct equality checker. The Boolean
equivalence itself preserves every checkpoint field and the entire ordered
state list; it introduces no weaker certificate condition.

A final bounded comparison checked the two-depth segment 368-to-370 in
31.063 seconds, including 5.61 seconds of kernel checking. This suggested
some per-depth benefit from shorter chunks, but would require roughly eight
times as many checkpoint witnesses. Production retained the already reviewed
sixteen-depth layout; no further syntax or chunk-size experiments were used.

## Exact recovery of large generated data

The complete source ZIP encountered an actual 100 MiB upload limit. The
archive therefore retains all original JSON inputs, all proof sources,
generators, manifests and checking receipts, while the 44 pure generated
`Section5MassChunkData*.lean` copies can be restored exactly. Every local
source file remains present and unchanged. This storage arrangement changes
neither a Lean theorem nor the required kernel checks.

`scripts/restore_section5_chunk_data.py` reconstructs only those data modules
in a separate empty output directory. It preserves the original base-19
import chain, base-661's already checked batches 00/01 and independent
batches 02 onward, and the independent batches in the other two chains.
It uses explicit UTF-8/CRLF encoding on every platform and requires each
file's byte length and SHA-256 to equal the archived manifest before writing,
then checks the saved file again. Existing files are never overwritten.

A complete real restoration ran from 03:14:39 to 03:21:04 Asia/Shanghai on
7 October, taking 385.281 seconds. All 44 files, totalling 453,477,561 bytes,
matched their manifests. A separate read of the live Lean sources confirmed
all 44 restored hashes also match the current source files. The unchanged
receipt is `docs/section5-chunk-data-restoration.json`, SHA-256
`f2c24365447987ff8a71d2cf674e94283cf492306f26894d07f610c22f2d9101`.
It records both script hashes, all four manifest and input hashes, and every
restored file hash. This is a byte-restoration test, not another Lean build.

From the archive's extracted `code` directory, using Python 3.11 or newer:

```powershell
python scripts/restore_section5_chunk_data.py --output-dir ../restored-data
```

After the tool reports success, copy its `Universality/Certificates` data
files into the corresponding directory of the newly extracted source tree.
The destination for restoration itself must remain a separate empty
directory; do not overwrite the existing verified working tree.

## Reproduction

Use the saved Lean sources with the pinned Lean 4.32.1 toolchain and mathlib
revision. If using the recipe archive, first restore its 44 data files by the
byte-checked procedure above. The production initial-mass manifests
`section5-certificate-chunks-*.json` specify the original data/proof layout.
For the interrupted base-661 batch, also apply the separately verified
`section5-proof66112-split-overlay.json`: compile its four leaf modules before
the original-named four-import aggregate. The manifests themselves remain
unchanged so the restoration hashes retain their historical meaning.
The two `section5-certificate-repair-chunks-*.json`
manifests likewise specify the larger seeds' bounded repair checks.

The allocation and scalar generators are retained as construction provenance:

```powershell
python scripts/section5_certificate_data.py
python scripts/section5_certificate_moments.py
python scripts/section5_certificate_sourcecheck.py
```

Full regeneration should occur in a separate source copy, followed by a
comparison with the recorded manifests. Earlier generators include historical
monolithic mass-check layouts; running them over the current source tree is
not the production reproduction procedure. The exact restoration command
above was tested against every production data file, including its historical
import layout and line endings.

Compile local dependencies in import order, then check the saved endpoint
modules with `scripts/section5_certificate_check.py --profile <module>`.
This driver uses `scripts/check.ps1`, one Lean worker, and records current
source/dependency snapshots and output-object hashes. The parent task's
`section5_final_driver.py` and `section5-final-execution-plan.json` manage the
final dependency-closure audit. Each theorem reported as complete requires a
successful actual compile; generated witnesses and source-correspondence
checks alone establish no certificate.
