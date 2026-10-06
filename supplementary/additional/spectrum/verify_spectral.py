"""Exact, standard-library check of the short spectral perturbation proof."""
if not __debug__: raise RuntimeError('Run without -O or -OO.')
from pathlib import Path
from fractions import Fraction as F
import json,sys
sys.set_int_max_str_digits(0)
ROOT=Path(__file__).resolve().parent
def mm(A,B): return [[sum(A[i][k]*B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
def add(A,B):return [[A[i][j]+B[i][j] for j in range(2)] for i in range(2)]
def scale(a,A):return [[a*x for x in row] for row in A]
def tr(A):return A[0][0]+A[1][1]
def det(A):return A[0][0]*A[1][1]-A[0][1]*A[1][0]
K=[[22,18],[5,18]];J=[[9,12],[3,6]];D=[[37,48],[13,26]]
H=[[0,0],[0,0]]
changes=[-17413779,169010230,-155094721,3498270]
assert sum(changes)==0
for tail,change in zip(['1100','1010','1001','0110'],changes):
    A=[[1,0],[0,1]]
    for letter in tail:A=mm(A,K if letter=='0' else J)
    H=add(H,scale(change,mm(A,D)))
assert H==[[304626366720,-728454355200],[119886741000,-286685685000]]
assert all(row[0]*55+row[1]*23==0 for row in H)
assert H==[[13244624640*23,-13244624640*55],[5212467000*23,-5212467000*55]]
row=[23,-55]
for _ in range(5):row=[sum(row[i]*K[i][j] for i in range(2)) for j in range(2)]
assert row==[-4444644,-17343936]
base=json.loads((ROOT.parents[1]/'section5/certificates/n424/word_base.json').read_text())
a=base['floor_groups'][339][0]
assert min(a,2**339-a-1)>=max(map(abs,changes))
# Also verify the small independent witness in Section 3.
A=scale(F(1,16),add(scale(2,K),J))
B=scale(F(1,16),add(add(mm(K,A),K),J))
assert B==scale(F(1,256),[[1896,2292],[627,1380]])
ABAB=mm(mm(A,B),mm(A,B));AABB=mm(mm(A,A),mm(B,B))
assert det(ABAB)==det(AABB)>0
assert tr(AABB)-tr(ABAB)==F(-1521,4194304)
result={'spectral_perturbation':'PASS','allocation_capacity':'PASS','trace_sign':'strictly negative','noncommuting_witness':'PASS','trace_difference':'-1521/4194304'}
(ROOT/'spectral-verification.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result))
