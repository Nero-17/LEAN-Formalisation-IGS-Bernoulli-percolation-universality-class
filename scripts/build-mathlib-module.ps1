param(
    [Parameter(Mandatory=$true)][string]$Module,
    [string]$PackageCache = 'C:/Users/lzysh/Documents/Codex/lean32/packages',
    [string]$LeanBin = 'C:/Users/lzysh/.elan/toolchains/leanprover--lean4---v4.32.1/bin'
)
$ErrorActionPreference = 'Stop'
if ($Module -notmatch '^Mathlib(?:\.[A-Za-z0-9_]+)+$') { throw 'Expected a Mathlib module name' }
$taskRoot = Split-Path $PSScriptRoot -Parent
$taskLibrary = Join-Path $PackageCache 'mathlib'
$taskRelative = $Module.Replace('.', '/')
$taskSource = Join-Path $taskLibrary ($taskRelative + '.lean')
$taskBuild = Join-Path $taskRoot '.lake/build/lib/lean'
$taskOutput = Join-Path (Join-Path $taskLibrary '.lake/build/lib/lean') ($taskRelative + '.olean')
New-Item -ItemType Directory -Path (Split-Path $taskOutput -Parent) -Force | Out-Null
$taskPaths = @($taskBuild) + @(Get-ChildItem -LiteralPath $PackageCache -Directory | ForEach-Object { Join-Path $_.FullName '.lake/build/lib/lean' })
$env:LEAN_PATH = $taskPaths -join ';'
$taskHash = (Get-FileHash -LiteralPath $taskSource -Algorithm SHA256).Hash.ToLowerInvariant()
& (Join-Path $LeanBin 'lean.exe') '-DautoImplicit=false' '-DmaxSynthPendingDepth=3' '--root' $taskLibrary.Replace('\', '/') '-o' $taskOutput $taskSource.Replace('\', '/')
$taskExit = $LASTEXITCODE
if ($taskExit -eq 0) {
    $taskRecord = [pscustomobject]@{
        module=$Module; source=$taskSource; source_sha256=$taskHash;
        output=$taskOutput; exit_code=$taskExit; checked_at_utc=(Get-Date).ToUniversalTime().ToString('o');
        mathlib_revision='520045ab14e26149ee970e2e617ca04b09bde5d6'
    }
    $taskRecord | ConvertTo-Json -Compress | Add-Content -LiteralPath (Join-Path $taskRoot 'docs/supplemental-mathlib-builds.jsonl') -Encoding utf8
}
exit $taskExit
