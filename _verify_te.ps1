$f = "D:\Comfy-Desktop\ComfyUI-Shared\models\text_encoders\qwen3vl_4b_fp8_scaled.safetensors"
"=== FILE CHECK ==="
if(Test-Path $f){
    $fi = Get-Item $f
    "SIZE: $($fi.Length) bytes ($([math]::Round($fi.Length/1GB,2)) GB)"
    $fs = [System.IO.File]::OpenRead($f)
    $buf = New-Object byte[] 8
    $fs.Read($buf, 0, 8) | Out-Null
    $fs.Close()
    $hex = ($buf | ForEach-Object { $_.ToString("X2") }) -join " "
    $len = [BitConverter]::ToUInt64($buf, 0)
    "HEADER HEX: $hex"
    "JSON LEN: $len (valid safetensors if < 1000000)"
    # Also read first 100 bytes as ASCII to spot HTML/JSON errors
    $fs2 = [System.IO.File]::OpenRead($f)
    $buf2 = New-Object byte[] 100
    $fs2.Read($buf2, 0, 100) | Out-Null
    $fs2.Close()
    $ascii = -join ($buf2[8..99] | ForEach-Object { if($_ -ge 32 -and $_ -le 126){[char]$_}else{"."} })
    "AFTER 8B HEADER: $ascii"
} else {
    "FILE NOT FOUND"
}
"=== HF API re-verify size ==="
try { $r = Invoke-RestMethod -Uri "https://huggingface.co/api/models/Comfy-Org/Qwen3-VL/tree/main/text_encoders" -TimeoutSec 15; $r | ForEach-Object { "$($_.path)  size=$($_.size)" } } catch { "API FAIL: $($_.Exception.Message)" }