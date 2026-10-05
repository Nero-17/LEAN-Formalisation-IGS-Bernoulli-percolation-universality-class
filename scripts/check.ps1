param(
    [string]$Module = 'Universality/Matrix/TwoByTwo.lean',
    [string]$PackageCache = 'C:/Users/lzysh/Documents/Codex/lean32/packages',
    [string]$LeanBin = 'C:/Users/lzysh/.elan/toolchains/leanprover--lean4---v4.32.1/bin'
)
$ErrorActionPreference = 'Stop'
$taskRoot = Split-Path $PSScriptRoot -Parent
Set-Location $taskRoot
$taskBuild = Join-Path $taskRoot '.lake/build/lib/lean'
New-Item -ItemType Directory -Path $taskBuild -Force | Out-Null
$taskPaths = @($taskBuild) + @(Get-ChildItem -LiteralPath $PackageCache -Directory | ForEach-Object { Join-Path $_.FullName '.lake/build/lib/lean' })
$env:LEAN_PATH = $taskPaths -join ';'
$taskOutput = Join-Path $taskBuild ([IO.Path]::ChangeExtension($Module, '.olean'))
New-Item -ItemType Directory -Path (Split-Path $taskOutput -Parent) -Force | Out-Null
& (Join-Path $LeanBin 'lean.exe') '-o' $taskOutput $Module
exit $LASTEXITCODE
