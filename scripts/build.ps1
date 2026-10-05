param(
    [string]$Target = 'Audit.lean',
    [string]$PackageCache = 'C:/Users/lzysh/Documents/Codex/lean32/packages',
    [string]$LeanBin = 'C:/Users/lzysh/.elan/toolchains/leanprover--lean4---v4.32.1/bin',
    [switch]$ReuseVerified
)
$ErrorActionPreference = 'Stop'
$taskRoot = Split-Path $PSScriptRoot -Parent
Set-Location $taskRoot
$taskVisited = [System.Collections.Generic.HashSet[string]]::new()
$taskOrder = [System.Collections.Generic.List[string]]::new()
function Add-TaskModule([string]$module) {
    if (-not $taskVisited.Add($module)) { return }
    foreach ($line in Get-Content -LiteralPath (Join-Path $taskRoot $module)) {
        if ($line -match '^import (Universality(?:\.[A-Za-z0-9_]+)*)\s*$') {
            Add-TaskModule ($Matches[1].Replace('.', '/') + '.lean')
        }
    }
    $taskOrder.Add($module)
}
Add-TaskModule $Target
$taskPrevious = @{}
$taskManifest = Join-Path $taskRoot 'docs/build-results.json'
if ($ReuseVerified -and (Test-Path -LiteralPath $taskManifest)) {
    foreach ($taskEntry in (Get-Content -LiteralPath $taskManifest -Raw | ConvertFrom-Json)) {
        $taskPrevious[$taskEntry.module] = $taskEntry
    }
}
$taskRebuilt = [System.Collections.Generic.HashSet[string]]::new()
$taskResults = @()
foreach ($module in $taskOrder) {
    $taskHash = (Get-FileHash -LiteralPath (Join-Path $taskRoot $module) -Algorithm SHA256).Hash.ToLowerInvariant()
    $taskDependencyRebuilt = $false
    foreach ($line in Get-Content -LiteralPath (Join-Path $taskRoot $module)) {
        if ($line -match '^import (Universality(?:\.[A-Za-z0-9_]+)*)\s*$') {
            if ($taskRebuilt.Contains($Matches[1].Replace('.', '/') + '.lean')) { $taskDependencyRebuilt = $true }
        }
    }
    $taskObject = Join-Path $taskRoot ('.lake/build/lib/lean/' + [IO.Path]::ChangeExtension($module, '.olean'))
    $taskPrior = $taskPrevious[$module]
    if ($ReuseVerified -and $taskPrior -and $taskPrior.exit_code -eq 0 -and
        $taskPrior.source_sha256 -eq $taskHash -and -not $taskDependencyRebuilt -and
        (Test-Path -LiteralPath $taskObject)) {
        Write-Output "Reusing verified $module"
        $taskResults += $taskPrior
        continue
    }
    $taskStarted = Get-Date
    Write-Output "Checking $module"
    & (Join-Path $PSScriptRoot 'check.ps1') -Module $module -PackageCache $PackageCache -LeanBin $LeanBin
    $taskExitCode = $LASTEXITCODE
    $taskSeconds = ((Get-Date) - $taskStarted).TotalSeconds
    $taskResults += [pscustomobject]@{module=$module; exit_code=$taskExitCode; seconds=$taskSeconds; source_sha256=$taskHash; checked_at_utc=(Get-Date).ToUniversalTime().ToString('o')}
    if ($taskExitCode -ne 0) { throw "Lean rejected $module with exit code $taskExitCode" }
    [void]$taskRebuilt.Add($module)
}
$taskResults | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $taskRoot 'docs/build-results.json') -Encoding utf8
[pscustomobject]@{
    target=$Target; module_count=$taskOrder.Count; rebuilt_count=$taskRebuilt.Count;
    reuse_verified=[bool]$ReuseVerified; lean_version=(& (Join-Path $LeanBin 'lean.exe') '--version');
    mathlib_revision='520045ab14e26149ee970e2e617ca04b09bde5d6';
    completed_at_utc=(Get-Date).ToUniversalTime().ToString('o')
} | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $taskRoot 'docs/build-metadata.json') -Encoding utf8
Write-Output "Verified $($taskOrder.Count) project modules; rebuilt $($taskRebuilt.Count)."
