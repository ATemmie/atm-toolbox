import urllib.request, json

# Get model info from HF for DeepSeek R1 1.5B
url = 'https://huggingface.co/api/models/deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B'
try:
    data = json.loads(urllib.request.urlopen(url, timeout=15).read())
    print(f"Model: {data.get('modelId', 'N/A')}")
    print(f"Downloads: {data.get('downloads', 'N/A')}")
    print(f"Likes: {data.get('likes', 'N/A')}")
    print(f"Tags: {data.get('tags', [])[:10]}")
    print(f"Pipeline tag: {data.get('pipeline_tag', 'N/A')}")
    print(f"Library name: {data.get('library_name', 'N/A')}")
    print(f"Safetensors: {data.get('safetensors', {})}")
except Exception as e:
    print(f"Error: {e}")

# Get GGUF files for the main repo
print("\n--- GGUF files (unsloth) ---")
url2 = 'https://huggingface.co/api/models/unsloth/DeepSeek-R1-Distill-Qwen-1.5B-GGUF/tree/main?recursive=true'
try:
    data2 = json.loads(urllib.request.urlopen(url2, timeout=15).read())
    for f in data2:
        if f['type'] == 'file' and f['path'].endswith('.gguf'):
            print(f"  {f['path']} - {f['size']/1024/1024:.1f} MB")
except Exception as e:
    print(f"Error: {e}")
