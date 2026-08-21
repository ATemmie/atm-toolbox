$f = "D:\Comfy-Desktop\ComfyUI-Shared\models\loras\Krea2_TextFusion_Refusal_Reduction.safetensors"
"=== LoRA FILE CHECK ==="
if(Test-Path $f){
    $fi = Get-Item $f
    "SIZE: $($fi.Length) bytes ($([math]::Round($fi.Length/1MB,1)) MB)"
    $fs = [System.IO.File]::OpenRead($f)
    $buf = New-Object byte[] 8
    $fs.Read($buf, 0, 8) | Out-Null
    $fs.Close()
    $hex = ($buf | ForEach-Object { $_.ToString("X2") }) -join " "
    $len = [BitConverter]::ToUInt64($buf, 0)
    "HEADER HEX: $hex"
    "JSON LEN: $len (valid if < 1000000)"
    "LOOKS_LIKE_SAFETENSORS: $($len -gt 0 -and $len -lt 1000000)"
} else {
    "FILE NOT FOUND"
}
"=== loras directory ==="
Get-ChildItem "D:\Comfy-Desktop\ComfyUI-Shared\models\loras" -ErrorAction SilentlyContinue | ForEach-Object { "{0:N1}MB  {1}" -f ($_.Length/1MB), $_.Name }