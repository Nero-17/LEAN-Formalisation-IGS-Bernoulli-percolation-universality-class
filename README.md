# Hierarchical-percolation universality in Lean

This repository formalises selected arguments from *Iterated Graph Systems (II):
Bernoulli percolation and universality class on hierarchical lattices*.

Source manuscript at the start of this work: Overleaf Git commit `6270a59`.
Lean: **4.32.1**. Mathlib: **520045ab14e26149ee970e2e617ca04b09bde5d6**.

## Scope and trust

The project is in progress. A compiled matrix identity is not advertised as a
formal proof about actual hierarchical lattices until the graph and probability
bridges have been proved. Likewise the physical critical-exponent definitions
are not replaced with their desired formulas. Missing analytic results will not
be hidden behind axioms or `sorry` in the verified library.

The primary initial target is the finite-graph noncommutative obstruction in
Section 3.2. Section 5 certificate verification is a subsequent target. The
four exponent-existence theorems and the infinite-volume model are not yet
formalised.

## Build

The Lake files pin the toolchain and exact mathlib revision. A conventional
fresh environment can use `lake build`; the build actually verified during
development is the dependency-ordered command `./scripts/build.ps1` below.
The Windows development environment has the dependencies cached at
`C:/Users/lzysh/Documents/Codex/lean32/packages`. The helper
`scripts/check.ps1 -Module <module>.lean` uses that cache and calls Lean directly;
it never substitutes native computation for a proof. It writes checked object
files under `.lake/build/lib/lean`. Its cache and compiler paths can be overridden
with the `PackageCache` and `LeanBin` parameters.

`./scripts/build.ps1` recursively checks every project import of `Audit.lean`,
then prints the axioms of the milestone theorems. It writes per-module exit
codes and elapsed build times to `docs/build-results.json`. The four data
modules also contain ordinary kernel-checked `decide` proofs. No native
evaluation is substituted for their proofs.

## Verified core

* `Percolation/FiniteNetwork`: finite two-terminal edge-indexed networks,
  graph-theoretic connectivity, three live states, fair conditional expectations.
* `Percolation/Wheatstone`: the genuine five-edge graph, kernel-checked exact
  configuration counts and its two-dimensional conditional mass block.
* `Matrix/TwoByTwo`: the rational trace discrepancy, determinant equality and
  the algebraic common-root obstruction.
* `Matrix/SpectralSeparation`: disjoint spectra over characteristic-zero fields.
* `Algebra/MultiplicativeObstruction`: any family of scalar multiplicative
  observations forgets the displayed rearrangement of factors. Applying this
  to a physical class requires the graph and exponent theorems separately.
* `Graph/Reachability`: a verified finite breadth-first search used to make
  subsequent configuration enumeration practical.
* `Percolation/Bernoulli`, `ReliabilityPolynomial`, `ReliabilityDerivative`:
  actual finite probabilities, conditional mass expectations, configuration
  polynomials, their Bernstein expansion, and the real derivative.
* `Matrix/PositiveEigenvector`, `PositiveTwoByTwo`, `MassPlane`:
  positive-vector certificates for the actual complex spectral radius and
  the passage between the full three-state operator and its invariant plane.
* `Matrix/PopulationGrowth`, `Percolation/FirstMoments`:
  first-moment recursion, matrix powers, geometric bounds and logarithmic
  growth limits. Their identification with glued infinite graph clusters
  remains separate.
* `Arithmetic/Commensurability`: finite blocking, rational logarithmic ratios
  and pairwise incommensurability of `(19 * 661^k)^100`.
* `Algebra/WordExpansion`, `GroupedWords`, `PacketCancellation`:
  ordered expansions, weighted grouped sums and the signed commutator packets.
* `Certificates/Data/*`: all four supplied integer datasets satisfy their
  scale, volume and thermal moment identities. This does **not** yet certify
  the full mass-spectrum or graph-realisation part of those large examples.

`Percolation/OppositeWheatstone.lean` is still a development target and is not
imported by the verified root until its larger enumeration finishes. The
exact scope, failed approaches and remaining bridges are recorded in the
single round report under `docs/`.

Completed modules and their dependencies will be listed in the round report
and audited using Lean's `#print axioms` command.
