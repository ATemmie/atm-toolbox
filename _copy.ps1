# Kill leftover curl, then copy the already-downloaded main model into place
Get-Process -Name curl -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 1

$src = "D:\app\pcl\PCL\MyDownload\2e83bf6e023aefb2a0a6dd2fa8c111634815cbe1a8b1a6f1f80e057f7eb54096"
$destDir = "D:\Comfy-Desktop\ComfyUI-Shared\models\diffusion_models"
$dest = Join-Path $destDir "krea2_turbo_fp8_scaled.safetensors"

# remove any 0-byte partial from failed download
if((Test-Path $dest) -and ((Get-Item $dest).Length -lt 1000000)){ Remove-Item $dest -Force }
Remove-Item "$dest.parts" -Recurse -Force -ErrorAction SilentlyContinue

"SRC EXISTS: $(Test-Path $src)"
if(Test-Path $src){
    $sw = [System.Diagnostics.Stopwatch]::StartNew()
    Copy-Item $src $dest -Force
    $sw.Stop()
    $sz = (Get-Item $dest).Length
    "COPIED: $dest"
    "SIZE: $sz bytes ($([math]::Round($sz/1GB,2)) GB)"
    "TIME: $([math]::Round($sw.Elapsed.TotalSeconds,1))s"
    "MATCH: $($sz -eq 13141730784)"
}