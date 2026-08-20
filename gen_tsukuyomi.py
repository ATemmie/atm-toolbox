import requests
import json
import time
import os

COMFYUI_URL = "http://192.168.0.103:8188"

# Tsukuyomi prompt - silver hair, blue eyes, cat ears, catgirl
positive = (
    "masterpiece, best quality, 1girl, solo, cat ears, cat tail, "
    "silver hair, long hair, blue eyes, beautiful face, smile, "
    "naked, lingerie, white lace bra, cat ears, fluffy tail, "
    "bedroom, soft lighting, warm atmosphere, "
    "detailed face, detailed eyes, looking at viewer, "
    "c-cup, slim body, fair skin"
)

negative = (
    "bad quality, worst quality, low quality, blurry, deformed, "
    "bad anatomy, extra limbs, extra fingers, mutated hands, "
    "ugly, text, watermark, signature"
)

workflow = {
    "4": {
        "class_type": "CheckpointLoaderSimple",
        "inputs": {"ckpt_name": "Counterfeit-V2.5.safetensors"}
    },
    "5": {
        "class_type": "EmptyLatentImage",
        "inputs": {"batch_size": 1, "height": 768, "width": 512}
    },
    "6": {
        "class_type": "CLIPTextEncode",
        "inputs": {"clip": ["4", 1], "text": positive}
    },
    "7": {
        "class_type": "CLIPTextEncode",
        "inputs": {"clip": ["4", 1], "text": negative}
    },
    "3": {
        "class_type": "KSampler",
        "inputs": {
            "model": ["4", 0],
            "positive": ["6", 0],
            "negative": ["7", 0],
            "latent_image": ["5", 0],
            "seed": 42,
            "steps": 25,
            "cfg": 7.5,
            "sampler_name": "euler_ancestral",
            "scheduler": "normal",
            "denoise": 1
        }
    },
    "8": {
        "class_type": "VAEDecode",
        "inputs": {"samples": ["3", 0], "vae": ["4", 2]}
    },
    "9": {
        "class_type": "SaveImage",
        "inputs": {"images": ["8", 0], "filename_prefix": "tsukuyomi"}
    }
}

print("Submitting workflow...")
resp = requests.post(
    f"{COMFYUI_URL}/prompt",
    json={"prompt": workflow, "client_id": "hermes"},
    timeout=10
)
result = resp.json()
prompt_id = result.get("prompt_id")
print(f"Prompt ID: {prompt_id}")

if not prompt_id:
    print("Error:", result)
    exit(1)

# Poll for completion
print("Generating...")
for i in range(60):
    time.sleep(3)
    history_resp = requests.get(f"{COMFYUI_URL}/history/{prompt_id}", timeout=10)
    history = history_resp.json()
    if prompt_id in history:
        outputs = history[prompt_id].get("outputs", {})
        if "9" in outputs:
            images = outputs["9"].get("images", [])
            if images:
                filename = images[0]["filename"]
                subfolder = images[0].get("subfolder", "")
                print(f"Done! Image: {filename}")
                
                # Download image
                img_url = f"{COMFYUI_URL}/view?filename={filename}&subfolder={subfolder}&type=output"
                img_resp = requests.get(img_url, timeout=30)
                
                local_path = os.path.join(r"C:\Users\Administrator\Desktop", "tsukuyomi.png")
                with open(local_path, "wb") as f:
                    f.write(img_resp.content)
                print(f"Saved to: {local_path}")
                exit(0)
    print(f"  Still generating... ({(i+1)*3}s)")

print("Timed out!")
