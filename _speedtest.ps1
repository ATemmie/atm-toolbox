# Multi-part parallel downloader for HF models via Clash proxy
# Part 1: test whether HF honors Range requests through this proxy, and measure speed
$ErrorActionPreference = 'Stop'
$proxy = "http://127.0.0.1:7890"
$url = "https://huggingface.co/Comfy-Org/Krea-2/resolve/main/diffusion_models/krea2_turbo_fp8_scaled.safetensors"

# expected total size
$head = Invoke-WebRequest -Uri $url -Method Head -Proxy $proxy -TimeoutSec 30
$total = [long]$head.Headers.'Content-Length'
"TOTAL: $total bytes ($([math]::Round($total/1GB,2)) GB)"

# test a 50MB range
$tmp = "C:\krea_test_part.bin"
$sw = [System.Diagnostics.Stopwatch]::StartNew()
$range = "bytes=0-52428799"
$wc = New-Object System.Net.WebClient
$wc.Proxy = New-Object System.Net.WebProxy($proxy)
$wc.Headers.Add("Range", $range)
$wc.DownloadFile($url, $tmp)
$sw.Stop()
$sz = (Get-Item $tmp).Length
$speed = $sz/1MB/$sw.Elapsed.TotalSeconds
"RANGE TEST: got $sz bytes in $([math]::Round($sw.Elapsed.TotalSeconds,1))s = $([math]::Round($speed,1)) MB/s"
Remove-Item $tmp -Force -ErrorAction SilentlyContinue
"RANGE_SUPPORTED: $($sz -ge 52428799)"