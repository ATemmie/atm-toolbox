# Check status: curl running? file size?
$curlProcs = Get-Process curl -ErrorAction SilentlyContinue
if($curlProcs){ "CURL RUNNING: $($curlProcs.Count) processes"; $curlProcs | Select-Object Id,StartTime | Format-Table -AutoSize | Out-String } else { "NO CURL RUNNING" }

$f = "D:\Comfy-Desktop\ComfyUI-Shared\models\text_encoders\qwen3vl_4b_fp8_scaled.safetensors"
if(Test-Path $f){
    $sz = (Get-Item $f).Length
    "FILE: $sz bytes ($([math]::Round($sz/1GB,2)) GB)"
    "EXPECTED: 5242467968 bytes (4.88 GB)"
    "RATIO: $([math]::Round($sz/5242467968*100,1))%"
} else {
    "FILE NOT FOUND - may have been deleted by the script"
}
# Check reDL_te log
if(Test-Path "C:\dl_te.log"){ "=== dl_te.log ==="; Get-Content "C:\dl_te.log" -Tail 5 }
# Check if any .ps1 script is still running
Get-Process powershell -ErrorAction SilentlyContinue | Select-Object Id,StartTime | Format-Table -AutoSize | Out-String