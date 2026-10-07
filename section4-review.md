# Section 4 independent review

Research mode: Standard Research. Reviewer: Agent 3. Full Section 4 objective recorded at 2026-10-06 13:12:38 UTC (21:12:38 Asia/Shanghai). The authoritative round-state subsequently preserved the earlier uninterrupted-work clock of 13:08:30 UTC; R078 uses that earlier clock, without resetting at this subtask. Critical-review effort target: max; the persistent session's effective runtime setting is unverified. This is a supporting local review note, not a separate research round or external archive.

## Fixed scope and acceptance rule

Source: the full section `The six exponentials theorem and common scales`, from `sec:scale` through `cor:diamond-commensurability`, in the supplied manuscript. The opening universal commensurability assertion is a conjecture, subsequently refuted in Section 5 for rational classes; it must not become a theorem. Section 4's actual theorems and examples, including the unnumbered pivotal-transcendence conclusion, are the formalisation targets.

Only the six-exponentials theorem and, after the user's explicit supplemental authorization, Gelfond--Schneider may enter as external mathematical theorem interfaces. Their exact signatures and use must be auditable. Lean's ordinary foundational axioms are a different category. No extra axiom for graph polynomial degree, Hensel lifting, positive Perron conjugation, residue sums, finite graph algebraicity or a concrete example is authorized.

Acceptance requires: a Lean proposition with the manuscript's actual hypotheses and conclusion; a checked proof; the bridge from the actual graph definitions where relevant; and an audit showing no `sorryAx` or unauthorized theorem assumption. A generic conditional lemma is legitimate progress but not proof of the paper statement whose missing premise it assumes. File counts, declaration counts and compilation of unrelated modules are not evidence of mathematical closure.

Pre-result milestone weights: actual graph algebraicity 10; rank and common primitive base 30; graph iteration and aligned comparison 10; polynomial structure 20; irreducible criterion 20; exact examples and transcendence 10. Scores will follow actual checked coverage, using completion levels 0, 1/4, 1/2, 3/4 and 1. A blocking premise prevents downstream application credit, although its independently proved generic algebra can be listed separately.

## Exact audit checklist

### S4-ALG: Actual graph algebraicity

- The reliability polynomial must come from the finite Bernoulli crossing experiment. Its rational/integer coefficient bridge is proved, not stipulated.
- Show the polynomial `phi-X` is nonzero using the graph endpoint hypotheses; merely saying the critical point is a root does not establish algebraicity for the zero polynomial.
- Connect the real derivative of graph reliability to polynomial derivative evaluation.
- Derive conditional mass entries as rational functions of the critical point with all denominators nonzero. Distinguish the full three-state matrix from its invariant two-state block.
- Derive every complex eigenvalue's algebraicity via the nonzero monic characteristic polynomial; separately identify the Perron root used by the dimensions.

### S4-RANK: Rank and common scale

- Exact equivalence between positive integral power alignment and rational ratio of real logarithms for integer scales greater than one.
- Use six exponentials on genuinely rationally independent finite families. The exponentials equal the integer scale and actual algebraic growth values.
- Rank at least three in the span of `{1,D_H,D_M,D_P}` gives pairwise commensurability throughout the full class, not only a family chosen in advance.
- Nonempty pairwise commensurate integer scales share one integer primitive base, with positive integer exponents. The primitive base is not a proper integral power; no finite-family restriction is allowed unless the paper is explicitly weakened.
- If a shared dimension is irrational, the rational span of *all* scale logarithms has dimension at most two. Finite triple independence must be connected to this possibly infinite-family rank statement.
- The class is nonempty because it contains the initial representative; do not infer an arbitrary family has a member.

### S4-W: Wheatstone example

- Identify the actual graph W, prove its scale 2, edge count 5, critical point 1/2 and derivative 13/8 from existing graph calculations.
- Prove rational linear independence of `1`, `log 5/log 2`, `log (13/8)/log 2`, with denominator positivity and rational-to-integer coefficient clearing.
- Prime valuations at 13, 5 and 2 cover negative integer exponents as well as positive powers.
- Deduce that every scale in its class is a positive power of 2; this is stronger than merely producing an unspecified primitive common base.

### S4-ITER: Iteration

- Actual graph generation remains classical and has distance and edge count powers.
- Reliability is the iterate; its sole interior fixed point is unchanged. A fixed-point implication in one direction is not enough.
- At the common fixed point, derivative and mass matrix are powers. Matrix multiplication requires the applicable terminal-symmetry hypotheses.
- Spectral radius of the matrix power is the power of the positive Perron root; generic scalar log cancellation does not prove this matrix fact.
- Three actual dimensions are unchanged.
- Aligned-scale equivalence holds in both directions for all three positive growth factors; no equality of full matrices or graph substitutions is claimed.

### S4-POLY: Complete fixed-point quotient

- Define the complete integer polynomial `(phi-X)/(X(1-X))` by an exact divisibility identity, not an arbitrary minimal polynomial.
- Prove endpoint values -1 and 1 after cancellation, hence primitivity.
- Prove its exact degree `m-2` for every classical graph. This requires nonvanishing of the top reliability coefficient, not just a degree upper bound.
- Canonicality must imply connectedness of the cycle matroid after adding a terminal edge, and the Crapo-beta positivity argument must either be formalised or replaced by a proved route.
- Prove nonconstant reduction modulo every prime. Endpoint values alone exclude odd primes but do not exclude characteristic two.
- For the characteristic-two step, identify the coefficient of `p^2` with length-two terminal paths and the corresponding closed-edge coefficient with minimal cuts of size two; check simplicity and distance/cut hypotheses.
- Show a two-edge minimum terminal cut leaves exactly two connected components, including the absence of other components.
- Use terminal involution to prove those two counts cannot both be odd, then conclude the positive-degree coefficients have gcd one.

### S4-IRR: Irreducible commensurability criterion

- Irreducibility is of the *complete quotient* over Q. Prove primitive integral divisibility into `phi'^n-N` from a relation at the actual critical point.
- For every prime dividing N, obtain a root of the nonconstant reduced quotient over a finite residue extension.
- Prove this root is simple using the differentiated fixed-point identity, including nonzero derivative, root not 0 or 1 and the characteristic-independent minus-one identity.
- Supply the unramified lift and integer-valued normalized valuation, or a proved replacement. These cannot be new external axioms.
- Infer `n | v_q(N)` at every prime divisor and hence N is an nth power; positivity then forces the actual derivative to be an integer.
- Prove all quotient roots have that common integer multiplier and are simple; account for exactly `m-2` quotient roots and endpoints.
- Prove the fixed-point residue sum identity or an algebraic replacement, leading to derivative `m/2`.
- Connect the existing graph pivotal bound `derivative^2 < m` and `m>=4` to the contradiction.
- Derive multiplicative independence of edge count and derivative, including arbitrary integer signs.
- Use the actual positive mass block and nonsplitting over Q(p_c) to construct its nontrivial relative conjugation; the other root is nonzero and strictly smaller in absolute value.
- Clear rational coefficients, apply the conjugation, and prove the three dimension values independent. A conjugation supplied as a premise without a graph-field construction is conditional progress only.
- Apply the accepted six-exponentials rank theorem to the entire graph class.

### S4-TRANS and S4-DHL: Consequences and exact example

- Under quotient irreducibility alone, exclude every positive integral power of the derivative in Z, deduce pivotal dimension irrational, then apply the authorized Gelfond--Schneider interface to exclude algebraic irrationality.
- For the actual DHL graph, identify the quotient `X^2+X-1` and prove its rational irreducibility.
- Prove its actual critical field is Q(sqrt 5), not simply assume that field equality.
- Connect the existing mass calculation to `7-2 sqrt 5 + sqrt(73-32 sqrt 5)`.
- Prove the norm of `73-32 sqrt 5` is 209, show 209 is not a rational square, and conclude nonsplitting of the mass quadratic over the critical field.
- Apply the general criterion to obtain every scale commensurate with 2, with all graph/field hypotheses discharged.

## Initial independent findings

1. **ACCEPT, generic scalar arithmetic only:** existing `ScaleBlocking.normalized_log_pow` and `aligned_log_dimensions_iff` have the right scalar content. They do not by themselves establish graph iteration, critical point uniqueness or spectral-radius powers.
2. **Symmetry concern RESOLVED:** the weaker existing `Rule.TerminalSymmetric` asks only for a swapping automorphism, but `Rule.Classical.symmetric` in `Graph/ClassicalRule.lean` already explicitly includes `Function.Involutive`. This exactly matches manuscript Definition `def:standing`. The structure lemma should use `rule.Classical`; no strengthening of the paper class is needed.
3. **ACCEPT, optional mathematical generalisation:** even with a swapping finite automorphism rather than an involution, simultaneous odd counts of middle vertices and two-cuts are impossible. Each odd invariant set has an odd-length orbit; odd powers fix one object of each kind; an odd common power then fixes both while swapping terminal components. This observation is not itself a checked Lean result and is unnecessary if the existing classical involution is used.
4. **External theorem scope updated:** initial GS concern is resolved by the user's explicit supplemental authorization. Accepted external mathematical theorem list is exactly six exponentials plus Gelfond--Schneider, with precise signatures still to be reviewed.

No milestone completion is asserted from this initial checklist. Full adoption dispositions and progress scores will be appended after examining actual resulting declarations and their axiom reports.

## Accepted replacement argument and reviewed interfaces

**S4-IRR-COEFF — ACCEPT as a replacement proof, with generic hypotheses still explicit.** The residue-theorem step has an elementary alternative. If the complete quotient divides `phi'-L`, write `phi'-L=Q*T`. Exact polynomial degrees make T linear. Since `Q(0)=-1`, `Q(1)=1` and both endpoint derivatives vanish, `T(0)=L` and `T(1)=-L`; thus `T=L(1-2X)`. Comparing leading coefficients gives `m=2L`. Construction implemented this in `constant_multiplier_twice_eq_degree`; source review verifies that nonzero quotient, linear degree, endpoint values and leading-coefficient cancellation are all derived. This removes the need to formalise complex residues or enumerate roots for that step. It does not discharge the graph's exact degree or the preceding integer-power-to-integer multiplier argument.

**S4-EXT6 — ACCEPT.** `External.six_exponentials` states the standard complex 2-by-3 theorem with rational linear independence in both families and a genuinely transcendental exponential output. The real corollary maps rational independence injectively into C and transfers algebraicity back correctly. An independent compiler run of `SixExponentialsReal.lean` reported exactly `propext`, `Classical.choice`, `Quot.sound`, and `Universality.External.six_exponentials`.

**S4-EXTGS — ACCEPT.** `External.gelfond_schneider_real` has positive algebraic base different from one and algebraic irrational exponent, with the real power expressed as `exp(exponent*log base)`. The logarithmic-dimension corollary cancels a proved nonzero base logarithm and uses positive multiplier. An independent compiler run reported exactly the ordinary three foundational axioms and `Universality.External.gelfond_schneider_real`. The user's authorization resolves the initial concern about adding this theorem.

**S4-RANK-FIN — ACCEPT as generic finite arithmetic.** `DimensionRank.lean` correctly selects three independent entries from a finite generating family of adequate finrank, proves independence of positive-scale logs from noncommensurability, and invokes the accepted six-exponentials theorem. Its finite `Fin size` span causes no infinite-dimensional finrank ambiguity. The actual graph-class specialization and the arbitrary-family scale-rank conclusion are distinct obligations.

**S4-BASE — ACCEPT, independently recompiled after repair.** `CommonPrimitiveBase.lean` chooses the least base representing one scale, derives primitivity by minimality, then uses `Nat.exists_eq_pow_of_pow_eq_pow` to express every commensurate scale as its positive power. Its family is arbitrary and explicitly nonempty. My first compiler replay reached two pre-repair `omega` failures involving natural division; these were repaired by explicit positivity/nonzero arguments. The subsequent independent replay passed and reported exactly the three standard foundational axioms.

## Reviewer-authored concrete advance, pending lead's independent review

`Universality/Arithmetic/WheatstoneArithmetic.lean` now contains a checked signed prime-valuation certificate for 2,5,13, integer logarithmic independence, and rational linear independence of `1, log(5)/log(2), log(13/8)/log(2)` via scalar localization from Z to Q. The core compiler audit reports only the three ordinary foundational axioms. It invokes no external transcendence theorem. The lead will independently review this reviewer-authored code; I do not count self-review as independent adoption.

A temporary attempt to import the actual distance bridge exposed absent old `GraphDistances` object files and was separated from the pure arithmetic core. The completed arithmetic file now also uses the already checked actual Wheatstone reliability derivative. Its scale conclusion retains an explicit algebraic-exponential premise until integrated with the real rule definitions. The final compiler audit of this scale conclusion contains only the three standard foundational axioms and the accepted six-exponentials axiom. Do not describe an unbuilt graph wrapper as proved.

## Second review ledger

**S4-SCALE-RANK — ACCEPT, source review and producer compiler audit.** `ScaleLogRank.scale_log_rank_le_two` bounds cardinal `Module.rank`, not only `finrank`. It selects a basis from the generating set of actual scale logarithms, extracts three independent generators if rank exceeds two, and invokes six exponentials with the independent pair `1,dimension`. This covers arbitrary indexed families, including potentially infinite ones. The strongest remaining scope objection is the need to instantiate it on actual equal-dimension graph representatives; the generic theorem itself correctly rules out infinite-dimensional spans.

**S4-NOPOWER — ACCEPT as a conditional arithmetic result.** `NoIntegerPower` proves irrationality of the logarithmic ratio from absence of all positive integer powers in Z, and transcendence using only the authorized Gelfond--Schneider theorem. Positivity makes the rational numerator positive and denominator clearing produces an actual integer power, including the sign checks. It also proves independence of the two logarithms. The integer-power exclusion is an explicit premise and cannot be credited to this file.

**S4-GRAPH — ACCEPT on source review; graph build pending.** `GraphAlgebraicity` derives nonzero reliability-minus-X from the actual zero endpoint derivative, proves fixed-point and derivative algebraicity, closes actual conditional matrix entries under the critical field, and uses a monic characteristic polynomial for every complex eigenvalue. The actual spectral radius is identified via the already proved positive invariant-block eigenvector, rather than assumed algebraic. `GraphCriticalDimensions` then connects the three displayed logarithmic formulas to the existing finite-graph growth theorem. This source review does not certify uncompiled declarations or add an infinite-volume theorem.

**S4-GRAPH-ITER — ACCEPT on source review; graph build pending.** `GraphIteration` correctly treats `generation n` as `n+1` substitutions, packages positive iteration counts via `steps-1`, establishes both directions of equality of the interior fixed points, and proves actual matrix and spectral-radius powers. Its aligned comparison is an iff for all three scalar responses. It makes no claim that equal growth factors imply equality of full matrices or of graphs.

**S4-GRAPH-RANK — ACCEPT as pairwise actual-graph specialization; broader wrappers pending.** The rank values include `1` and all three actual dimensions. Algebraicity of the six exponentials is discharged from graph definitions. The initial file establishes the pairwise commensurability theorem and its contrapositive rank bound. An explicit arbitrary-class common primitive base and actual graph scale-log cardinal-rank wrapper remain separate obligations; these were sent to the evidence agent for completion.

**S4-INTEGER-RECURRENCE — ACCEPT as a replacement polynomial argument, source review.** In `IntegerMultiplierObstruction`, the differential identity gives `(n+1-index)c[n+1]=(n-2index)c[n]`. Since `c[0]=-1`, coefficients remain nonzero strictly below a positive integer index. At `n=index-1`, the left factor vanishes while the right factor is `-index-1`, a contradiction. With `index=multiplier-1`, this bypasses the manuscript's graph degree and square-bound route for excluding integer multipliers. Its predecessor identity still has to be derived from irreducibility and the complete fixed-point quotient; no p-adic integer-power argument is thereby supplied.

## Subsequent closure and local arithmetic review

**S4-GRAPH build update — ACCEPT.** The evidence agent supplied successful sequential compiler and axiom logs for `GraphAlgebraicHelpers`, `GraphAlgebraicity`, `GraphCriticalDimensions` and `GraphIteration`, with source/object hashes in its evidence record. The updated general fixed-point response theorem also covers admissible nonsymmetric networks because its hypotheses require only terminal distance greater than one and an actual fixed point. This is a producer build combined with independent source review, not a claimed independent build replay.

**S4-GRAPH-FAMILY — ACCEPT, source review.** `common_primitive_base_of_criticalDimension_rank` now works for arbitrary indexed actual-graph families and has an explicit reference representative, supplying nonemptiness. `scale_log_rank_le_two_of_irrational_criticalDimension` specializes the cardinal rank theorem to any one common irrational actual dimension. No finite-family or preexisting finite-dimensional assumption is inserted. This closes the earlier source-scope objection, subject to the recorded final compiler check.

**S4-GRAPH-W — ACCEPT, source review.** `GraphWheatstoneArithmetic` identifies the actual graph's ambient and pivotal dimensions and applies the arithmetic scale certificate. Its whole-class conclusion even needs only equality of these two dimensions; all other-representative algebraicity premises are discharged by graph theorems. The distance and derivative are actual proved graph quantities.

**S4-MASS-CONJUGATION — ACCEPT.** `IrreducibleConjugation` derives the nonsplit quadratic as the minimal polynomial. A power relation at the positive root makes this polynomial divide the power-minus-constant polynomial, so the secondary root satisfies the same relation. The strict bound on its absolute value contradicts equality of positive powers; negative integer powers reduce by field inverses. `IrreducibleMass` obtains the trace, determinant, quadratic roots and strict absolute bound from the actual classical graph mass block. This avoids postulating an automorphism of the real field. Producer compilation is successful; the source argument has been independently reviewed.

**S4-HENSEL — ACCEPT.** `IrreducibleHensel` gives the nonmonic simple-root lift by the existing mathlib adic Newton proof, whose monicity premise was unused. The source is attributed, and the producer reports successful compilation. No Hensel theorem is introduced as an axiom.

**S4-WITT — ACCEPT as a conditional polynomial theorem.** `IrreducibleValuations` supplies a root in the algebraic closure of the residue field, lifts it into its Witt vectors, and compares exponents of the uniformizer p. Witt vectors over this perfect residue field provide a complete discrete valuation ring; a finite residue extension is unnecessary for the argument. Every-prime valuation divisibility then reconstructs an exact natural-number power. The producer reports successful compilation. Integer polynomial divisibility and nonconstant reduction at every prime remain explicit premises here; they must be discharged elsewhere.

## Second reviewer-authored advance, awaiting lead adoption

`DiamondArithmetic.lean` compiles with an exact field-closure proof that every member of Q(sqrt 5) has rational coordinates. It proves that `73-32 sqrt 5` has no square root in that field by deriving a rational square equal to 209 and contradicting the exact nonsquare certificate. It proves the equality of Q((sqrt 5-1)/2) and Q(sqrt 5), hence exclusion of the displayed mass expression from the actual critical-field expression. A paired-coordinate power induction independently proves that no positive power of `6-2 sqrt 5` is an integer, because its positive conjugate is strictly larger. All these declarations use only the three standard foundational axioms. The resulting pivotal-dimension transcendence theorem uses only the authorized GS axiom in addition. The actual graph spectral-radius expression and final whole-class scale theorem require separate integration; self-authored code awaits the lead's independent audit.

## Final integration review (same R078 round; integration build still running)

The lead independently read and recompiled `DiamondArithmetic`, accepting the exact arithmetic and its actual graph wrappers. Existing `DiamondClassical` already contained the actual spectral-radius expression; I compiled that prerequisite and used it to connect the field exclusion to the real three-state matrix. This resolves the earlier unintegrated-expression limitation.

**S4-LOG-TRIPLE — lead ACCEPT of reviewer-authored source; producer compile passed.** `LogarithmicIndependence` converts an arbitrary signed integer relation into a product equal to one. The mass power belongs to the coefficient field because the integer base and pivotal multiplier do; nonsplitting forces its exponent to zero. Restriction to integer scalars of the already proved two-log independence kills the other exponents. Localization then gives rational linear independence of the three normalized logarithms. It uses no transcendence axiom. `GraphLogarithmicIndependence` discharges positivity, critical-field membership and edge-count conditions for actual classical graphs. Its scale conclusion uses six exponentials alone.

**S4-DIAMOND-INTEGRATION — producer compile passed; final lead audit pending.** `GraphDiamondArithmetic` proves the actual complete quotient equals `X^2+X-1`, not just that the critical point is a root of that quadratic. It proves rational irreducibility by showing that a rational root would make 5 a rational square. It also proves independence of all three actual finite-growth dimensions and the scale `2^k` conclusion for every actual classical rule with the same dimension tuple. The explicit diamond certificates discharge all no-power and nonsplitting conditions. The independence and quotient irreducibility have only foundational axioms; the scale conclusion adds only six exponentials. A harmless tactic-style warning was subsequently removed without changing the statement or proof argument; the lead's full source-closure rebuild is the final replay of that edit.

**S4-PARITY — ACCEPT, complete source review plus successful producer build.** The actual graph theorem assumes no coefficient or parity premise. Simplicity turns the terminal-exchanging vertex involution into an edge involution. An invariant two-open crossing contains a length-two path with a unique middle vertex, hence a fixed vertex. Every two-closed failure is an inclusion-minimal terminal cut because reopening either edge leaves a single-edge deletion. The proof derives that every vertex belongs to one of the two terminal components; an invariant cut therefore permits no fixed vertex. Pairing configurations gives the exact even-count disjunction. The producer's compiler audit reports the three standard foundational axioms only.

**S4-COEFFICIENTS — ACCEPT on complete source review.** The actual Bernoulli product supplies coefficient two by counting configurations after excluding smaller events. The complemented failure polynomial is obtained from the full configuration sum. A constant complete quotient modulo two forces both primal and complemented reliability to equal `X^2`; both second coefficients would therefore be odd, contradicting the proved graph parity theorem. At an odd prime the endpoint values `-1,+1` already exclude a constant quotient. `GraphFixedPointStructure` combines these facts without an extra hypothesis; the lead reports its successful compilation.

**S4-IRREDUCIBLE-ENDPOINT — ACCEPT on complete source review, final integrated compile pending.** `IrreducibleCommensurability` supplies the actual graph no-integer-power result from irreducibility of the complete quotient; no reduction, valuation, divisibility, degree or no-power premise is left. It obtains pivotal transcendence using GS, three-dimension independence using mass nonsplitting, and actual pair commensurability using six exponentials. The remaining two arithmetic hypotheses are precisely the manuscript's irreducibility and nonsplitting conditions. The replacement coefficient recurrence allows this theorem to be complete without first proving the standalone full-degree lemma.

**S4-DEGREE — REVISE any claim of completion.** `FixedPointDegree` proves the actual degree upper bound, the exact alternating top-coefficient formula, and an iff between full degree and nonvanishing. It does not yet prove nonvanishing from canonicality. The decisive missing result is: for every actual classical rule, the alternating sum of crossing configurations, weighted by `(-1)^(edges-openCount)`, is nonzero. This is the manuscript's connected-matroid/Crapo-beta step. The generic degree identity for the quotient cannot substitute for that missing graph theorem. The construction and evidence agents remain assigned to this gap; no stopping recommendation is based on a file count or elapsed time.

### Completion accounting and interpretation boundary

Using the milestone weights fixed before results, the provisional finite-rule arithmetic accounting is:

| Obligation | Weight | Level | Credit |
|---|---:|---:|---:|
| Actual graph algebraicity | 10 | 1 | 10 |
| Rank, common primitive base, arbitrary-family scale-log rank | 30 | 1 | 30 |
| Actual graph iteration and aligned iff | 10 | 1 | 10 |
| Complete polynomial structure | 20 | 0.75 | 15 |
| Irreducible criterion, with exact manuscript arithmetic hypotheses | 20 | 1 after integration passes | 20 |
| Exact examples and authorized transcendence consequences | 10 | 1 | 10 |

This is **95/100 provisionally**, or 90/100 if the final integrated irreducible module has not passed. The polynomial credit explicitly excludes the unproved standalone full-degree claim. The number counts discharged proof obligations in the stated scope; it is not a probability that remaining proofs will work, a token/time efficiency score, or evidence that the whole manuscript has been formalised.

There is also a semantic boundary outside these local arithmetic milestones. `Rule.criticalDimensions` denotes the actual finite-growth logarithmic formulas, and `criticalDimensions_finite_growth` connects them to actual finite-network limits. Existing `FiniteCore.lean` explicitly states that its ambient-growth result is not a Hausdorff-dimension theorem and that its fixed-point geometry is not an identification of the infinite-volume percolation threshold. I did not find a Lean theorem here deriving equality of these tuples from a separately formalised infinite physical critical-exponent universality class. Thus **ACCEPT** the arithmetic conclusions for actual finite rules sharing the proved growth tuple; **REVISE** any unqualified statement of literal complete infinite-lattice/physical-class formalisation. One may apply the Section 4 arithmetic after the paper's earlier identifications, but must distinguish that mathematical interpretation from an imported checked Lean theorem.

The strongest remaining objection is therefore precise, not a general distrust of the result: full-degree nonvanishing is still unproved, and the physical interpretation must not silently become a new axiom. The decisive next checks are the canonical nonvanishing proof, the complete source-closure compilation and axiom audit, and an explicit final statement of the finite-growth scope. Six exponentials and GS are user-authorized established external theorems and are not unresolved proof gaps.

**Additional final source checks — ACCEPT with exact scope.** The added `common_primitive_base_of_irreducible_fixedPoint` handles arbitrary nonempty actual graph families through an explicit reference and requires the two arithmetic hypotheses only on that reference. `GraphCanonicalAugmentation` proves that every original edge is on a simple cycle with the genuinely new terminal edge, every vertex lies on a terminal path, and deletion of any vertex leaves the augmented graph preconnected. These are useful proved graph prerequisites, but they do not yet supply the alternating-coefficient nonvanishing or a beta-invariant positivity theorem. They therefore do not change the provisional polynomial milestone credit.

## Continued full-degree work in the same round

The lead confirmed successful compilation of the integrated irreducible criterion. The finite-rule accounting is therefore 95/100 rather than the earlier conditional 90/100. No credit has yet been added for canonical nonvanishing.

**S4-DELETE-CONTRACT — ACCEPT on complete source review.** `FixedPointDeletionContraction` permits repeated edges, loops, and coincident terminals in an endpoint-indexed model. `Linked` is the equivalence closure of the oriented open endpoint relation, so it describes ordinary undirected reachability. The closed-head and open-head connectivity bridges are proved by relation induction. The exact signed coefficient recurrence follows by splitting all Boolean configurations at the head; opening contributes the contracted coefficient and closing its negative. This statement does not assert positivity.

**S4-DELETE-VERTEX — ACCEPT on complete source review and producer build.** `GraphDeletionContractionConnectivity` proves that edge deletion preserves every vertex-deletion preconnectedness, or deletion of both edge endpoints is preconnected. When deletion fails, its two endpoints lie in different components after the offending vertex is removed; otherwise the existing nonbridge theorem restores connectivity. Each remaining vertex can be joined to the offending vertex while avoiding both endpoints. The two prefix arguments correctly use path simplicity to exclude the final vertex before its first endpoint encounter. Neither a finiteness assumption nor an unstated lower bound on the number of vertices is used.

**S4-DEGREE-SIGN — REVISE the initial natural-subtraction normalization.** The unparenthesized natural expression `edges - vertices.card + 1` has the wrong sign on a tree with `edges = vertices.card - 1`. The implementation now uses `(-1)^(edges + vertices.card + 1)`, which has the intended parity without truncated subtraction. A connected supported active vertex set is essential: counting extraneous isolated vertices would change the sign. The deletion/contraction induction must retain this active-set invariant.

**Reviewer-authored cancellation and alternate path lemmas — producer compilation passed, lead audit required.** `FixedPointCoefficientCancellation` proves vanishing when the head coordinate leaves terminal connectivity unchanged, and when the fully open graph fails to connect the terminals. `GraphEdgeNonbridge` proves an alternate endpoint path from vertex-deletion preconnectedness and an explicit third vertex. Both modules report only the three foundational axioms. The latter uses paths avoiding the two endpoints separately, so it covers arbitrary vertex types without a finite-cardinality premise. These are supporting lemmas, not a replacement for the still required strict positivity induction.

**S4-ACTIVE-CONTRACTION — ACCEPT on complete source review and producer build.** `GraphIndexedVertexConnectivity` transports the dichotomy to actual indexed minors. For the merged vertex it uses the original graph with both endpoints removed; for any other removed vertex it uses a surjective weak graph map from the original vertex-deleted graph. A weak map expressly permits an edge to collapse to a point. The deletion branch uses inclusion from the simple-edge-deleted graph into the actual indexed-deletion graph, thereby preserving parallel-edge and virtual-terminal-edge cases. The active set is erased exactly once on contraction; no isolated vertices are silently removed.

**S4-NONNEGATIVE — ACCEPT on complete source review and producer build.** `FixedPointBridge` characterizes connectivity after adding the head edge. When it is a full-graph bridge and the terminals remain connected after deletion, that coordinate is irrelevant for every configuration, so the signed coefficient cancels. `FixedPointCoefficientSign` treats loops first, has an exact zero-edge singleton base, and proves general nonnegativity on supported connected active sets. In the bridge case with disconnected terminals the deleted coefficient is exactly zero. The proof does not apply a connected-graph sign theorem to a disconnected deletion.

**S4-STRICT-POSITIVE — ACCEPT on complete source review and producer build.** `FixedPointConnectedFromVertex` proves that a nonempty loopless indexed network with distinct terminals and vertex-connected augmentation is connected on its active set. With two active vertices any existing loopless edge joins the terminals; with a third vertex the alternate path lemma removes the virtual terminal edge. It also proves that a genuine head bridge must separate the terminals under these geometric conditions. `FixedPointCoefficientPositive` then handles zero and one edge separately, sends parallel or direct-terminal heads through deletion, and excludes both cases before invoking strict positivity of a contraction. This order preserves looplessness and distinct terminals in the chosen strict minor. Every step adds one positive minor coefficient to a proved nonnegative minor coefficient. The producer reports only the three foundational axioms; no Crapo-beta, matroid-connectivity, or nonvanishing axiom is introduced.

The reviewer-authored actual coefficient bridge has also compiled. Its identity holds for every original `FiniteNetwork`, including networks with isolated vertices or repeated edges, because it only compares the same Boolean configurations and connectivity events. The final `GraphFixedPointDegree` wrapper is currently being compiled; no completion upgrade is recorded until this actual-graph endpoint passes and the lead reviews this reviewer-authored integration.

## Actual full-degree closure and final substantive accounting

**S4-DEGREE — ACCEPT, superseding the earlier open disposition.** `GraphFixedPointDegree.lean` has compiled successfully, including its final warning-free source, and the lead has independently read and accepted the reviewer-authored wrapper. `Classical.integerReliabilityPolynomial_natDegree` proves that the actual integer Bernoulli polynomial has degree equal to the actual edge count. `Classical.integerFixedPointPolynomial_degree` proves the literal polynomial degree of the complete quotient equals `edges - 2` in `WithBot Nat`; the quotient is explicitly proved nonzero. The rational coefficient versions are also provided. The only premise at this actual-graph endpoint is `Rule.Classical`; no positivity, nonzero leading coefficient, minor connectivity, or exact-degree premise remains. The reported axiom lists contain only `propext`, `Classical.choice`, and `Quot.sound`.

The proof uses the existing canonical terminal paths to establish vertex connectivity of the augmented actual graph, then applies the fully proved indexed deletion–contraction positivity theorem on the entire original vertex set. The exact coefficient bridge identifies its signed sum with the actual highest coefficient. The degree upper bound and complete quotient identity finish the argument. This is a replacement proof of the manuscript statement, without importing a Crapo-beta positivity theorem as a new external assumption.

The predefined finite-rule Section 4 obligation score is now **100/100**:

| Obligation | Weight | Final level | Credit |
|---|---:|---:|---:|
| Actual graph algebraicity | 10 | 1 | 10 |
| Rank, common primitive base, arbitrary-family scale-log rank | 30 | 1 | 30 |
| Actual graph iteration and aligned iff | 10 | 1 | 10 |
| Complete fixed-point polynomial structure, including exact degree | 20 | 1 | 20 |
| Irreducible criterion with exact manuscript arithmetic hypotheses | 20 | 1 | 20 |
| Exact examples and authorized transcendence consequences | 10 | 1 | 10 |

This supersedes the historical 95/100 checkpoint. The lead's final dependency-closure replay, source/object hash audit, archive update, and publication checks remain pending. It is not yet a claim that those delivery checks have completed or that a fresh portable `lake build` has run. The score concerns the six predefined finite-rule arithmetic obligations only. The physical-exponent-to-growth-tuple interpretation remains the separate Section 3 interface described above.

**Statement-map cross-check — ACCEPT with documentation updates sent to the lead.** Every numbered theorem, lemma, definition, example, and corollary from `sec:scale` through `cor:diamond-commensurability` has an implementation entry. The precise-degree row and old text saying that this degree remains open must now be updated. The final unnumbered consequence, rational pivotal dimension implies reducibility of the complete quotient, is a direct contrapositive of the proved no-integer-power/transcendence theorem; a named corollary and explicit table row were requested for clarity. The opening `conj:scale-commensurability` is a conjecture, not an additional theorem to assume or prove here; Section 5's claimed counterexample construction is outside this round's target. No claim about its resolution follows from the present formalisation.

**Stopping criterion.** There is no remaining mathematical gap among the six predefined finite-rule obligations. After the final complete dependency audit and authorized delivery succeed, ending this round is justified by completion of that scope, not elapsed time, effort, file counts, or a heuristic stopping rule. The separate physical interpretation and Section 5 construction must remain explicit boundaries of the final report.

**S4-RATIONAL-PIVOTAL — ACCEPT, final supplementary statement check.** `RationalPivotalObstruction` now gives the named actual-graph conclusion `Classical.not_irreducible_fixedPoint_of_rational_pivotal_dimension`, including the equivalent rational-range formulation. It first derives pivotal irrationality directly from the proved integer-power obstruction and then takes the contrapositive. There is no mass-nonsplitting premise and no use of GS or six exponentials; the producer's three axiom lists contain only the foundational three. This closes the documentation request about the section's final unnumbered consequence. The explanatory identification of a nonsplit mass quadratic with its irreducible minimal polynomial is already supported by `nonsplit_quadratic_minpoly`; a separately named converse is not used as an extra assumption by the main theorem.

## Lead final integration verification

2026-10-06 15:56:57 UTC: PASS. The final 289-module closure rebuilt 28 modules and reused 261 only after recursive source/object/environment validation. All 3046 kernel declarations originating in 287 project modules passed the five-item axiom allowlist. The final source/object hashes and actual compiler/package environment were rechecked. This supersedes all historical pending-build dispositions above; the stated Section 3 and Section 5 scope boundaries remain.

Final publication: draft PR https://github.com/Nero-17/LEAN-Formalisation-IGS-Bernoulli-percolation-universality-class/pull/1 on codex/section4-independent was verified at proof commit c6adbe81800628942bb07ba933321c8481e2c8bf. All mathematical and integrated-build pending items above are closed; subsequent record-only updates do not alter Lean sources.
