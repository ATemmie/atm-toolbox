$WshShell = New-Object -ComObject WScript.Shell
$desktop = [Environment]::GetFolderPath('Desktop')
$lnk = $WshShell.CreateShortcut("$desktop\📊 Go用量.lnk")
$lnk.TargetPath = 'powershell.exe'
$lnk.Arguments = '-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File "C:\Users\Administrator\Desktop\传输\projects\atm-toolbox\go_usage_popup.ps1"'
$lnk.WorkingDirectory = 'C:\Users\Administrator\Desktop\传输\projects\atm-toolbox'
$lnk.Description = '一键查看 OpenCode Go 用量'
# 设置快捷键 Ctrl+Alt+U
$lnk.Hotkey = 'Ctrl+Alt+U'
$lnk.Save()
Write-Host "快捷方式已创建: $desktop\📊 Go用量.lnk"
Write-Host "快捷键: Ctrl+Alt+U"

# 验证
$check = $WshShell.CreateShortcut("$desktop\📊 Go用量.lnk")
Write-Host "验证: Target=$($check.TargetPath) Args=$($check.Arguments) Hotkey=$($check.Hotkey)"