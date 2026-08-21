# Check available CLIP loaders and see if template exists
$cli1 = & "C:\Windows\System32\curl.exe" -s "http://127.0.0.1:8188/object_info/CLIPLoader" 2>&1
"=== CLIPLoader ==="
$cli1 | Select-String -Pattern "type|clip_name" | ForEach-Object { $_.Line } | Select-Object -First 5
""
$cli2 = & "C:\Windows\System32\curl.exe" -s "http://127.0.0.1:8188/object_info/QuadrupleCLIPLoader" 2>&1
"=== QuadrupleCLIPLoader ==="
$cli2 | Select-String -Pattern "type|clip_name" | ForEach-Object { $_.Line } | Select-Object -First 5

# Check if templates exist on game laptop
"=== Templates dir ==="
Get-ChildItem "D:\Comfy-Desktop\ComfyUI-Installs\Krea-2-Turbo\ComfyUI\templates" -ErrorAction SilentlyContinue | Select-Object -First 20 Name
Get-ChildItem "C:\Users\ATemmie\AppData\Roaming\Comfy Desktop" -Recurse -ErrorAction SilentlyContinue -Filter "*krea*" | Select-Object FullName