from pathlib import Path
p=Path('scratch/AffineCriticalCorrections.lean');t=p.read_text(encoding='utf-8-sig');t=t.replace('  nlinarith [mul_nonneg hcorrection (Real.rpow_nonneg hdistance power)]','  have hidentityScaled := congrArg (fun x : ℝ => x * distance ^ power) hidentity\n  nlinarith [mul_nonneg hcorrection (Real.rpow_nonneg hdistance power)]')
t=t.replace('  have hcomparison : -(rate / (expansion - 1)) * nextDistance ≤','  have hidentityScaled := congrArg (fun x : ℝ => x * distance) hidentity\n  have hcomparison : -(rate / (expansion - 1)) * nextDistance ≤')
p.write_text(t,encoding='utf-8')
