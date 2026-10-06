# Hierarchical-percolation universality in Lean


This project formalises *Iterated Graph Systems (II): Bernoulli percolation and
universality class on hierarchical lattices*. The Overleaf manuscript was not
modified in this formalisation round.

Lean **4.32.1**; mathlib **520045ab14e26149ee970e2e617ca04b09bde5d6**.
Manuscript source: Overleaf `69b4d5f8e9e9b26ffd015f17`, frozen Section 3 at
commit `fccfba64fd345f8b0cbaafd94abec48420c0c6fa`.

## Current verification status

**The original Section 3 is formalized and verified**, including its additional
four-exponent material later moved to an appendix. The complete build passed
**863 modules / 956 ordered kernel axiom outputs / 136 certificate batches**
at 2026-10-06T20:05:04.0560222Z. Source/build verification reports zero errors and
only the standard logical axioms. Code commit: `5b80bbe96fd5d55e4ce2ee03e3576665d5e37eb6`.

Start with [Universality/Section3.lean](Universality/Section3.lean), the complete
[statement coverage map](docs/SECTION3_COVERAGE.md), or the single continuous
[R077 report](docs/R077_完整研究记录.md). Post-build source/object/dependency
fingerprints are in `docs/section3-final-integrity.json`. Historical Section 2
and earlier Section 3 evidence remains in the R071/R072/R074/R075 reports.

## Section 3 scope

The definitions use actual finite edge-indexed graphs, independent Bernoulli
configurations, graph reachability, and uniform-vertex sampling. Matrix and
birth-series identities are derived from these observables.

- Actual internal-vertex mass recursion and all integer moment bounds; a common
  coherent history probability space and the actual mass L² limit; smoothing,
  nonlattice limits, smooth normalized densities, strict single-state positive
  support, all-integer uniform local limits and arbitrary-order point bounds.
- An actual age-mixture rooted direct-limit graph, finite-stage Bernoulli laws,
  almost-sure local finiteness, full rooted-ball local weak convergence, and
  identification of its finite/infinite component probabilities.
- The four physical exponents beta, crossing nu, point-size delta and averaged
  eta: existence, uniqueness, formulas, and classification by three explicit
  dimensions. Eta uses every fixed ambient-distance window 0<a<b<1.
- Finite-cluster moments at fixed and near-critical parameters, exact thresholds
  including equality, power/logarithmic bounds, subthreshold continuity,
  susceptibility and adjacent-moment gap exponents, and the common-gap criterion.
- Actual cluster-number density as the sum of finite-cluster probabilities
  divided by size; the functional equation, uniqueness, analytic extension,
  critical regularity and raw-alpha criterion; diamond, central-Wheatstone and
  Wheatstone alpha examples, including a strong Wheatstone third-response bound.
- Actual ambient-radius tail and point events, critical power tails, the
  necessary point exponent value, and a genuine diamond spike construction
  proving that its point logarithmic exponent does not exist.
- Arbitrary cyclic substitution words, actual noncommutative classical models
  with different physical classes, and failure of arbitrary multiplicative
  observations to classify. Connected unit resistances multiply under
  substitution; Tie/Gem have resistance 4/3.

The newest graph/radius, cluster-number, LLT normalization and electrical
bridges are all included in the successful complete build, with the numerical examples.
The ambient Hausdorff theorem is reused from the separate completed R080
geometry work: 22 frozen new source modules, with 117 shared identical
project dependencies, have been recompiled and verified here. No upstream object files or
arithmetic external axioms are imported. New classification wrappers use the
Hausdorff dimension of the actual compact generation metric space directly.

## Precise conventions and boundaries

- `outer * inner` replaces each edge of `outer` by `inner`, corresponding to
  manuscript `inner ∘ outer`.
- `generation n` is manuscript depth `n+1`. The exact paper LLT wrapper uses
  `rho^(n+1)`, density `rho * w(rho*x)`, and the same history limit divided by
  `rho`; this is a proved density/law transformation, not an absorbed constant.
- The actual accumulated vertex mass has L² convergence. Its full-sequence
  almost-sure convergence is not claimed. The associated population martingale
  has its separately proved almost-sure convergence.
- Rooted local weak convergence is expressed by probabilities of every finite
  rooted-ball isomorphism event. No unlabelled graph quotient topology is
  introduced. Exact-radius events mean that the ambient maximum is attained
  at the specified integer; their definition is not a birth series.
- At p=0 the positive-subcritical moment divergence criterion does not apply.
  For p=1 all finite-cluster moments are finite. Infinite ENNReal moments are
  not interpreted through their real coercion as finite quantities.
- Physical kappa is defined on probabilities p in [0,1]. Its auxiliary real
  zero extension is not asserted to be analytic across endpoints; the precise
  endpoint statement is interval analyticity or existence of an analytic
  extension equal to the observable on [0,1].
- The cluster-number regularity proposition has a different verified proof.
  Its proof's optional linearizing coordinate, log-periodic amplitude and
  resonant display formulas are not separately formalized claims here.
- Real reciprocal resistance is physically interpreted only for connected
  networks. All Classical uses are connected and have positive conductance;
  the totalized zero value at a disconnected network is not physical infinity.
- Section 4 and Section 5 are developed in separate worktrees/rounds. Their
  completion status is not inferred from this repository's partial arithmetic
  or integer-certificate files. R077 did not modify their worktrees.

## Build and trust

The command actually checked in this environment is:

```powershell
./scripts/build.ps1
```

It dependency-orders every project import of `Audit.lean`, calls Lean on each
source, and prints milestone axiom dependencies. `docs/build-results.json`
records source SHA256, check time, exit code and duration. After a checked full
build, `./scripts/build.ps1 -ReuseVerified` recompiles new or changed sources and
their importing modules, retaining records for unchanged sources. The default
command rebuilds everything.

The Windows helper defaults to the shared dependency cache
`C:/Users/lzysh/Documents/Codex/lean32/packages` and the installed Lean 4.32.1
binary. Override `PackageCache` and `LeanBin` to change those paths. Dependencies
are pinned by `lean-toolchain`, `lakefile.toml` and `lake-manifest.json`. A standard
Lake build is the intended portable route, but **a fresh `lake build` has not been
verified in this round**. The direct Lean build is the verification evidence.
`lake --no-cache env lean Universality/Percolation/ClassicalCriticalPoint.lean`
was also checked successfully using the same installed dependencies. On this
shared Windows cache, Git ownership exceptions were limited to the exact package
directories in that one process; no global Git configuration was changed.

The checked library contains no `sorry`, `admit`, `native_decide`, or added
mathematical axioms. The audit reports only `propext`, `Classical.choice` and
`Quot.sound`; some finite certificates need only `propext`. Finite computations
use proof-producing tactics checked by Lean's kernel. All literals needed for
compilation are already in the source. Regenerating manuscript integer inputs
requires the original certificate JSON files, whose hashes are recorded in `docs/`.

