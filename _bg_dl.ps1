# Download text encoder in detached process (survives SSH disconnect)
$dest = "D:\Comfy-Desktop\ComfyUI-Shared\models\text_encoders\qwen3vl_4b_fp8_scaled.safetensors"
$url = "https://huggingface.co/Comfy-Org/Krea-2/resolve/main/text_encoders/qwen3vl_4b_fp8_scaled.safetensors"
$log = "C:\reDL_te_progress.log"

# Clear old log
"" | Out-File $log -Encoding ascii

# Start curl in detached background window
Start-Process -FilePath "C:\Windows\System32\curl.exe" `
    -ArgumentList "-s -L -x http://127.0.0.1:7890 -o $dest $url" `
    -WindowStyle Hidden

# Exit immediately so SSH session closes
"DOWNLOAD_STARTED_IN_BACKGROUND - check $log and file size later"
"curl PID: $((Get-Process curl -EA 0).Id -join ',')"