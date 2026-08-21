"===== D:\Comfy-Desktop tree (top) ====="
Get-ChildItem "D:\Comfy-Desktop" -ErrorAction SilentlyContinue | Select-Object Name,Length,Mode | Format-Table -AutoSize | Out-String -Width 200
"===== find main.py / ComfyUI subdir ====="
Get-ChildItem "D:\Comfy-Desktop" -Recurse -Depth 2 -Filter "main.py" -ErrorAction SilentlyContinue | Select-Object FullName | Out-String -Width 250
"===== models dir ====="
Get-ChildItem "D:\Comfy-Desktop" -Recurse -Depth 3 -Directory -ErrorAction SilentlyContinue | Where-Object {$_.Name -in @("models","diffusion_models","text_encoders","vae","loras","checkpoints")} | Select-Object FullName | Out-String -Width 250
"===== version ====="
$ver = Get-ChildItem "D:\Comfy-Desktop" -Filter "*.txt" -ErrorAction SilentlyContinue
Get-ChildItem "D:\Comfy-Desktop" -Recurse -Depth 3 -Filter "version*.txt" -ErrorAction SilentlyContinue | ForEach-Object { $_.FullName; Get-Content $_.FullName -TotalCount 3 }
"===== ComfyUI Desktop data dir ====="
Get-ChildItem "$env:APPDATA\ComfyUI" -ErrorAction SilentlyContinue | Select-Object FullName | Out-String -Width 200
Get-ChildItem "$env:USERPROFILE\.comfyui" -ErrorAction SilentlyContinue | Select-Object FullName | Out-String -Width 200