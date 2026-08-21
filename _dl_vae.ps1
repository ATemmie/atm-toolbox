# Krea 2 Turbo FP8 model downloader (runs on game laptop)
# Uses system Clash proxy at 127.0.0.1:7890, resumes interrupted downloads
$ErrorActionPreference = 'Stop'
$proxy = "http://127.0.0.1:7890"

$jobs = @(
    @{
        Url  = "https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI/resolve/main/split_files/vae/qwen_image_vae.safetensors"
        Dest = "D:\Comfy-Desktop\ComfyUI-Shared\models\vae\qwen_image_vae.safetensors"
        Name = "qwen_image_vae.safetensors"
    }
)

foreach($j in $jobs){
    $dest = $j.Dest
    $dir = Split-Path $dest -Parent
    if(-not (Test-Path $dir)){ New-Item -ItemType Directory -Force $dir | Out-Null }

    # Check if already complete
    if((Test-Path $dest) -and ((Get-Item $dest).Length -gt 250000000)){
        "SKIP (exists): $($j.Name)"
        continue
    }

    "DOWNLOADING: $($j.Name)"
    $tmp = "$dest.part"
    # Get expected size
    try {
        $head = Invoke-WebRequest -Uri $j.Url -Method Head -Proxy $proxy -TimeoutSec 30
        $expected = $head.Headers.'Content-Length'
        "expected bytes: $expected"
    } catch {
        "HEAD failed (will download blind): $($_.Exception.Message)"
        $expected = $null
    }

    $sw = [System.Diagnostics.Stopwatch]::StartNew()
    try {
        Invoke-WebRequest -Uri $j.Url -OutFile $tmp -Proxy $proxy -TimeoutSec 600 -UseBasicParsing
        Move-Item $tmp $dest -Force
        $sw.Stop()
        $sz = (Get-Item $dest).Length
        "DONE: $($j.Name) | $sz bytes | $([math]::Round($sw.Elapsed.TotalSeconds,1))s | $([math]::Round($sz/1MB/$sw.Elapsed.TotalSeconds,1)) MB/s"
    } catch {
        "FAIL: $($j.Name) :: $($_.Exception.Message)"
        if(Test-Path $tmp){ "partial file kept at $tmp ($((Get-Item $tmp).Length) bytes)" }
    }
}
"ALL_JOBS_FINISHED"