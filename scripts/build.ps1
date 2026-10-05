param(
    [string]$Target = 'Audit.lean',
    [string]$PackageCache = 'C:/Users/lzysh/Documents/Codex/lean32/packages',
    [string]$LeanBin = 'C:/Users/lzysh/.elan/toolchains/leanprover--lean4---v4.32.1/bin'
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
$taskResults = @()
foreach ($module in $taskOrder) {
    $taskStarted = Get-Date
    Write-Output "Checking $module"
    & (Join-Path $PSScriptRoot 'check.ps1') -Module $module -PackageCache $PackageCache -LeanBin $LeanBin
    $taskExitCode = $LASTEXITCODE
    $taskSeconds = ((Get-Date) - $taskStarted).TotalSeconds
    $taskResults += [pscustomobject]@{module=$module; exit_code=$taskExitCode; seconds=$taskSeconds}
    if ($taskExitCode -ne 0) { throw "Lean rejected $module with exit code $taskExitCode" }
}
$taskResults | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $taskRoot 'docs/build-results.json') -Encoding utf8
Write-Output "Verified $($taskOrder.Count) project modules."
