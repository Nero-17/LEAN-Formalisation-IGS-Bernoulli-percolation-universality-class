"""Verify the explicit transcendental-dimension rule, using integer arithmetic."""
from pathlib import Path
from math import gcd
import json
from verify import verify
root=Path(__file__).resolve().parent
result=verify(root/'transcendental',19,424,scale_offset=480)
assert gcd(19,19**100+480)==1
result['scale_offset']=480
result['scale']=str(19**100+480)
result['coprime_to_19']=True
(root/'transcendental-verification.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
