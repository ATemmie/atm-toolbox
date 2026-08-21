# Poll for completion and get output
$sw = [System.Diagnostics.Stopwatch]::StartNew()
$done = $false
while(-not $done -and $sw.Elapsed.TotalSeconds -lt 300){
    Start-Sleep -Seconds 5
    $hist = & "C:\Windows\System32\curl.exe" -s "http://127.0.0.1:8188/history/97a908b7-6155-4327-bb81-4d139df897c9"
    if($hist -match '"status".*"completed"'){
        $done = $true
        "COMPLETED after $([math]::Round($sw.Elapsed.TotalSeconds,1))s"
        # Parse outputs
        $json = $hist | ConvertFrom-Json
        $outputs = $json.'97a908b7-6155-4327-bb81-4d139df897c9'.outputs
        $saveNode = $outputs.'9'
        if($saveNode -and $saveNode.images){
            foreach($img in $saveNode.images){
                "IMAGE: $($img.filename) in $($img.subfolder) (type: $($img.type))"
                # Download image
                $imgUrl = "http://127.0.0.1:8188/api/view?filename=$($img.filename)&subfolder=$($img.subfolder)&type=$($img.type)"
                $outPath = "D:\Comfy-Desktop\ComfyUI-Shared\output\$($img.filename)"
                & "C:\Windows\System32\curl.exe" -s -o $outPath $imgUrl
                $sz = (Get-Item $outPath).Length
                "SAVED: $outPath ($sz bytes)"
            }
        } else {
            "No images in output. Full history:"
            $hist | Select-Object -First 2000
        }
    } else {
        "waiting... ($([math]::Round($sw.Elapsed.TotalSeconds,1))s)"
    }
}
if(-not $done){ "TIMEOUT after 300s" }
"DONE"