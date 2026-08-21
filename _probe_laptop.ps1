"===== SYSTEM ====="
$cs = Get-CimInstance Win32_ComputerSystem
"Model: $($cs.Manufacturer) $($cs.Model)"
"RAM_GB: $([math]::Round($cs.TotalPhysicalMemory/1GB,0))"
"===== GPU ====="
$gpu = Get-CimInstance Win32_VideoController
foreach($g in $gpu){ "GPU: $($g.Name) | Driver: $($g.DriverVersion)" }
"===== NVIDIA-SMI ====="
$nv = "C:\Windows\System32\nvidia-smi.exe"
if(Test-Path $nv){ & $nv } else { "nvidia-smi not in System32" }
"===== COMFYUI SEARCH ====="
$candidates = @(
    "$env:USERPROFILE\Documents\comfy\ComfyUI",
    "C:\ComfyUI",
    "$env:USERPROFILE\ComfyUI",
    "C:\Users\ATemmie\Documents\ComfyUI",
    "C:\Users\ATemmie\Desktop\ComfyUI"
)
foreach($c in $candidates){ if(Test-Path $c){ "FOUND: $c" } }
"--- ComfyUI Desktop app dir ---"
Get-ChildItem "$env:LOCALAPPDATA\Programs" -Directory -ErrorAction SilentlyContinue | Where-Object {$_.Name -like "*Comfy*"} | ForEach-Object { $_.FullName }
Get-ChildItem "$env:APPDATA\ComfyUI" -Directory -ErrorAction SilentlyContinue | ForEach-Object { $_.FullName }
"--- search drives ---"
Get-PSDrive -PSProvider FileSystem | Where-Object {$_.Used -ne $null} | ForEach-Object {
    $root = $_.Root
    Get-ChildItem $root -Directory -ErrorAction SilentlyContinue | Where-Object {$_.Name -match "Comfy|Stable" } | ForEach-Object { $_.FullName }
}