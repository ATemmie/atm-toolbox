# Create a scheduled task to download text encoder (survives SSH disconnect)
$dest = "D:\Comfy-Desktop\ComfyUI-Shared\models\text_encoders\qwen3vl_4b_fp8_scaled.safetensors"
$url = "https://huggingface.co/Comfy-Org/Krea-2/resolve/main/text_encoders/qwen3vl_4b_fp8_scaled.safetensors"

# Delete old 0-byte file
if(Test-Path $dest){ Remove-Item $dest -Force }

# Write a bat file for the task
$bat = @"
@echo off
curl -s -L -x http://127.0.0.1:7890 -o "$dest" "$url" > C:\dl_te_task.log 2>&1
echo DONE %DATE% %TIME% >> C:\dl_te_task.log
"@
$bat | Out-File "C:\dl_te_task.bat" -Encoding ascii -Force

# Create one-time scheduled task to run immediately
schtasks /Delete /TN "KreaDL_TE" /F 2>$null
schtasks /Create /TN "KreaDL_TE" /TR "cmd /c C:\dl_te_task.bat" /SC ONCE /ST 00:00 /RL HIGHEST /F /RU ATemmie
schtasks /Run /TN "KreaDL_TE"

Start-Sleep -Seconds 3
"TASK CREATED AND RUN"
"curl should be running now"
tasklist /FI IMAGENAME eq curl.exe 2>$null