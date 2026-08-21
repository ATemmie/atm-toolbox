Remove-Item "D:\Comfy-Desktop\ComfyUI-Shared\models\diffusion_models\krea2_turbo_fp8_scaled.safetensors.parts" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "D:\Comfy-Desktop\ComfyUI-Shared\models\text_encoders\qwen3vl_4b_fp8_scaled.safetensors.parts" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "C:\krea_test_part.bin" -Force -ErrorAction SilentlyContinue
Remove-Item "C:\krea_diag" -Recurse -Force -ErrorAction SilentlyContinue
"=== diffusion_models ==="
Get-ChildItem "D:\Comfy-Desktop\ComfyUI-Shared\models\diffusion_models" -ErrorAction SilentlyContinue | ForEach-Object { "{0:N1}MB`t{1}" -f ($_.Length/1MB), $_.Name }
"=== text_encoders ==="
Get-ChildItem "D:\Comfy-Desktop\ComfyUI-Shared\models\text_encoders" -ErrorAction SilentlyContinue | ForEach-Object { "{0:N1}MB`t{1}" -f ($_.Length/1MB), $_.Name }
"=== vae ==="
Get-ChildItem "D:\Comfy-Desktop\ComfyUI-Shared\models\vae" -ErrorAction SilentlyContinue | ForEach-Object { "{0:N1}MB`t{1}" -f ($_.Length/1MB), $_.Name }