# Get raw object_info for Krea2 nodes
$raw = & "C:\Windows\System32\curl.exe" -s "http://127.0.0.1:8188/object_info/Krea2ImageNode"
"=== RAW Krea2ImageNode ==="
$raw
""
$raw2 = & "C:\Windows\System32\curl.exe" -s "http://127.0.0.1:8188/object_info/UNETLoader"
"=== RAW UNETLoader ==="
$raw2