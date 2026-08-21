# Wrap prompt and submit via curl (avoids PowerShell encoding issues)
$raw = Get-Content "C:\krea2_test_api.json" -Raw
$payload = "{`"prompt`": $raw}"
$payload | Out-File "C:\krea2_payload.json" -Encoding utf8 -NoNewline
"CURL SUBMIT..."
$sw = [System.Diagnostics.Stopwatch]::StartNew()
$c = "C:\Windows\System32\curl.exe"
$result = & $c -s -w "\n%{http_code}" -X POST -H "Content-Type: application/json" -d "@C:\krea2_payload.json" "http://127.0.0.1:8188/api/prompt"
$sw.Stop()
"TIME: $([math]::Round($sw.Elapsed.TotalSeconds,1))s"
"RESULT: $result"