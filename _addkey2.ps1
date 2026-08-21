$key = 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIMPJh4wzjUP8YZZIeMf9wOVCXKLNTC647b/6NLjVK3sl atemmie@WIN-8ITJT0L7H4P'
$authFile = 'C:\ProgramData\ssh\administrators_authorized_keys'
$content = Get-Content $authFile -Raw
if ($content -like '*atemmie@WIN-8ITJT0L7H4P*') {
    "ALREADY_PRESENT"
} else {
    Add-Content -Path $authFile -Value $key
    "APPENDED"
}
"KEY_COUNT: " + (Get-Content $authFile | Measure-Object -Line).Lines
"--- ACL ---"
icacls $authFile | Out-String