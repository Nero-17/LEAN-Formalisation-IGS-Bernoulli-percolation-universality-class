param([switch]$Compile)
$ErrorActionPreference = 'Stop'
$taskRoot = Split-Path $PSScriptRoot -Parent
$taskUpstream = 'C:/Users/lzysh/Documents/Codex/2026-09-13/new-chat/work/universality-lean'
$taskReceiptPath = Join-Path $taskRoot 'docs/section5-physical-integration-receipt.json'
$taskLogRoot = Join-Path $taskRoot 'docs/section5-physical-integration-logs'
$taskSnapshotRoot = Join-Path $taskRoot 'docs/section5-physical-upstream-snapshot'

function Get-TaskHash([byte[]]$Bytes) {
    [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($Bytes)).ToLowerInvariant()
}

if (-not (Test-Path -LiteralPath $taskReceiptPath)) {
    $taskInspection = Get-Content -LiteralPath (Join-Path $taskRoot 'docs/section5-upstream-physical-inspection.json') -Raw | ConvertFrom-Json
    $taskAuditBytes = [IO.File]::ReadAllBytes((Join-Path $taskUpstream 'docs/source-audit.json'))
    $taskBuildBytes = [IO.File]::ReadAllBytes((Join-Path $taskUpstream 'docs/build-results.json'))
    $taskMetadataBytes = [IO.File]::ReadAllBytes((Join-Path $taskUpstream 'docs/build-metadata.json'))
    if ((Get-TaskHash $taskAuditBytes) -ne $taskInspection.source_audit_sha256 -or
        (Get-TaskHash $taskBuildBytes) -ne $taskInspection.build_results_sha256) {
        throw 'Upstream verification snapshot changed since the read-only inspection. No source copied.'
    }
    $taskAudit = [Text.Encoding]::UTF8.GetString($taskAuditBytes).TrimStart([char]0xfeff) | ConvertFrom-Json
    $taskBuilds = [Text.Encoding]::UTF8.GetString($taskBuildBytes).TrimStart([char]0xfeff) | ConvertFrom-Json
    $taskMetadata = [Text.Encoding]::UTF8.GetString($taskMetadataBytes).TrimStart([char]0xfeff) | ConvertFrom-Json
    if (-not $taskAudit.ok -or $taskAudit.module_count -ne 752 -or
        $taskAudit.errors.Count -ne 0 -or $taskAudit.kernel_axioms.Count -ne 3 -or
        $taskAudit.kernel_axioms -notcontains 'Classical.choice' -or
        $taskAudit.kernel_axioms -notcontains 'Quot.sound' -or
        $taskAudit.kernel_axioms -notcontains 'propext') {
        throw 'The inspected source audit is not the expected successful standard-axiom snapshot.'
    }
    $taskAuditMap = @{}
    foreach ($taskSource in $taskAudit.sources) { $taskAuditMap[$taskSource.module] = $taskSource }
    $taskBuildMap = @{}
    foreach ($taskBuild in $taskBuilds) { $taskBuildMap[$taskBuild.module] = $taskBuild }
    $script:taskVisited = [Collections.Generic.HashSet[string]]::new()
    $script:taskOrder = [Collections.Generic.List[string]]::new()
    $script:taskSources = @{}
    function Visit-TaskModule([string]$Module) {
        if (-not $script:taskVisited.Add($Module)) { return }
        $taskRelative = $Module.Replace('.', '/') + '.lean'
        $taskPath = Join-Path $taskUpstream $taskRelative
        $taskBytes = [IO.File]::ReadAllBytes($taskPath)
        $taskHash = Get-TaskHash $taskBytes
        if (-not $taskAuditMap.ContainsKey($taskRelative) -or
            $taskAuditMap[$taskRelative].source_sha256 -ne $taskHash -or
            -not $taskBuildMap.ContainsKey($taskRelative) -or
            $taskBuildMap[$taskRelative].exit_code -ne 0 -or
            $taskBuildMap[$taskRelative].source_sha256 -ne $taskHash) {
            throw "Source is absent or mismatched in the verified snapshot: $taskRelative"
        }
        $taskText = [Text.Encoding]::UTF8.GetString($taskBytes)
        if ($taskText -match '(?m)^\s*(axiom|unsafe\s|sorry\b)' -or
            $taskText -match '\b(native_decide|sorryAx)\b') {
            throw "Forbidden declaration or proof shortcut requires inspection: $taskRelative"
        }
        $script:taskSources[$Module] = $taskBytes
        foreach ($taskLine in ($taskText -split '\r?\n')) {
            if ($taskLine -match '^import\s+(Universality\.\S+)') { Visit-TaskModule $Matches[1] }
        }
        $script:taskOrder.Add($Module)
    }
    Visit-TaskModule 'Universality.Percolation.PhysicalExponentClass'
    $taskExisting = @()
    $taskMissing = @()
    foreach ($taskModule in $script:taskOrder) {
        $taskRelative = $taskModule.Replace('.', '/') + '.lean'
        $taskDestination = Join-Path $taskRoot $taskRelative
        $taskBytes = $script:taskSources[$taskModule]
        if (Test-Path -LiteralPath $taskDestination) {
            $taskFrozenText = [Text.Encoding]::UTF8.GetString($taskBytes).Replace([string][char]13, '')
            $taskExistingText = [IO.File]::ReadAllText($taskDestination).Replace([string][char]13, '')
            if ($taskFrozenText -ne $taskExistingText) { throw "Existing substantive source conflict: $taskRelative" }
            $taskObjectPath = Join-Path $taskRoot ('.lake/build/lib/lean/' + $taskModule.Replace('.', '/') + '.olean')
            if (-not (Test-Path -LiteralPath $taskObjectPath)) { throw "Existing dependency has no local object: $taskRelative" }
            $taskExisting += [ordered]@{
                module = $taskModule
                upstream_sha256 = Get-TaskHash $taskBytes
                local_sha256 = (Get-FileHash -LiteralPath $taskDestination).Hash.ToLowerInvariant()
                local_olean_sha256 = (Get-FileHash -LiteralPath $taskObjectPath).Hash.ToLowerInvariant()
                snapshot_checked_at_utc = $taskBuildMap[$taskRelative].checked_at_utc
                comparison = 'Identical after CRLF/LF normalization; existing file preserved'
            }
        } else { $taskMissing += $taskModule }
    }
    if ($taskMissing.Count -ne 112 -or $script:taskOrder.Count -ne 403) {
        throw "Expected 112 missing among 403 modules; found $($taskMissing.Count) among $($script:taskOrder.Count). No source copied."
    }
    New-Item -ItemType Directory -Path $taskSnapshotRoot -Force | Out-Null
    [IO.File]::WriteAllBytes((Join-Path $taskSnapshotRoot 'source-audit.json'), $taskAuditBytes)
    [IO.File]::WriteAllBytes((Join-Path $taskSnapshotRoot 'build-results.json'), $taskBuildBytes)
    [IO.File]::WriteAllBytes((Join-Path $taskSnapshotRoot 'build-metadata.json'), $taskMetadataBytes)
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
            snapshot_checked_at_utc = $taskBuildMap[$taskRelative].checked_at_utc
            copied_at_utc = [DateTime]::UtcNow.ToString('o')
        }
    }
    $taskReceipt = [ordered]@{
        root_module = 'Universality.Percolation.PhysicalExponentClass'
        upstream_root = $taskUpstream
        destination_root = $taskRoot
        snapshot_source_audit_sha256 = Get-TaskHash $taskAuditBytes
        snapshot_build_results_sha256 = Get-TaskHash $taskBuildBytes
        snapshot_build_metadata_sha256 = Get-TaskHash $taskMetadataBytes
        snapshot_metadata = $taskMetadata
        snapshot_kernel_axioms = $taskAudit.kernel_axioms
        freeze_completed_at_utc = [DateTime]::UtcNow.ToString('o')
        closure_count = $script:taskOrder.Count
        existing_identical = $taskExisting
        frozen_modules_in_dependency_order = $taskCopies
        builds = @()
        status = 'frozen_not_compiled'
    }
    $taskReceipt | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $taskReceiptPath -Encoding utf8
    Write-Output "Frozen $($taskCopies.Count) verified exact-byte modules; $($taskExisting.Count) existing sources preserved."
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
    Write-Output 'All 112 frozen physical-exponent modules compiled successfully.'
}
