# Krea 2 Turbo FP8 - parallel segmented downloader (runs on game laptop)
# Uses curl.exe with Range requests through Clash proxy, then merges parts.
$ErrorActionPreference = 'Continue'
$curl = "C:\Windows\System32\curl.exe"
$proxy = "http://127.0.0.1:7890"

function Get-PartialDownload {
    param(
        [string]$Url,
        [string]$Dest,
        [int]$Segments = 6,
        [long]$ExpectedSize
    )
    $dir = Split-Path $Dest -Parent
    if(-not (Test-Path $dir)){ New-Item -ItemType Directory -Force $dir | Out-Null }

    # already complete?
    if((Test-Path $Dest) -and ((Get-Item $Dest).Length -ge $ExpectedSize - 1024)){
        "SKIP (exists): $(Split-Path $Dest -Leaf)"
        return
    }

    "=== DOWNLOAD: $(Split-Path $Dest -Leaf) ($([math]::Round($ExpectedSize/1GB,2)) GB, $Segments segments) ==="
    $partDir = "$Dest.parts"
    if(-not (Test-Path $partDir)){ New-Item -ItemType Directory -Force $partDir | Out-Null }

    $segSize = [math]::Ceiling($ExpectedSize / $Segments)
    $procs = @()
    for($i=0; $i -lt $Segments; $i++){
        $start = $i * $segSize
        if($start -ge $ExpectedSize){ break }
        $end = [math]::Min($start + $segSize - 1, $ExpectedSize - 1)
        $partFile = Join-Path $partDir ("part_{0:D2}" -f $i)
        $range = "bytes=$start-$end"
        # resume: skip if part already at expected size
        if((Test-Path $partFile) -and ((Get-Item $partFile).Length -ge ($end - $start + 1))){
            "part $i already done"
            continue
        }
        $p = Start-Process -FilePath $curl -ArgumentList '-s','-L','-x',$proxy,'-r',$range,'-o',$partFile,$Url -NoNewWindow -PassThru
        $procs += ,$p
        "started part $i (bytes $start-$end)"
    }
    foreach($p in $procs){ $p.WaitForExit() }
    "all curl processes exited"

    # verify parts and merge
    $good = $true
    $totalGot = [long]0
    $partFiles = @()
    for($i=0; $i -lt $Segments; $i++){
        $partFile = Join-Path $partDir ("part_{0:D2}" -f $i)
        if(-not (Test-Path $partFile)){ "MISSING part $i"; $good = $false; continue }
        $sz = (Get-Item $partFile).Length
        $totalGot += $sz
        $partFiles += $partFile
        "part $i size $sz"
    }
    if($good -and ($totalGot -ge $ExpectedSize - 1024)){
        "merging parts ($totalGot bytes)..."
        $mergeScript = "copy /b " + ($partFiles -join "+") + " `"$Dest`""
        cmd /c $mergeScript | Out-Null
        $final = (Get-Item $Dest).Length
        "MERGED: $Dest ($final bytes)"
        if($final -ge $ExpectedSize - 1024){
            Remove-Item $partDir -Recurse -Force -ErrorAction SilentlyContinue
            "CLEANUP OK"
        } else {
            "WARNING: final size mismatch, parts kept for retry"
        }
    } else {
        "PARTIAL: $totalGot / $ExpectedSize - parts kept, rerun to resume"
    }
}

# Job 1: main diffusion model (13.1 GB, 6 segments)
Get-PartialDownload `
    -Url "https://huggingface.co/Comfy-Org/Krea-2/resolve/main/diffusion_models/krea2_turbo_fp8_scaled.safetensors" `
    -Dest "D:\Comfy-Desktop\ComfyUI-Shared\models\diffusion_models\krea2_turbo_fp8_scaled.safetensors" `
    -Segments 6 -ExpectedSize 13141730784

# Job 2: text encoder (5.2 GB, 4 segments)
Get-PartialDownload `
    -Url "https://huggingface.co/Comfy-Org/Qwen3-VL/resolve/main/text_encoders/qwen3vl_4b_fp8_scaled.safetensors" `
    -Dest "D:\Comfy-Desktop\ComfyUI-Shared\models\text_encoders\qwen3vl_4b_fp8_scaled.safetensors" `
    -Segments 4 -ExpectedSize 5242467968

"===== ALL DOWNLOADS FINISHED ====="