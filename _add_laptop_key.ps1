# Add game laptop's SSH key to administrators_authorized_keys on 103
# Run via scheduled task as SYSTEM to bypass ACL restrictions
$key = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIMPJh4wzjUP8YZZIeMf9wOVCXKLNTC647b/6NLjVK3sl atemmie@WIN-8ITJT0L7H4P"
$file = "C:\ProgramData\ssh\administrators_authorized_keys"

# Check if already present
$content = Get-Content $file -Raw -ErrorAction SilentlyContinue
if($content -and $content.Contains("atemmie@WIN-8ITJT0L7H4P")){
    "ALREADY PRESENT"
} else {
    Add-Content -Path $file -Value $key
    "ADDED"
}
# Verify
$count = (Get-Content $file | Measure-Object -Line).Lines
"Total keys: $count"