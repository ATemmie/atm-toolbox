$errs = $null
$tokens = $null
$null = [System.Management.Automation.Language.Parser]::ParseFile('C:\Users\Administrator\Desktop\传输\projects\atm-toolbox\go_usage_popup.ps1', [ref]$tokens, [ref]$errs)
if ($errs.Count -gt 0) {
    Write-Host ("语法错误数: " + $errs.Count)
    $errs | Select-Object -First 5 | ForEach-Object { Write-Host $_.Message }
} else {
    Write-Host '语法OK'
}