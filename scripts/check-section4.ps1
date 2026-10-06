param(
  [string]$Target = 'Section4Audit.lean',
  [string]$PackageCache = 'C:/Users/lzysh/Documents/Codex/lean32/packages',
  [string]$LeanBin = 'C:/Users/lzysh/.elan/toolchains/leanprover--lean4---v4.32.1/bin',
  [switch]$Rebuild
)
$ErrorActionPreference = 'Stop'
$sectionRoot = Split-Path $PSScriptRoot -Parent
Set-Location $sectionRoot
. (Join-Path $PSScriptRoot 'section4-source-guard.ps1')
$sectionEnvironment = & (Join-Path $PSScriptRoot 'section4-environment.ps1') -PackageCache $PackageCache -LeanBin $LeanBin
$sectionManifest = Join-Path $sectionRoot 'docs/section4-build-results.json'
$sectionLogDirectory = Join-Path $sectionRoot 'docs/section4-build-logs'
New-Item -ItemType Directory -Path $sectionLogDirectory -Force | Out-Null
$sectionPrevious = @{}
foreach ($recordPath in @('work/section4-evidence-dependencies.json', 'docs/section4-build-results.json')) {
  $fullRecordPath = Join-Path $sectionRoot $recordPath
  if (Test-Path -LiteralPath $fullRecordPath) {
    foreach ($entry in (Get-Content -LiteralPath $fullRecordPath -Raw | ConvertFrom-Json)) {
      $sectionPrevious[$entry.module] = $entry
    }
  }
}
$sectionVisited = [System.Collections.Generic.HashSet[string]]::new()
$sectionOrder = [System.Collections.Generic.List[string]]::new()
function Add-SectionModule([string]$module) {
  if (-not $sectionVisited.Add($module)) { return }
  foreach ($dependency in Get-SectionProjectImports ([IO.File]::ReadAllText((Join-Path $sectionRoot $module))) $sectionRoot) {
    Add-SectionModule $dependency
  }
  $sectionOrder.Add($module)
}
Add-SectionModule $Target
$sectionFingerprints = @{}
$sectionResults = [System.Collections.Generic.List[object]]::new()
$sectionRebuiltCount = 0
$sectionKernelAudit = $null
$sectionAllowed = @('propext', 'Classical.choice', 'Quot.sound',
  'Universality.External.six_exponentials', 'Universality.External.gelfond_schneider_real')
foreach ($module in $sectionOrder) {
  $sourcePath = Join-Path $sectionRoot $module
  $sourceText = [IO.File]::ReadAllText($sourcePath)
  $sourceHash = (Get-FileHash -LiteralPath $sourcePath -Algorithm SHA256).Hash.ToLowerInvariant()
  Assert-SectionLeanSource $module $sourceText
  $dependencies = [System.Collections.Generic.List[string]]::new()
  foreach ($child in Get-SectionProjectImports $sourceText $sectionRoot) {
    $dependencies.Add($child + ':' + $sectionFingerprints[$child])
  }
  $fingerprintText = $module + ':' + $sourceHash + '|' + (($dependencies | Sort-Object) -join '|')
  $fingerprint = [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData([Text.Encoding]::UTF8.GetBytes($fingerprintText))).ToLowerInvariant()
  $sectionFingerprints[$module] = $fingerprint
  $objectPath = Join-Path $sectionRoot ('.lake/build/lib/lean/' + [IO.Path]::ChangeExtension($module, '.olean'))
  $previous = $sectionPrevious[$module]
  $reuse = ($module -ne $Target) -and -not $Rebuild -and $previous -and $previous.environment_fingerprint -eq $sectionEnvironment.sha256 -and $previous.source_sha256 -eq $sourceHash -and
    $previous.dependency_fingerprint -eq $fingerprint -and (Test-Path -LiteralPath $objectPath)
  if ($reuse) {
    $reuse = (Get-FileHash -LiteralPath $objectPath -Algorithm SHA256).Hash.ToLowerInvariant() -eq $previous.olean_sha256
    if ($previous.PSObject.Properties['exit_code'] -and $previous.exit_code -ne 0) { $reuse = $false }
  }
  if ($reuse) {
    $sectionResults.Add($previous)
  } else {
    Write-Host "Checking $module"
    $started = (Get-Date).ToUniversalTime()
    $output = @(& (Join-Path $PSScriptRoot 'check.ps1') -Module $module -PackageCache $PackageCache -LeanBin $LeanBin 2>&1)
    $exitCode = $LASTEXITCODE
    $logRelative = 'docs/section4-build-logs/' + $module.Replace('/', '_').Replace('.lean', '.log')
    [IO.File]::WriteAllText((Join-Path $sectionRoot $logRelative), ($output -join [Environment]::NewLine), [Text.UTF8Encoding]::new($false))
    if ($exitCode -ne 0) { $output | ForEach-Object { Write-Host $_ }; throw "Lean rejected $module" }
    if ((Get-FileHash -LiteralPath $sourcePath -Algorithm SHA256).Hash.ToLowerInvariant() -ne $sourceHash) { throw "Source changed during build: $module" }
    foreach ($audit in [regex]::Matches(($output -join "`n"), 'depends on axioms:\s*\[([^\]]*)\]')) {
      foreach ($axiom in ($audit.Groups[1].Value -split ',')) {
        if ($axiom.Trim() -notin $sectionAllowed) { throw "Unapproved axiom $axiom in $module" }
      }
    }
    if (($output -join "`n") -match 'sorryAx') { throw "Admitted proof detected: $module" }
    if ($module -eq $Target -and $sourceText -match '#audit_section4_axioms') {
      $kernelCheck = [regex]::Match(($output -join "`n"), 'SECTION4_KERNEL_AXIOM_AUDIT_OK declarations=(\d+) modules=(\d+)')
      if (-not $kernelCheck.Success -or [int]$kernelCheck.Groups[1].Value -eq 0) {
        throw 'The final all-project-declaration axiom audit did not report success'
      }
      $sectionKernelAudit = [ordered]@{declarations=[int]$kernelCheck.Groups[1].Value; modules=[int]$kernelCheck.Groups[2].Value}
    }
    $sectionResults.Add([pscustomobject]@{
      module=$module; exit_code=0; mode='rebuilt'; source_sha256=$sourceHash;
      environment_fingerprint=$sectionEnvironment.sha256;
      dependency_fingerprint=$fingerprint;
      olean_sha256=(Get-FileHash -LiteralPath $objectPath -Algorithm SHA256).Hash.ToLowerInvariant();
      started_at_utc=$started.ToString('o'); checked_at_utc=(Get-Date).ToUniversalTime().ToString('o'); log=$logRelative
    })
    $sectionRebuiltCount++
  }
  $sectionResults | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $sectionManifest -Encoding utf8
}
foreach ($record in $sectionResults) {
  $finalSource = Join-Path $sectionRoot $record.module
  $finalObject = Join-Path $sectionRoot ('.lake/build/lib/lean/' + [IO.Path]::ChangeExtension($record.module, '.olean'))
  if ((Get-FileHash -LiteralPath $finalSource -Algorithm SHA256).Hash.ToLowerInvariant() -ne $record.source_sha256 -or
      (Get-FileHash -LiteralPath $finalObject -Algorithm SHA256).Hash.ToLowerInvariant() -ne $record.olean_sha256) {
    throw "Source or object changed during closure verification: $($record.module)"
  }
}
$sectionEnvironmentAfter = & (Join-Path $PSScriptRoot 'section4-environment.ps1') -PackageCache $PackageCache -LeanBin $LeanBin
if ($sectionEnvironmentAfter.sha256 -ne $sectionEnvironment.sha256) { throw 'Build environment changed during verification' }
$sectionEnvironment | ConvertTo-Json -Depth 8 | Set-Content docs/section4-build-environment.json -Encoding utf8
[pscustomobject]@{
  target=$Target; module_count=$sectionOrder.Count; rebuilt_count=$sectionRebuiltCount;
  kernel_axiom_audit=$sectionKernelAudit;
  allowed_axioms=$sectionAllowed; lean_version=$sectionEnvironment.identity.lean_version;
  environment_fingerprint=$sectionEnvironment.sha256;
  mathlib_revision=(@($sectionEnvironment.identity.packages | Where-Object name -eq 'mathlib')[0].revision);
  completed_at_utc=(Get-Date).ToUniversalTime().ToString('o')
} | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath docs/section4-build-metadata.json -Encoding utf8
Write-Host "Verified $($sectionOrder.Count) project modules; rebuilt $sectionRebuiltCount."
