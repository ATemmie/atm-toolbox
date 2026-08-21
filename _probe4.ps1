"===== extra_model_paths files ====="
Get-ChildItem "D:\Comfy-Desktop" -Recurse -Depth 4 -Filter "extra_model_paths*" -ErrorAction SilentlyContinue | ForEach-Object { $_.FullName; Get-Content $_.FullName }
"===== ComfyUI (1) version ====="
$c1 = "D:\Comfy-Desktop\ComfyUI-Installs\ComfyUI (1)\ComfyUI"
if(Test-Path "$c1\.git"){
    Push-Location $c1
    git log -1 --oneline 2>&1 | Out-String
    git describe --tags 2>&1 | Out-String
    Pop-Location
}
"===== main.py exists? ====="
Test-Path "$c1\main.py"
"===== Krea install main.py? ====="
Test-Path "D:\Comfy-Desktop\ComfyUI-Installs\Krea-2-Turbo\ComfyUI\main.py"
"===== custom_nodes in ComfyUI (1) ====="
Get-ChildItem "$c1\custom_nodes" -Directory -ErrorAction SilentlyContinue | Select-Object Name | Out-String -Width 200
"===== custom_nodes in Krea install ====="
Get-ChildItem "D:\Comfy-Desktop\ComfyUI-Installs\Krea-2-Turbo\ComfyUI\custom_nodes" -Directory -ErrorAction SilentlyContinue | Select-Object Name | Out-String -Width 200
"===== ComfyUI Desktop main app version ====="
$app = "D:\Comfy-Desktop"
Get-ChildItem $app -Recurse -Depth 3 -Filter "package.json" -ErrorAction SilentlyContinue | Where-Object {$_.FullName -like "*Desktop*"} | Select-Object -First 5 FullName | Out-String -Width 250
Get-ChildItem $app -Filter "*.exe" -Recurse -Depth 2 -ErrorAction SilentlyContinue | Select-Object -First 10 FullName | Out-String -Width 250