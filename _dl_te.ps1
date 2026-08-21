# Download qwen3vl_4b_fp8_scaled.safetensors (5.2GB) with resume+retry
$ErrorActionPreference = 'Continue'
$curl = "C:\Windows\System32\curl.exe"
$proxy = "http://127.0.0.1:7890"
$log = "C:\dl_te.log"

$url = "https://huggingface.co/Comfy-Org/Qwen3-VL/resolve/main/text_encoders/qwen3vl_4b_fp8_scaled.safetensors"
$dest = "D:\Comfy-Desktop\ComfyUI-Shared\models\text_encoders\qwen3vl_4b_fp8_scaled.safetensors"
$expected = 5242467968

Add-Content $log "[$(Get-Date -Format 'HH:mm:ss')] START qwen3vl_4b_fp8_scaled"
$sw = [System.Diagnostics.Stopwatch]::StartNew()
$attempt = 0
while($attempt -lt 30){
    $attempt++
    $p = Start-Process -FilePath $curl -ArgumentList @('-s','-L','-x',$proxy,'-C','-','-o',$dest,$url) -NoNewWindow -Wait -PassThru
    $sz = if(Test-Path $dest){ (Get-Item $dest).Length } else { 0 }
    if($p.ExitCode -eq 0 -and $sz -ge $expected - 2048){
        $sw.Stop()
        $rate = $sz/1MB/$sw.Elapsed.TotalSeconds
        Add-Content $log "[$(Get-Date -Format 'HH:mm:ss')] DONE $sz bytes $([math]::Round($rate,1)) MB/s attempt $attempt"
        break
    } else {
        Add-Content $log "[$(Get-Date -Format 'HH:mm:ss')] attempt $attempt exit=$($p.ExitCode) size=$sz - retry"
        Start-Sleep -Seconds 5
    }
}
Add-Content $log "[$(Get-Date -Format 'HH:mm:ss')] FINAL size=$((Get-Item $dest).Length) expected=$expected"
Add-Content $log "TE_DOWNLOAD_DONE"