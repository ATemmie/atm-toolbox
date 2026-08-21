# Check ComfyUI server logs for the 500 error
$logDir = "D:\Comfy-Desktop\ComfyUI-Installs\Krea-2-Turbo\ComfyUI\logs"
if(Test-Path $logDir){
    Get-ChildItem $logDir | Sort-Object LastWriteTime -Descending | Select-Object -First 1 | ForEach-Object {
        "=== LATEST LOG: $($_.Name) ==="
        Get-Content $_.FullName -Tail 50
    }
}
# Also check ComfyUI Desktop log locations
$desktopLog = "$env:APPDATA\Comfy Desktop\logs"
if(Test-Path $desktopLog){
    Get-ChildItem $desktopLog -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 1 | ForEach-Object {
        "=== DESKTOP LOG: $($_.Name) ==="
        Get-Content $_.FullName -Tail 30
    }
}
# Try to get ComfyUI console output via the running process
"=== python stderr via process list ==="
Get-Process python -ErrorAction SilentlyContinue | Where-Object {$_.Path -like "*Krea*"} | Select-Object Id,ProcessName,Path | Format-Table -AutoSize | Out-String