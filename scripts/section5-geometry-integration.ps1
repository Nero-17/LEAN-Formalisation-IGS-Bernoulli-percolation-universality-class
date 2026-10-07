param([switch]$Compile)
$ErrorActionPreference = 'Stop'
$taskRoot = Split-Path $PSScriptRoot -Parent
$taskUpstream = 'C:/Users/lzysh/Documents/Codex/2026-10-06/new-chat/work/universality-section4'
$taskReceiptPath = Join-Path $taskRoot 'docs/section5-geometry-integration-receipt.json'
$taskLogRoot = Join-Path $taskRoot 'docs/section5-geometry-integration-logs'

function Get-TaskHash([byte[]]$Bytes) {
    [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($Bytes)).ToLowerInvariant()
}

if (-not (Test-Path -LiteralPath $taskReceiptPath)) {
    $script:taskVisited = [Collections.Generic.HashSet[string]]::new()
    $script:taskOrder = [Collections.Generic.List[string]]::new()
    $script:taskSources = @{}
    function Visit-TaskModule([string]$Module) {
        if (-not $script:taskVisited.Add($Module)) { return }
        $taskRelative = $Module.Replace('.', '/') + '.lean'
        $taskPath = Join-Path $taskUpstream $taskRelative
        $taskBytes = [IO.File]::ReadAllBytes($taskPath)
        $taskText = [Text.Encoding]::UTF8.GetString($taskBytes)
        $script:taskSources[$Module] = $taskBytes
        foreach ($taskLine in ($taskText -split '\r?\n')) {
            if ($taskLine -match '^import\s+(Universality\.\S+)') {
                Visit-TaskModule $Matches[1]
            }
        }
        $script:taskOrder.Add($Module)
    }
    Visit-TaskModule 'Universality.Geometry.GenerationHausdorffDimension'

    $taskExisting = @()
    $taskMissing = @()
    foreach ($taskModule in $script:taskOrder) {
        $taskRelative = $taskModule.Replace('.', '/') + '.lean'
        $taskDestination = Join-Path $taskRoot $taskRelative
        $taskBytes = $script:taskSources[$taskModule]
        if (Test-Path -LiteralPath $taskDestination) {
            $taskFrozenText = [Text.Encoding]::UTF8.GetString($taskBytes).Replace([string][char]13, '')
            $taskExistingText = [IO.File]::ReadAllText($taskDestination).Replace([string][char]13, '')
            if ($taskFrozenText -ne $taskExistingText) { throw "Existing source conflict: $taskRelative" }
            $taskExisting += [ordered]@{
                module = $taskModule
                upstream_sha256 = Get-TaskHash $taskBytes
                local_sha256 = (Get-FileHash -LiteralPath $taskDestination).Hash.ToLowerInvariant()
                comparison = 'Identical after CRLF/LF normalization; existing file preserved'
            }
        } else {
            $taskMissing += $taskModule
        }
    }
    if ($taskMissing.Count -ne 25) { throw "Expected 25 missing modules; found $($taskMissing.Count). No source copied." }

    $taskCopies = @()
    foreach ($taskModule in $taskMissing) {
        $taskRelative = $taskModule.Replace('.', '/') + '.lean'
        $taskUpstreamPath = Join-Path $taskUpstream $taskRelative
        $taskDestination = Join-Path $taskRoot $taskRelative
        $taskBytes = $script:taskSources[$taskModule]
        $taskHash = Get-TaskHash $taskBytes
        if ((Get-FileHash -LiteralPath $taskUpstreamPath).Hash.ToLowerInvariant() -ne $taskHash) {
            throw "Upstream source changed during freeze: $taskRelative"
        }
        if (Test-Path -LiteralPath $taskDestination) { throw "Destination appeared during freeze: $taskRelative" }
        New-Item -ItemType Directory -Path (Split-Path $taskDestination -Parent) -Force | Out-Null
        [IO.File]::WriteAllBytes($taskDestination, $taskBytes)
        if ((Get-FileHash -LiteralPath $taskDestination).Hash.ToLowerInvariant() -ne $taskHash) {
            throw "Exact-byte copy verification failed: $taskRelative"
        }
        $taskCopies += [ordered]@{
            module = $taskModule
            relative_path = $taskRelative
            upstream_path = $taskUpstreamPath
            upstream_sha256 = $taskHash
            copied_sha256 = $taskHash
            copied_at_utc = [DateTime]::UtcNow.ToString('o')
        }
    }
    $taskReceipt = [ordered]@{
        root_module = 'Universality.Geometry.GenerationHausdorffDimension'
        upstream_root = $taskUpstream
        destination_root = $taskRoot
        freeze_completed_at_utc = [DateTime]::UtcNow.ToString('o')
        closure_count = $script:taskOrder.Count
        existing_identical = $taskExisting
        frozen_modules_in_dependency_order = $taskCopies
        builds = @()
        status = 'frozen_not_compiled'
    }
    $taskReceipt | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $taskReceiptPath -Encoding utf8
    Write-Output "Frozen $($taskCopies.Count) exact-byte modules; $($taskExisting.Count) existing sources preserved."
}

if ($Compile) {
    $taskReceipt = Get-Content -LiteralPath $taskReceiptPath -Raw | ConvertFrom-Json -AsHashtable
    $taskRebuilt = $false
    New-Item -ItemType Directory -Path $taskLogRoot -Force | Out-Null
    foreach ($taskBaseline in $taskReceipt.existing_identical) {
        $taskBaselinePath = Join-Path $taskRoot ($taskBaseline.module.Replace('.', '/') + '.lean')
        if ((Get-FileHash -LiteralPath $taskBaselinePath).Hash.ToLowerInvariant() -ne $taskBaseline.local_sha256) {
            throw "Previously checked baseline source changed: $($taskBaseline.module)"
        }
    }
    foreach ($taskCopy in $taskReceipt.frozen_modules_in_dependency_order) {
        $taskSourcePath = Join-Path $taskRoot $taskCopy.relative_path
        $taskCurrentHash = (Get-FileHash -LiteralPath $taskSourcePath).Hash.ToLowerInvariant()
        if ($taskCurrentHash -ne $taskCopy.copied_sha256) { throw "Frozen source changed: $($taskCopy.relative_path)" }
        $taskSuccess = @($taskReceipt.builds | Where-Object {
            $_.module -eq $taskCopy.module -and $_.exit_code -eq 0 -and $_.source_sha256 -eq $taskCurrentHash
        })
        $taskObjectPath = Join-Path $taskRoot ('.lake/build/lib/lean/' + $taskCopy.module.Replace('.', '/') + '.olean')
        if ($taskSuccess.Count -gt 0 -and (Test-Path -LiteralPath $taskObjectPath)) {
            $taskObjectHash = (Get-FileHash -LiteralPath $taskObjectPath).Hash.ToLowerInvariant()
            if ($taskSuccess[-1].olean_sha256 -eq $taskObjectHash) { continue }
        }
        $taskLogPath = Join-Path $taskLogRoot ($taskCopy.module.Replace('.', '_') + '.log')
        $taskStarted = [DateTime]::UtcNow.ToString('o')
        Write-Output "Compiling $($taskCopy.module)"
        $taskRebuilt = $true
        & (Join-Path $PSScriptRoot 'check.ps1') -Module $taskCopy.relative_path -Threads 1 *> $taskLogPath
        $taskExit = $LASTEXITCODE
        $taskBuild = [ordered]@{
            module = $taskCopy.module
            source_sha256 = $taskCurrentHash
            started_at_utc = $taskStarted
            finished_at_utc = [DateTime]::UtcNow.ToString('o')
            exit_code = $taskExit
            command = "./scripts/check.ps1 -Module $($taskCopy.relative_path) -Threads 1"
            log = $taskLogPath
        }
        if ($taskExit -eq 0) {
            $taskBuild.olean_sha256 = (Get-FileHash -LiteralPath $taskObjectPath).Hash.ToLowerInvariant()
        }
        $taskReceipt.builds += $taskBuild
        $taskReceipt.status = if ($taskExit -eq 0) { 'compiling' } else { 'compile_failed' }
        $taskReceipt | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $taskReceiptPath -Encoding utf8
        Write-Output "Exit $taskExit : $($taskCopy.module)"
        if ($taskExit -ne 0) { Get-Content -LiteralPath $taskLogPath; exit $taskExit }
    }
    $taskReceipt.status = 'all_frozen_modules_compiled'
    if ($taskRebuilt) { $taskReceipt.compilation_completed_at_utc = [DateTime]::UtcNow.ToString('o') }
    $taskReceipt.verification_completed_at_utc = [DateTime]::UtcNow.ToString('o')
    $taskReceipt | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $taskReceiptPath -Encoding utf8
    Write-Output 'All 25 frozen geometry modules compiled successfully.'
}
