# Re-download text encoder from correct source (Comfy-Org/Krea-2 repo, not Qwen3-VL)
$ErrorActionPreference = 'Stop'
$curl = "C:\Windows\System32\curl.exe"
$proxy = "http://127.0.0.1:7890"
$dest = "D:\Comfy-Desktop\ComfyUI-Shared\models\text_encoders\qwen3vl_4b_fp8_scaled.safetensors"

# Use the URL from workflow template (Krea-2 repo)
$url = "https://huggingface.co/Comfy-Org/Krea-2/resolve/main/text_encoders/qwen3vl_4b_fp8_scaled.safetensors"

# Delete old corrupted file
if(Test-Path $dest){
    $old = Get-Item $dest
    "OLD: $($old.Length) bytes (expected 5242467968)"
    Remove-Item $dest -Force
}

# Get expected size first
$head = & $curl -s -x $proxy -I -L $url
"HEAD response:"
$head
$sizeLine = ($head -split "`n") | Where-Object { $_ -match "content-length" } | Select-Object -First 1
"SIZE LINE: $sizeLine"

# Download
"DOWNLOADING from $url"
$sw = [System.Diagnostics.Stopwatch]::StartNew()
& $curl -s -L -x $proxy -o $dest $url
$sw.Stop()

if(Test-Path $dest){
    $sz = (Get-Item $dest).Length
    "DOWNLOADED: $sz bytes ($([math]::Round($sz/1GB,2)) GB) in $([math]::Round($sw.Elapsed.TotalSeconds,1))s"
    "SIZE MATCH EXACT: $($sz -eq 5242467968)"
    "SIZE CLOSE (>5GB): $($sz -gt 5000000000)"
} else {
    "DOWNLOAD FAILED"
}