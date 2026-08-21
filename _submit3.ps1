# Fixed submit: write payload WITHOUT BOM using .NET methods
$raw = Get-Content "C:\krea2_test_api.json" -Raw
$payload = "{`"prompt`": $raw}"
# Write without BOM (UTF8 without BOM)
[System.IO.File]::WriteAllText("C:\krea2_payload.json", $payload, [System.Text.UTF8Encoding]::new($false))
"payload written ($($payload.Length) chars)"
# Submit via curl
$sw = [System.Diagnostics.Stopwatch]::StartNew()
$result = & "C:\Windows\System32\curl.exe" -s -w "\n%{http_code}" -X POST -H "Content-Type: application/json" -d "@C:\krea2_payload.json" "http://127.0.0.1:8188/api/prompt"
$sw.Stop()
"TIME: $([math]::Round($sw.Elapsed.TotalSeconds,1))s"
"RESULT: $result"