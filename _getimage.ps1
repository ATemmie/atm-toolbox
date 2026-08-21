# Download output image
$dest = "D:\Comfy-Desktop\ComfyUI-Shared\output\krea2_test_00001_.png"
$url = "http://127.0.0.1:8188/api/view?filename=krea2_test_00001_.png&type=output"
& "C:\Windows\System32\curl.exe" -s -o $dest $url
$sz = (Get-Item $dest).Length
"IMAGE: $dest ($sz bytes)"
# Copy to Desktop for easy access
Copy-Item $dest "C:\Users\ATemmie\Desktop\krea2_test_00001_.png" -Force
"Copied to Desktop: krea2_test_00001_.png"