$raw = Get-Content "C:\krea2_test_api.json" -Raw
$payload = "{`"prompt`": $raw}"
[System.IO.File]::WriteAllText("C:\krea2_payload.json", $payload, [System.Text.UTF8Encoding]::new($false))
$result = & "C:\Windows\System32\curl.exe" -s -w "\n%{http_code}" -X POST -H "Content-Type: application/json" -d "@C:\krea2_payload.json" "http://127.0.0.1:8188/api/prompt"
$result