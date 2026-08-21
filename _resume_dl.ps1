# Resume download with verbose output and size check
$dest = "D:\Comfy-Desktop\ComfyUI-Shared\models\text_encoders\qwen3vl_4b_fp8_scaled.safetensors"
$url = "https://huggingface.co/Comfy-Org/Krea-2/resolve/main/text_encoders/qwen3vl_4b_fp8_scaled.safetensors"
$expected = 5242467968
$log = "C:\dl_te_resume.log"

$current = if(Test-Path $dest){ (Get-Item $dest).Length } else { 0 }
"CURRENT: $current bytes, EXPECTED: $expected bytes"

if($current -ge $expected - 1024){
    "ALREADY COMPLETE"
    exit 0
}

# Delete incomplete and re-download fresh (no resume, clean slate)
if(Test-Path $dest){ Remove-Item $dest -Force }

$bat = @"
@echo off
echo STARTING DOWNLOAD %DATE% %TIME%
curl -L -x http://127.0.0.1:7890 -o "$dest" "$url"
echo EXIT CODE: %ERRORLEVEL%
dir "$dest"
echo DONE %DATE% %TIME%
"@
$bat | Out-File "C:\dl_te_resume.bat" -Encoding ascii -Force

schtasks /Delete /TN "KreaDL_TE" /F 2>$null
schtasks /Create /TN "KreaDL_TE" /TR "cmd /c C:\dl_te_resume.bat" /SC ONCE /ST 00:00 /RL HIGHEST /F /RU ATemmie
schtasks /Run /TN "KreaDL_TE"
Start-Sleep -Seconds 3
"TASK STARTED - will take ~5-10 min for 4.88GB"
tasklist /FI IMAGENAME eq curl.exe 2>nul