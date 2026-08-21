# Download Krea2 Refusal-Reduction LoRA from HuggingFace
$dest = "D:\Comfy-Desktop\ComfyUI-Shared\models\loras\Krea2_TextFusion_Refusal_Reduction.safetensors"
$url = "https://huggingface.co/Quiho/Krea2_TextFusion_Refusal-Reduction_LoRA_v1.0_lora/resolve/main/Krea2_TextFusion_Refusal_Reduction.safetensors"

if(Test-Path $dest){
    $sz = (Get-Item $dest).Length
    "ALREADY EXISTS: $sz bytes"
    exit 0
}

# Check expected size first
$head = & "C:\Windows\System32\curl.exe" -s -x http://127.0.0.1:7890 -I -L $url 2>&1
$sizeLine = ($head -split "`n") | Where-Object { $_ -match "content-length" } | Select-Object -First 1
"SIZE: $sizeLine"

# Download via scheduled task (survives SSH disconnect)
$bat = @"
@echo off
echo STARTING LORA DOWNLOAD %DATE% %TIME%
curl -L -x http://127.0.0.1:7890 -o "$dest" "$url"
echo EXIT CODE: %ERRORLEVEL%
dir "$dest"
echo DONE %DATE% %TIME%
"@
$bat | Out-File "C:\dl_lora.bat" -Encoding ascii -Force

schtasks /Delete /TN "KreaDL_LoRA" /F 2>$null
schtasks /Create /TN "KreaDL_LoRA" /TR "cmd /c C:\dl_lora.bat" /SC ONCE /ST 00:00 /RL HIGHEST /F /RU ATemmie
schtasks /Run /TN "KreaDL_LoRA"
Start-Sleep -Seconds 3
"TASK STARTED - downloading LoRA..."
tasklist /FI IMAGENAME eq curl.exe 2>nul