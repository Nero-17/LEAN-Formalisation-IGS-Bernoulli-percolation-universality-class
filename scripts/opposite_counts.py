"""Development cross-check only. The Lean theorem will verify the same numbers."""
from itertools import product
edges = [(2,1),(0,3),(2,3),(0,4),(4,2),(0,5),(5,2),(4,5),
         (3,6),(6,1),(3,7),(7,1),(6,7)]
counts = [[0]*3 for _ in range(3)]
cardinalities = [0]*14
for bits in product((False, True), repeat=13):
    comp = list(range(8))
    def find(x):
        while comp[x] != x:
            x = comp[x]
        return x
    for opened, (a,b) in zip(bits, edges):
        if opened:
            comp[find(a)] = find(b)
    roots = [find(x) for x in range(8)]
    connected = roots[0] == roots[1]
    if connected:
        cardinalities[sum(bits)] += 1
    for row in ([0] if connected else [1,2]):
        active = {roots[0], roots[1]} if row == 1 else {roots[0]}
        for opened, (a,b) in zip(bits, edges):
            ends = (roots[a] in active) + (roots[b] in active)
            if ends == 2:
                counts[row][0 if opened else 1] += 1
            elif ends == 1:
                counts[row][2] += 1
print('Counts:', counts)
print('Crossing counts by number of open edges:', cardinalities)
