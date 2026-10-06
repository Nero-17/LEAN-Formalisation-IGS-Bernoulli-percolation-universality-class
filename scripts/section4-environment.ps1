param(
  [string]$PackageCache = 'C:/Users/lzysh/Documents/Codex/lean32/packages',
  [string]$LeanBin = 'C:/Users/lzysh/.elan/toolchains/leanprover--lean4---v4.32.1/bin'
)
$ErrorActionPreference = 'Stop'
$sectionEnvironmentRoot = Split-Path $PSScriptRoot -Parent
$sectionLeanExecutable = (Resolve-Path -LiteralPath (Join-Path $LeanBin 'lean.exe')).Path
$sectionPinnedManifest = Get-Content -LiteralPath (Join-Path $sectionEnvironmentRoot 'lake-manifest.json') -Raw | ConvertFrom-Json
$sectionPackageRecords = @()
foreach ($sectionPackage in ($sectionPinnedManifest.packages | Sort-Object name)) {
  $sectionPackagePath = (Resolve-Path -LiteralPath (Join-Path $PackageCache $sectionPackage.name)).Path
  $sectionPackageRevision = (& git -c "safe.directory=$sectionPackagePath" -C $sectionPackagePath rev-parse HEAD).Trim()
  if ($LASTEXITCODE -ne 0 -or $sectionPackageRevision -ne $sectionPackage.rev) {
    throw "Pinned revision mismatch: $($sectionPackage.name)"
  }
  & git -c "safe.directory=$sectionPackagePath" -C $sectionPackagePath diff --quiet HEAD --
  if ($LASTEXITCODE -ne 0) { throw "Tracked dependency sources changed: $($sectionPackage.name)" }
  $sectionPackageRecords += [ordered]@{name=$sectionPackage.name; path=$sectionPackagePath; revision=$sectionPackageRevision}
}
$sectionEnvironmentIdentity = [ordered]@{
  lean_executable=$sectionLeanExecutable;
  lean_sha256=(Get-FileHash -LiteralPath $sectionLeanExecutable -Algorithm SHA256).Hash.ToLowerInvariant();
  lean_version=(& $sectionLeanExecutable '--version');
  lean_toolchain_sha256=(Get-FileHash -LiteralPath (Join-Path $sectionEnvironmentRoot 'lean-toolchain') -Algorithm SHA256).Hash.ToLowerInvariant();
  lake_manifest_sha256=(Get-FileHash -LiteralPath (Join-Path $sectionEnvironmentRoot 'lake-manifest.json') -Algorithm SHA256).Hash.ToLowerInvariant();
  packages=$sectionPackageRecords
}
$sectionEnvironmentJson = $sectionEnvironmentIdentity | ConvertTo-Json -Depth 6 -Compress
$sectionEnvironmentHash = [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData([Text.Encoding]::UTF8.GetBytes($sectionEnvironmentJson))).ToLowerInvariant()
[pscustomobject]@{sha256=$sectionEnvironmentHash; identity=$sectionEnvironmentIdentity}