# Get detailed info on Krea2 nodes
$result = & "C:\Windows\System32\curl.exe" -s "http://127.0.0.1:8188/object_info/Krea2ImageNode" | ConvertFrom-Json
"=== Krea2ImageNode ==="
$result.input_required | ForEach-Object { "REQUIRED: $($_.name) ($($_.type))" }
$result.input_optional | ForEach-Object { "OPTIONAL: $($_.name) ($($_.type))" }
# Also check ModelMergeKrea2
$result2 = & "C:\Windows\System32\curl.exe" -s "http://127.0.0.1:8188/object_info/ModelMergeKrea2" | ConvertFrom-Json
"=== ModelMergeKrea2 ==="
$result2.input_required | ForEach-Object { "REQUIRED: $($_.name) ($($_.type))" }