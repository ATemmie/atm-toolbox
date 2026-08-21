"===== PCL MyDownload dir ====="
Get-ChildItem "D:\app\pcl\PCL\MyDownload" -ErrorAction SilentlyContinue | ForEach-Object {
    $sizeMB = [math]::Round($_.Length/1MB,1)
    "{0}`t{1}`t{2}" -f $sizeMB, $_.LastWriteTime, $_.FullName
}
"===== check if it's a safetensors (header) ====="
$f = "D:\app\pcl\PCL\MyDownload\2e83bf6e023aefb2a0a6dd2fa8c111634815cbe1a8b1a6f1f80e057f7eb54096"
if(Test-Path $f){
    $fi = Get-Item $f
    "SIZE: $($fi.Length) bytes ($([math]::Round($fi.Length/1GB,2)) GB)"
    $bytes = [System.IO.File]::ReadAllBytes($f)[0..7]
    $hex = ($bytes | ForEach-Object { $_.ToString("X2") }) -join " "
    "HEADER HEX: $hex"
    $ascii = -join ($bytes | ForEach-Object { if($_ -ge 32 -and $_ -le 126){[char]$_}else{"."} })
    "HEADER ASCII: $ascii"
    # safetensors header is a JSON length prefix (8 bytes little-endian)
    $len = [BitConverter]::ToUInt64($bytes, 0)
    "IF SAFETENSORS, JSON header length would be: $len"
}
"===== Krea shared dir current state ====="
Get-ChildItem "D:\Comfy-Desktop\ComfyUI-Shared\models\diffusion_models" -ErrorAction SilentlyContinue | ForEach-Object { "{0:N1}MB`t{1}" -f ($_.Length/1MB), $_.Name }
Get-ChildItem "D:\Comfy-Desktop\ComfyUI-Shared\models\text_encoders" -ErrorAction SilentlyContinue | ForEach-Object { "{0:N1}MB`t{1}" -f ($_.Length/1MB), $_.Name }
"===== dl_progress.log ====="
if(Test-Path "C:\dl_progress.log"){ Get-Content "C:\dl_progress.log" }
"===== curl processes running? ====="
Get-Process -Name curl -ErrorAction SilentlyContinue | Select-Object Id,CPU,StartTime | Format-Table -AutoSize | Out-String