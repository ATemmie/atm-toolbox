# Query ComfyUI API for available node types
$result = & "C:\Windows\System32\curl.exe" -s "http://127.0.0.1:8188/object_info" | ConvertFrom-Json
# Filter for relevant loader/sampler/encode nodes
$keywords = @("unet","load","sampler","clip","vae","krea","qwen","diffusion","encode","empty","save","image")
$found = @()
foreach($name in $result.PSObject.Properties.Name){
    if($name -match ($keywords -join "|")){ $found += $name }
}
"=== AVAILABLE LOADING/PROCESSING NODES ==="
$found | Sort-Object | ForEach-Object { $_ }