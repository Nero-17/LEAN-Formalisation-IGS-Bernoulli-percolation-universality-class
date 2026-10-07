"""Root's independent integer-only replay of the explicit 19/661 graph pair.

Reads only floor counts, lex remainders and packet coefficients. It never
reads the rational-interior certificate and imports none of the producer's
code. Re-enumerates the original 32-state three-type kernel from connectivity.
"""
if not __debug__:
    raise RuntimeError('Run without -O/-OO: exact certificate assertions must remain enabled.')
from pathlib import Path
from math import comb
from itertools import product
import json, sys, time, hashlib
sys.set_int_max_str_digits(0)
ROOT=Path(__file__).resolve().parent

def original_kernels():
    edges=[(0,2),(1,2),(0,3),(1,3),(2,3)]
    out=[[[0]*3 for _ in range(3)] for _ in edges]
    connected=0; connected_by_configuration={}
    for bits in product((0,1),repeat=5):
        adj=[[] for _ in range(4)]
        for yes,(u,v) in zip(bits,edges):
            if yes:adj[u].append(v);adj[v].append(u)
        def component(s):
            seen={s}; todo=[s]
            while todo:
                for v in adj[todo.pop()]:
                    if v not in seen:seen.add(v);todo.append(v)
            return seen
        source,sink=component(0),component(1)
        is_connected=1 in source
        connected_by_configuration[bits]=is_connected
        connected+=is_connected
        types=[(0,source)] if is_connected else [(1,source|sink),(2,source)]
        for row,active in types:
            for e,((u,v),yes) in enumerate(zip(edges,bits)):
                count=(u in active)+(v in active)
                if count:
                    col=(0 if yes else 1) if count==2 else 2
                    out[e][row][col]+=1
    assert connected==16
    pivotal=[]
    for e in range(5):
        count=0
        for bits,yes in connected_by_configuration.items():
            if bits[e]==0:
                opened=list(bits);opened[e]=1
                count+=int(connected_by_configuration[tuple(opened)])-int(yes)
        pivotal.append(count)
    assert pivotal==[6,6,6,6,2]
    # Denominator 16: the other four effective edges are independent fair bits.
    # Paired arm derivative 12/16=6/8; center 2/16=1/8; total 26/16=13/8.
    pair=lambda a,b:[[out[a][i][j]+out[b][i][j] for j in range(3)] for i in range(3)]
    K,J=pair(0,3),out[4]
    assert K==pair(1,2)
    return K,J

def mv3(A,v):return [sum(a*b for a,b in zip(row,v)) for row in A]
def induced(A):
    columns=[]
    for v in ([1,0,0],[0,2,1]):
        w=mv3(A,v);assert w[1]==2*w[2];columns.append((w[0],w[2]))
    return (columns[0][0],columns[1][0],columns[0][1],columns[1][1])
def mm(A,B):
    a,b,c,d=A;e,f,g,h=B
    return a*e+b*g,a*f+b*h,c*e+d*g,c*f+d*h
def mv(A,v):return (A[0]*v[0]+A[1]*v[1],A[2]*v[0]+A[3]*v[1])
def plus(a,b):return tuple(x+y for x,y in zip(a,b))
def scale(k,a):return tuple(k*x for x in a)
def rank_word(w):
    remaining=w.count('0'); rank=0
    for i,ch in enumerate(w):
        if ch=='0':remaining-=1
        elif remaining:rank+=comb(len(w)-i-1,remaining-1)
    return rank

def verify(folder, expected_base, expected_n, scale_offset=0):
    started=time.monotonic()
    input_bytes={name:(folder/name).read_bytes() for name in ['word_base.json','packet_repair.json']}
    base=json.loads(input_bytes['word_base.json'])
    packets=json.loads(input_bytes['packet_repair.json'])
    n=expected_n;b=expected_base;c=base['candidate']
    assert c==packets['candidate'] and c['n']==n and c['s']==b
    assert c['ell']==b**100+scale_offset
    assert all(c[k]==b**e for k,e in [('m',232),('r',219),('q',70)])
    N=base['Nz'];floors=base['floor_groups'];remainders=base['lex_remainders']
    assert len(N)==len(floors)==len(remainders)==n+1
    K3,J3=original_kernels()
    A3=[[2*K3[i][j]+J3[i][j] for j in range(3)] for i in range(3)]
    D3=[[A3[i][j]-16*(i==j) for j in range(3)] for i in range(3)]
    assert all(x>0 for row in A3+D3 for x in row)
    K,J,A,D=map(induced,[K3,J3,A3,D3])
    v=(55,23);delta_v=mv(D,v);original_v=[55,46,23]
    assert mv3(D3,original_v)==[delta_v[0],2*delta_v[1],delta_v[1]]
    eye=(1,0,0,1);zero=(0,0)
    Q=[[delta_v]]
    for d in range(1,n+1):
        Q.append([plus(mv(K,Q[d-1][z-1]) if z else zero,
                       mv(J,Q[d-1][z]) if z<d else zero) for z in range(d+1)])
    # Prefix decomposition into complete lexicographic cylinders, iterative.
    def lex_sum(d,z,r):
        ans=zero;prefix=eye
        while r:
            assert 0<r<=comb(d,z)
            if r==comb(d,z):return plus(ans,mv(prefix,Q[d][z]))
            first_size=comb(d-1,z-1) if z else 0
            if r<=first_size:
                prefix=mm(prefix,K);d-=1;z-=1
            else:
                if first_size:ans=plus(ans,mv(mm(prefix,K),Q[d-1][z-1]))
                prefix=mm(prefix,J);r-=first_size;d-=1
        return ans
    mass=zero;slack=[]
    for z in range(n+1):
        a,bfloor=floors[z];r=remainders[z]
        assert all(type(x) is int for x in (N[z],a,bfloor,r))
        count0=comb(n-1,z-1) if z else 0
        count1=comb(n-1,z) if z<n else 0
        assert 0<=r<=count0+count1
        assert N[z]==count0*a+count1*bfloor+r
        assert 0<=N[z]<=comb(n,z)*2**z
        bounds=[]
        if count0:
            assert 0<=a<=a+int(r>0)<=2**z
            bounds += [a,2**z-a-int(r>0)]
            mass=plus(mass,scale(a,mv(K,Q[n-1][z-1])))
        if count1:
            assert 0<=bfloor<=bfloor+int(r>count0)<=2**z
            bounds += [bfloor,2**z-bfloor-int(r>count0)]
            mass=plus(mass,scale(bfloor,mv(J,Q[n-1][z])))
        slack.append(min(bounds))
        mass=plus(mass,lex_sum(n,z,r))
    assert N[0]==0 and 2**n+N[n]==b**100+scale_offset
    assert 5**n+4*sum(2**z*x for z,x in enumerate(N))==b**232
    assert 8*13**n+5*sum(6**z*x for z,x in enumerate(N))==8**(n+1)*b**70
    C=tuple(x-y for x,y in zip(mm(K,J),mm(J,K)))
    assert C==(-6,-6,3,6) and mm(C,C)==scale(18,eye)
    exceptions=0
    assert len(packets['layers'])==n//4
    for t,layer in enumerate(packets['layers']):
        h=2*t+1;L=n-2*h
        assert (layer['t'],layer['h'],layer['suffix_length'])==(t,h,L)
        coeff=layer['coefficients'];assert len(coeff)==4 and all(type(x) is int for x in coeff)
        tails=['0'*L,'1'+'0'*(L-1),'1'*L,'0'+'1'*(L-1)]
        assert len(set(tails))==4
        if L>2:assert all(any(tail[j:j+2] in ('00','11') for j in (0,2)) for tail in tails)
        for a,tail in zip(coeff,tails):
            z=h+tail.count('0')
            if abs(a)>slack[z]:
                assert h<=12
                for pairs in product(('01','10'),repeat=h):
                    word=''.join(pairs)+tail
                    x=floors[z][int(word[0])]+int(rank_word(word)<remainders[z])
                    assert 0<=x+a*(-1)**pairs.count('10')<=2**z
                    exceptions+=1
            y=delta_v
            for letter in reversed(tail):y=mv(K if letter=='0' else J,y)
            y=mv(C,y)
            mass=plus(mass,scale(a*18**t,y))
    baseline=original_v[:]
    for _ in range(n):baseline=mv3(A3,baseline)
    final=[16*baseline[0]+mass[0],16*baseline[1]+2*mass[1],16*baseline[2]+mass[1]]
    assert final==[16**(n+1)*b**219*x for x in original_v]
    out={'status':'ROOT INDEPENDENT INTEGER-ONLY CERTIFICATE PASS',
         'base':b,'n':n,'mass_definition':'original three-state, re-enumerated from 32 configurations',
         'input_files':['word_base.json','packet_repair.json'],'rational_center_read':False,
         'full_PF_vector':original_v,'exponents':[100,232,219,70],
         'thermal_pivotal_numerators_reenumerated':[6,6,6,6,2],
         'thermal_pivotal_denominator':16,
         'explicitly_checked_exception_words':exceptions,
         'hashes':{name:hashlib.sha256(data).hexdigest() for name,data in input_bytes.items()},
         'seconds':time.monotonic()-started}
    print(json.dumps(out),flush=True)
    return out

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificates',type=Path,default=ROOT)
    parser.add_argument('--output',type=Path,default=ROOT/'verification.json')
    parser.add_argument('--third-certificate',type=Path,default=ROOT/'n952',help='Optional directory containing the base739/depth952 pair of JSON files.')
    args=parser.parse_args()
    root=args.certificates
    out=[verify(root/'n424',19,424),verify(root/'n936',661,936)]
    if args.third_certificate:out.append(verify(args.third_certificate,739,952))
    args.output.write_text(json.dumps(out,indent=2),encoding='utf-8')
