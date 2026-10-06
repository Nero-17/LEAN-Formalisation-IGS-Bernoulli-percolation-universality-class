"""Exact finite constants used in the uniform realisation lemma of Section 5."""
if not __debug__:
    raise RuntimeError("Run without -O or -OO.")
from fractions import Fraction as F
from math import isqrt,gcd
from pathlib import Path
import json
class IV:
 def __init__(self,a,b=None):self.a=F(a);self.b=F(a if b is None else b)
 def __add__(x,y):
  y=y if isinstance(y,IV) else IV(y);return IV(x.a+y.a,x.b+y.b)
 __radd__=__add__
 def __neg__(x):return IV(-x.b,-x.a)
 def __sub__(x,y):return x+-asiv(y)
 def __rsub__(x,y):return asiv(y)+-x
 def __mul__(x,y):
  y=asiv(y);vals=[u*v for u in [x.a,x.b] for v in [y.a,y.b]];return IV(min(vals),max(vals))
 __rmul__=__mul__
 def __truediv__(x,y):
  y=asiv(y);assert not y.a<=0<=y.b;return x*IV(1/y.b,1/y.a)
 def __rtruediv__(x,y):return asiv(y)/x
 def approx(x):return [float(x.a),float(x.b)]
def asiv(x):return x if isinstance(x,IV) else IV(x)
def sqrt(x):
 x=asiv(x);S=10**50
 lo=isqrt((x.a*S*S).__floor__());hi=isqrt((x.b*S*S).__floor__())+1
 return IV(F(lo,S),F(hi,S))
def mv(M,v):return [sum(M[i][j]*v[j] for j in range(2)) for i in range(2)]
def det(u,v):return u[0]*v[1]-u[1]*v[0]
s=sqrt(2617);nu=(95+s)/32;other=(95-s)/32
K=[[F(22,16),F(18,16)],[F(5,16),F(18,16)]];J=[[F(9,16),F(12,16)],[F(3,16),F(6,16)]];A=[[2*K[i][j]+J[i][j] for j in range(2)] for i in range(2)]
projector=[[(A[i][j]-(other if i==j else 0))/(nu-other) for j in range(2)] for i in range(2)]
w=mv(projector,[55,23]);u=[2*(nu-1)/nu*t for t in mv(K,w)];v=[(nu-1)/nu*t for t in mv(J,w)];rhs=[sqrt(nu)*a-b for a,b in zip([55,23],w)]
fK=det(rhs,v)/det(u,v);fJ=det(u,rhs)/det(u,v)
volume=(sqrt(5)-1)/4;thermal=(sqrt(F(13,8))-1)/F(5,8)
mu=(40+992/s)/(16*nu)
assert F(81,100)<mu.a and mu.b<F(82,100)
for x in [fK,fJ,volume,thermal]:assert F(1,5)<x.a and x.b<F(4,5)
C=[[-6,-6],[3,6]];Cw=mv(C,w);repair_det=det(mv(K,Cw),mv(J,Cw));assert repair_det.a>0 or repair_det.b<0
out={'mass_zero_fraction':mu.approx(),'volume_fraction':volume.approx(),'thermal_fraction':thermal.approx(),'mass_prefix_K_fraction':fK.approx(),'mass_prefix_J_fraction':fJ.approx(),'all_four_fractions_strictly_in':['1/5','4/5'],'aggregate_preserving_prefix_KC_JC_determinant':repair_det.approx(),'arithmetic':'Exact rational interval arithmetic with integer square-root enclosures'}
K0=(22,18,5,18);J0=(9,12,3,6);dv=(3139,1313)
def product2(a,b):return tuple(sum(a[2*i+t]*b[2*t+j] for t in range(2)) for i in range(2) for j in range(2))
def action(a,b):return tuple(sum(a[2*i+t]*b[t] for t in range(2)) for i in range(2))
C0=tuple(a-b for a,b in zip(product2(K0,J0),product2(J0,K0)))
assert C0==(-6,-6,3,6)
assert product2(C0,C0)==(18,0,0,18)
assert sum(dv)%3==0
for kernel in [K0,J0]:
 for generator in [(1,-1),(0,3)]:assert sum(action(kernel,generator))%3==0
 for generator in [(18,0),(0,3)]:
  value=action(kernel,generator);assert value[0]%18==0 and value[1]%3==0
for generator in [(1,-1),(0,3)]:
 value=action(C0,generator);assert value[0]%18==0 and value[1]%3==0
assert all(t%9==0 for t in product2(J0,J0))
assert tuple(t%9 for t in K0[:2])==(4,0)
assert action(J0,dv)[0]%9==6
assert F(2)<=F(dv[0],dv[1])<=F(5,2)
for ratio in [F(2),F(5,2)]:
 assert F(2)<=(22*ratio+18)/(5*ratio+18)<=F(5,2)
assert 7*F(5,2)**2-12*F(5,2)-36==-F(89,4)
out.update({'commutator_square_18I':True,'adjacent_swap_mass_lattice_inclusion':'18Z x 3Z','scalar_kernel_mod18_correction_checked':True,'high_ratio_interval_invariant':True})
last=[]
for word in ['KK','JK','JJ','KJ']:
 vector=action(product2(K0 if word[0]=='K' else J0,K0 if word[1]=='K' else J0),dv)
 assert sum(vector)%3==0;last.append((vector[0],sum(vector)//3))
minors=[last[i][0]*last[j][1]-last[j][0]*last[i][1] for i in range(4) for j in range(i+1,4)]
g=0
for a in minors:g=gcd(g,a)
assert g==1
out.update({'last_packet_columns':last,'last_packet_minors':minors,'last_packet_minors_gcd':g,'raw_word_sum_PF_less_than_44':1009<33**2,'high_packet_inverse_ratio_interval':['2','5/2'],'high_packet_determinant_bound':'abs(7r^2-12r-36)>=89/4 for 2<=r<=5/2','high_packet_uniform_capacity_ratio_less_than_one':31**2<2*28**2})
print(json.dumps(out,indent=2));Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2))
