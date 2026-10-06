# Ignore nested Lean comments and string literals before checking declaration tokens.
if (-not ('Section4LeanSource' -as [type])) {
  Add-Type -TypeDefinition @"
using System.Text;
public static class Section4LeanSource {
  public static string Code(string source) {
    var result = new StringBuilder(source.Length);
    int depth = 0; bool line = false, text = false, escape = false;
    for (int i = 0; i < source.Length; i++) {
      char c = source[i]; char next = i + 1 < source.Length ? source[i + 1] : '\0';
      if (line) { if (c == '\n') line = false; result.Append(c == '\n' ? c : ' '); continue; }
      if (depth > 0) {
        if (c == '/' && next == '-') { depth++; result.Append("  "); i++; }
        else if (c == '-' && next == '/') { depth--; result.Append("  "); i++; }
        else result.Append(c == '\n' ? c : ' ');
        continue;
      }
      if (text) {
        if (escape) escape = false;
        else if (c == '\\') escape = true;
        else if (c == '"') text = false;
        result.Append(c == '\n' ? c : ' '); continue;
      }
      if (c == '-' && next == '-') { line = true; result.Append("  "); i++; }
      else if (c == '/' && next == '-') { depth = 1; result.Append("  "); i++; }
      else if (c == '"') { text = true; result.Append(' '); }
      else result.Append(c);
    }
    return result.ToString();
  }
}
"@
}
function Get-SectionProjectImports([string]$sourceText, [string]$root) {
  $code = [Section4LeanSource]::Code($sourceText)
  foreach ($import in [regex]::Matches($code, '(?m)^\s*(?:(?:public|private|meta)\s+)?import\s+([^\r\n]+)')) {
    foreach ($name in ($import.Groups[1].Value.Trim() -split '\s+')) {
      $relative = $name.Replace('.', '/') + '.lean'
      if (Test-Path -LiteralPath (Join-Path $root $relative)) { $relative }
    }
  }
}
function Assert-SectionLeanSource([string]$module, [string]$sourceText) {
  $code = [Section4LeanSource]::Code($sourceText)
  $declarationCode = [regex]::Replace($code, '(?m)^\s*#print\s+axioms\b', '')
  if ([regex]::IsMatch($declarationCode, '\b(sorry|admit|native_decide|sorryAx|axioms|constant|constants|opaque)\b|debug\.skipKernelTC')) {
    throw "Unapproved declaration or proof shortcut in $module"
  }
  foreach ($declaration in [regex]::Matches($code, '\baxiom\s+([A-Za-z0-9_\x27.]+)')) {
    $expected = @{
      'Universality/Arithmetic/SixExponentials.lean' = 'six_exponentials'
      'Universality/Arithmetic/GelfondSchneider.lean' = 'gelfond_schneider_real'
    }
    if ($expected[$module] -ne $declaration.Groups[1].Value) { throw "Unapproved axiom in $module" }
    if ([regex]::Matches($code, '\baxiom\s+').Count -ne 1 -or
        $code -notmatch ('namespace\s+Universality\.External\s+axiom\s+' + $expected[$module] + '\b')) {
      throw "Unexpected external axiom namespace or declaration count in $module"
    }
  }
}