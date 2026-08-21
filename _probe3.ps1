"===== Krea-2-Turbo install models ====="
$krea = "D:\Comfy-Desktop\ComfyUI-Installs\Krea-2-Turbo\ComfyUI\models"
if(Test-Path $krea){
    Get-ChildItem $krea -Recurse -Depth 1 -ErrorAction SilentlyContinue | ForEach-Object {
        $t = if($_.PSIsContainer){"[DIR]"}else{"{0:N1}MB" -f ($_.Length/1MB)}
        "{0}`t{1}" -f $t, $_.FullName
    }
}
"===== ComfyUI (1) models ====="
$c1 = "D:\Comfy-Desktop\ComfyUI-Installs\ComfyUI (1)\ComfyUI\models"
if(Test-Path $c1){
    Get-ChildItem $c1 -Recurse -Depth 1 -ErrorAction SilentlyContinue | ForEach-Object {
        $t = if($_.PSIsContainer){"[DIR]"}else{"{0:N1}MB" -f ($_.Length/1MB)}
        "{0}`t{1}" -f $t, $_.FullName
    }
}
"===== Shared models ====="
$sh = "D:\Comfy-Desktop\ComfyUI-Shared\models"
if(Test-Path $sh){
    Get-ChildItem $sh -Recurse -Depth 1 -ErrorAction SilentlyContinue | ForEach-Object {
        $t = if($_.PSIsContainer){"[DIR]"}else{"{0:N1}MB" -f ($_.Length/1MB)}
        "{0}`t{1}" -f $t, $_.FullName
    }
}