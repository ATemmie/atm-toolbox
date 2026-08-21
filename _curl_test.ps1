# Test curl.exe range download through Clash proxy on game laptop
$curl = "C:\Windows\System32\curl.exe"
if(-not (Test-Path $curl)){ $curl = (Get-Command curl.exe -ErrorAction SilentlyContinue).Source }
"CURL: $curl"

$url = "https://huggingface.co/Comfy-Org/Krea-2/resolve/main/diffusion_models/krea2_turbo_fp8_scaled.safetensors"
$tmp = "C:\krea_test_part.bin"

# single 50MB range via curl
$sw = [System.Diagnostics.Stopwatch]::StartNew()
$p = Start-Process -FilePath $curl -ArgumentList '-s','-L','-x','http://127.0.0.1:7890','-r','0-52428799','-o',$tmp,$url -Wait -NoNewWindow -PassThru
$sw.Stop()
if(Test-Path $tmp){
    $sz = (Get-Item $tmp).Length
    $speed = $sz/1MB/$sw.Elapsed.TotalSeconds
    "CURL RANGE: got $sz bytes in $([math]::Round($sw.Elapsed.TotalSeconds,1))s = $([math]::Round($speed,1)) MB/s | exit=$($p.ExitCode)"
    "RANGE_SUPPORTED: $($sz -ge 52428799)"
    Remove-Item $tmp -Force -ErrorAction SilentlyContinue
} else {
    "CURL FAILED exit=$($p.ExitCode)"
}