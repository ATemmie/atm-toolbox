$f = "D:\app\pcl\PCL\MyDownload\2e83bf6e023aefb2a0a6dd2fa8c111634815cbe1a8b1a6f1f80e057f7eb54096"
"FILE: $f"
"EXISTS: $(Test-Path $f)"
if(Test-Path $f){
    $fi = Get-Item $f
    "SIZE: $($fi.Length) bytes = $([math]::Round($fi.Length/1GB,2)) GB"
    # Read first 8 bytes via FileStream (header length for safetensors)
    $fs = [System.IO.File]::OpenRead($f)
    $buf = New-Object byte[] 8
    $read = $fs.Read($buf, 0, 8)
    $fs.Close()
    "READ: $read bytes"
    $hex = ($buf | ForEach-Object { $_.ToString("X2") }) -join " "
    "HEADER HEX (8 bytes): $hex"
    # safetensors: first 8 bytes = little-endian JSON header length
    if($read -eq 8){
        $len = [BitConverter]::ToUInt64($buf, 0)
        "JSON HEADER LENGTH: $len (sane if 50-1000)"
        "LOOKS_LIKE_SAFETENSORS: $($len -gt 0 -and $len -lt 1000000)"
    }
}