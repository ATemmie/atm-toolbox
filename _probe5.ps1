"===== ComfyUI Desktop config locations ====="
$paths = @(
    "$env:APPDATA\ComfyUI",
    "$env:USERPROFILE\.comfyui",
    "$env:LOCALAPPDATA\ComfyUI",
    "$env:APPDATA\Comfy-Portal",
    "D:\Comfy-Desktop\ComfyUI-Desktop"
)
foreach($p in $paths){ if(Test-Path $p){ "[EXISTS] $p"; Get-ChildItem $p -ErrorAction SilentlyContinue | Select-Object -First 20 Name | Out-String -Width 150 } }
"===== find config.json / settings ====="
Get-ChildItem "D:\Comfy-Desktop" -Recurse -Depth 3 -Include "config.json","settings.json","*.yaml","*.yml" -ErrorAction SilentlyContinue | Where-Object {$_.FullName -notlike "*models*"} | Select-Object -First 20 FullName | Out-String -Width 250
"===== running Comfy processes ====="
Get-Process -Name "*comfy*","*python*","*node*" -ErrorAction SilentlyContinue | Select-Object Id,ProcessName,Path,StartTime | Format-Table -AutoSize | Out-String -Width 250
"===== listening ports (8188 etc) ====="
netstat -ano 2>&1 | Select-String "8188|8189|127.0.0.1:8000|LISTENING" | Select-Object -First 20 | Out-String