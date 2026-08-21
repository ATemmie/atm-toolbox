# Diagnose: why did parallel curl segments yield 0 bytes?
$curl = "C:\Windows\System32\curl.exe"
$url = "https://huggingface.co/Comfy-Org/Krea-2/resolve/main/diffusion_models/krea2_turbo_fp8_scaled.safetensors"
$proxy = "http://127.0.0.1:7890"
$logDir = "C:\krea_diag"
New-Item -ItemType Directory -Force $logDir | Out-Null

# Test 1: single curl with stderr to file (same args as part downloader)
"--- TEST 1: single segment via Start-Process with stderr capture ---"
$args1 = @('-s','-L','-x',$proxy,'-r','0-52428799','-o',"$logDir\p0.bin",$url)
$p = Start-Process -FilePath $curl -ArgumentList $args1 -NoNewWindow -Wait -PassThru -RedirectStandardError "$logDir\p0.err"
"exit=$($p.ExitCode) size=$((Get-Item "$logDir\p0.bin" -ErrorAction SilentlyContinue).Length)"
Get-Content "$logDir\p0.err" -ErrorAction SilentlyContinue | Select-Object -First 5

# Test 2: same but wait manually (no -Wait), like the loop does
"--- TEST 2: Start-Process without -Wait, then WaitForExit ---"
$args2 = @('-s','-L','-x',$proxy,'-r','0-52428799','-o',"$logDir\p1.bin",$url)
$p2 = Start-Process -FilePath $curl -ArgumentList $args2 -NoNewWindow -PassThru -RedirectStandardError "$logDir\p1.err"
$p2.WaitForExit()
"exit=$($p2.ExitCode) size=$((Get-Item "$logDir\p1.bin" -ErrorAction SilentlyContinue).Length)"
Get-Content "$logDir\p1.err" -ErrorAction SilentlyContinue | Select-Object -First 5

# Test 3: run curl directly (synchronous, non-Start-Process) as baseline
"--- TEST 3: direct curl.exe invocation ---"
$sw = [System.Diagnostics.Stopwatch]::StartNew()
$p3 = Start-Process -FilePath $curl -ArgumentList @('-s','-L','-x',$proxy,'-r','0-52428799','-o',"$logDir\p2.bin",$url) -NoNewWindow -Wait -PassThru
$sw.Stop()
"exit=$($p3.ExitCode) size=$((Get-Item "$logDir\p2.bin" -ErrorAction SilentlyContinue).Length) in $([math]::Round($sw.Elapsed.TotalSeconds,1))s"

"DIAG_DONE"