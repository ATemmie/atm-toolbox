# Submit Krea2 test workflow to ComfyUI API
$raw = Get-Content "C:\krea2_test_api.json" -Raw
$body = "{`"prompt`": $raw}"
$bytes = [System.Text.Encoding]::UTF8.GetBytes($body)
"SUBMITTING to http://127.0.0.1:8188/api/prompt ($($bytes.Length) bytes)"
try {
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:8188/api/prompt" -Method Post -Body $bytes -ContentType "application/json" -TimeoutSec 30 -UseBasicParsing
    "STATUS: $($response.StatusCode)"
    "RESPONSE: $($response.Content)"
} catch {
    "ERROR: $($_.Exception.Message)"
    if($_.Exception.Response){
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        "BODY: $($reader.ReadToEnd())"
    }
}