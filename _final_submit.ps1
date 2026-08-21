# Resubmit workflow now that text encoder is correct
$raw = Get-Content "C:\krea2_test_api.json" -Raw
$payload = "{`"prompt`": $raw}"
[System.IO.File]::WriteAllText("C:\krea2_payload.json", $payload, [System.Text.UTF8Encoding]::new($false))
# Submit
$sw = [System.Diagnostics.Stopwatch]::StartNew()
$result = & "C:\Windows\System32\curl.exe" -s -w "\n%{http_code}" -X POST -H "Content-Type: application/json" -d "@C:\krea2_payload.json" "http://127.0.0.1:8188/api/prompt"
$sw.Stop()
$code = ($result -split "`n")[-1]
$body = ($result -split "`n" | Select-Object -First ($result.Split("`n").Count - 1)) -join "`n"
"HTTP: $code | TIME: $([math]::Round($sw.Elapsed.TotalSeconds,1))s"
"BODY: $body"
# Extract prompt_id
if($body -match '"prompt_id":\s*"([^"]+)"'){
    $pid = $matches[1]
    "PROMPT_ID: $pid"
    # Poll for completion
    $maxWait = 300
    $t = 0
    while($t -lt $maxWait){
        Start-Sleep -Seconds 5
        $t += 5
        $hist = & "C:\Windows\System32\curl.exe" -s "http://127.0.0.1:8188/history/$pid"
        if($hist -match '"completed":\s*true'){
            "COMPLETED after ${t}s"
            # Check for errors
            if($hist -match '"status_str":\s*"error"'){
                "ERROR in execution!"
                $hist
            } else {
                "SUCCESS - checking output..."
                $hist
            }
            break
        }
        if($t % 15 -eq 0){ "still running... ${t}s" }
    }
    if($t -ge $maxWait){ "TIMEOUT after ${maxWait}s" }
}