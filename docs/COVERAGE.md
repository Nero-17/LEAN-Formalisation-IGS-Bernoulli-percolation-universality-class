# Mathematical coverage and cross-section interfaces

## Common foundations

The sections share `Universality.Rule`, the same finite-network reliability
polynomial and three-state mass matrix. No section replaces a physical observable
with its desired formula as a definition. The compact rescaled generation
completion and its actual Hausdorff dimension are shared geometry results.

## Section 2

Finite Bernoulli configurations, conditional live states, exact random substitution
laws and mass recursions feed the critical Perron theory.

Manuscript Theorem 2.9 is implemented concretely in
`Geometry/PercolationTheorem29.lean`, with endpoint
`Rule.classical_percolation_graphDirected_gromovHausdorff`.
For every classical rule and its interior fixed point, the actual
terminal-connected clusters converge almost surely in mathlib's GH space under
the existing conditional Bernoulli history law. Their metric is the inherited
rescaled ambient graph metric, not the intrinsic open-path metric.

`percolationClusterVertices` uses actual reachable vertices in the compact
generation completion. Coarse-graining makes these sets increasing; compactness
gives Hausdorff convergence, and continuity of `NonemptyCompacts.toGHSpace`
gives GH convergence. This is an alternate proof of convergence, without a new
quantitative rate assertion. `Rule.percolationCellConfiguration_coherent` proves that actual
child configurations inherit coherence. `percolationCellState_eq` identifies
their depth-independent oriented terminal states.

`PercolationCellProcess.graphDirected_at_every_address` gives the exact set
equation at every finite address using `generationMetricCell`, whose distance
identity has ratio the reciprocal terminal distance. The child sets are the
closures of the actual terminal-selected vertices; no compatible geometric
realisation is assumed. `percolationCell_conditional_joint_weight` identifies
the complete conditional product law of child configurations, and
`ConfigurationHistory.infinite_randomEIGS_joint_law` identifies all finite-history
label observables on the same infinite probability space. Terminal conditioning
holds almost surely at every generation by `infiniteLaw_terminal_condition`.

This closes the concrete interface formerly missing from the generic
`GraphRealisation` and `TypedGraphRealisation` lemmas. It does not assert a
scaling-limit theorem for arbitrary random EIGS. Lean generation zero is the
first substituted graph (paper generation one).

## Section 3 and the appendix

`Universality.Section3` gathers the actual annealed uniform-root probability
model, rooted local limits and local finiteness; mass L² limits, smoothing and
point-size asymptotics; and the existence and formulas for beta, crossing nu,
point-size delta and window-averaged eta. Their class is equivalent to equality
of the three dimensions. The noncommutative example, cyclic invariance,
multiplicative-invariant obstruction and Tie/Gem interval certificates are included.

The supplementary exponents retain their exact qualifications: finite-cluster
moment thresholds for gamma and Delta; raw-alpha regularity and background
conditions; cumulative radius tails and point-radius nonexistence examples.
This does not assert unconditional existence of all eight traditional exponents.
Window-averaged eta is not a pointwise two-point theorem. L² convergence of
internal vertex mass is not silently upgraded to full-sequence almost-sure convergence.

## Section 3 to Section 4

`Universality.Arithmetic.GraphPhysicalClass` imports
`Universality.Percolation.PhysicalExponentClass`. Its
`Classical.same_physical_class_iff_criticalDimensions` proves the bridge from
the actual four-exponent class to the arithmetic dimension vector. The rank and
irreducibility commensurability conclusions then apply to that physical class.
`Section4Complete` also includes the actual compact Hausdorff geometry.

The six-exponentials criterion is sufficient under the stated rational-rank
condition. The irreducibility criterion retains its actual-field and nonsplitting
hypotheses; neither is a universal commensurability theorem.

## Sections 2–4 to Section 5

`Universality.Section5` combines the actual Wheatstone rule construction,
Bernoulli identities, spectral calculations and all four exact allocation
certificates with the shared geometry and physical-class results.

The seed scales are 19^100, 661^100 and 739^100; their logarithms are rationally
independent. The family with scales (19 * 661^k)^100 is unbounded and pairwise
incommensurate in one actual physical class. Its dimensions are 58/25, 219/100,
7/10, with beta = 13/70, nu = 10/7, delta = 219/13 and averaged eta = -3/50.

The shifted rule has scale 19^100 + 480. All three dimensions are transcendental
but rationally proportional. This is a single-rule example, not a counterexample
consisting of two incommensurate rules in a common irrational-dimension class.
The four-exponentials consequences remain conditional.

## Scope of verification

Formalisation covers stated mathematical conclusions using the indicated models
and hypotheses; it does not mean every displayed intermediate argument in the
manuscript has been translated line by line. Alternate proved arguments are used
where appropriate. See BUILD.md for the distinction between the fresh aggregate
audit and verified reuse of previously compiled dependencies.
