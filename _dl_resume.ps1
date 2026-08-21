# Krea 2 Turbo FP8 - sequential download with resume (runs on game laptop)
# curl -C - resumes; retries on failure; writes progress to C:\dl_progress.log
$ErrorActionPreference = 'Continue'
$curl = "C:\Windows\System32\curl.exe"
$proxy = "http://127.0.0.1:7890"
$log = "C:\dl_progress.log"

function Log($msg){ $line = "[{0}] {1}" -f (Get-Date -Format "HH:mm:ss"), $msg; Add-Content $log $line; Write-Output $line }

function Download-Resume {
    param([string]$Url, [string]$Dest, [long]$Expected)
    $dir = Split-Path $Dest -Parent
    if(-not (Test-Path $dir)){ New-Item -ItemType Directory -Force $dir | Out-Null }
    if((Test-Path $Dest) -and ((Get-Item $Dest).Length -ge $Expected - 2048)){
        Log "SKIP exists: $(Split-Path $Dest -Leaf)"
        return
    }
    $name = Split-Path $Dest -Leaf
    Log "START: $name ($([math]::Round($Expected/1GB,2)) GB)"
    $sw = [System.Diagnostics.Stopwatch]::StartNew()
    $attempt = 0
    while($attempt -lt 20){
        $attempt++
        $cur = if(Test-Path $Dest){ (Get-Item $Dest).Length } else { 0 }
        $bin = "$Dest.aria"  # aria2-style temp? no--use curl -C - on same file
        # curl with resume: -C - resumes existing file
        $args = @('-s','-L','-x',$proxy,'-C','-','-o',$Dest,$Url)
        $p = Start-Process -FilePath $curl -ArgumentList $args -NoNewWindow -Wait -PassThru
        if($p.ExitCode -eq 0){
            $sz = (Get-Item $Dest).Length
            if($sz -ge $Expected - 2048){
                $sw.Stop()
                $rate = $sz/1MB/$sw.Elapsed.TotalSeconds
                Log "DONE: $name | $sz bytes | $([math]::Round($rate,1)) MB/s | attempt $attempt"
                return
            } else {
                Log "INCOMPLETE: $name $sz/$Expected - retry"
            }
        } else {
            Log "CURL EXIT $($p.ExitCode) on $name attempt $attempt - retry in 5s"
            Start-Sleep -Seconds 5
        }
    }
    Log "GAVE UP: $name"
}

# Job 1: main diffusion model 13.1GB
Download-Resume `
    -Url "https://huggingface.co/Comfy-Org/Krea-2/resolve/main/diffusion_models/krea2_turbo_fp8_scaled.safetensors" `
    -Dest "D:\Comfy-Desktop\ComfyUI-Shared\models\diffusion_models\krea2_turbo_fp8_scaled.safetensors" `
    -Expected 13141730784

# Job 2: text encoder 5.2GB
Download-Resume `
    -Url "https://huggingface.co/Comfy-Org/Qwen3-VL/resolve/main/text_encoders/qwen3vl_4b_fp8_scaled.safetensors" `
    -Dest "D:\Comfy-Desktop\ComfyUI-Shared\models\text_encoders\qwen3vl_4b_fp8_scaled.safetensors" `
    -Expected 5242467968

Log "ALL_DOWNLOADS_FINISHED"