"""Exact exhaustive check of the Section 3 noncommuting witness."""
if not __debug__:
    raise RuntimeError("Run without -O or -OO.")
from fractions import Fraction as F
W=[(0,2),(2,1),(0,3),(3,1),(2,3)]
B=[(2,1),(0,3),(2,3)]
for x,y,base in [(0,2,4),(3,1,6)]:
    mapping={0:x,1:y,2:base,3:base+1}
    B += [(mapping[a],mapping[b]) for a,b in W]
def response(edges):
    counts=[[0]*3 for _ in range(3)]
    denominators=[0]*3
    derivative=0
    vertices=max(max(e) for e in edges)+1
    for mask in range(1<<len(edges)):
        parent=list(range(vertices))
        def find(x):
            while parent[x]!=x:
                x=parent[x]
            return x
        for k,(a,b) in enumerate(edges):
            if mask>>k&1:
                parent[find(a)]=find(b)
        roots=[find(i) for i in range(vertices)]
        connected=roots[0]==roots[1]
        if connected:
            derivative+=2*mask.bit_count()-len(edges)
        for row in ([0] if connected else [1,2]):
            denominators[row]+=1
            active={roots[0],roots[1]} if row==1 else {roots[0]}
            for k,(a,b) in enumerate(edges):
                ends=int(roots[a] in active)+int(roots[b] in active)
                if ends==2:
                    counts[row][0 if mask>>k&1 else 1]+=1
                elif ends==1:
                    counts[row][2]+=1
    M=[[F(x,denominators[i]) for x in row] for i,row in enumerate(counts)]
    return [[M[0][0],2*M[0][1]+M[0][2]],
            [M[2][0],2*M[2][1]+M[2][2]]],F(derivative,2**(len(edges)-1)),denominators[0]
def mul(a,b):
    return [[sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
def trace(a): return a[0][0]+a[1][1]
ma,da,ca=response(W)
mb,db,cb=response(B)
assert ma==[[F(53,16),F(48,16)],[F(13,16),F(42,16)]]
assert mb==[[F(1896,256),F(2292,256)],[F(627,256),F(1380,256)]]
assert (da,db,ca,cb)==(F(13,8),F(67,32),16,4096)
difference=trace(mul(mul(ma,ma),mul(mb,mb)))-trace(mul(mul(ma,mb),mul(ma,mb)))
assert difference==F(-1521,4194304)
print('Exact enumeration verified: 32 and 8192 configurations; crossing probabilities, derivatives, both mass blocks, and trace difference',difference)
