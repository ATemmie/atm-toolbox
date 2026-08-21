# Check ComfyUI Desktop workflow storage locations
$candidates = @(
    "C:\Users\ATemmie\ComfyUI",
    "C:\Users\ATemmie\Documents\ComfyUI",
    "$env:APPDATA\ComfyUI",
    "D:\Comfy-Desktop\ComfyUI-Installs\Krea-2-Turbo\ComfyUI\user",
    "D:\Comfy-Desktop\ComfyUI-Installs\ComfyUI (1)\ComfyUI\user"
)
"=== Checking workflow dirs ==="
foreach($c in $candidates){
    if(Test-Path $c){
        "[EXISTS] $c"
        Get-ChildItem $c -Recurse -Depth 2 -Directory -ErrorAction SilentlyContinue | Where-Object {$_.Name -match "workflow|template"} | ForEach-Object { "  DIR: $($_.FullName)" }
    }
}
"=== ComfyUI user default ==="
$userDir = "D:\Comfy-Desktop\ComfyUI-Installs\Krea-2-Turbo\ComfyUI\user\default"
if(Test-Path $userDir){
    "[EXISTS] $userDir"
    Get-ChildItem $userDir -ErrorAction SilentlyContinue | Select-Object -First 10 Name
} else {
    "NOT FOUND - creating"
    New-Item -ItemType Directory -Force $userDir | Out-Null
}
"=== Check ComfyUI API for workflows ==="
& "C:\Windows\System32\curl.exe" -s "http://127.0.0.1:8188/api/userdata" | ConvertFrom-Json | Select-Object -First 10 | ForEach-Object { "WORKFLOW: $($_.path) ($($_.size) bytes)" }
"=== Check templates dir ==="
Get-ChildItem "D:\Comfy-Desktop\ComfyUI-Installs\Krea-2-Turbo\ComfyUI\templates" -ErrorAction SilentlyContinue | Select-Object -First 10 Name | Out-String