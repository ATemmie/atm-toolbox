# Krea 2 Turbo FP8 工作流使用指南

## 已安装的工作流

### 1. krea2_turbo_t2i.json (官方完整版)
- **用途**: 文生图（Text-to-Image）
- **特性**: 包含完整的节点编辑器界面、说明文档、多模型选项
- **如何使用**: 
  1. 打开 ComfyUI Desktop（游戏本）
  2. 点击菜单 → Open Workflow → 选择 `krea2_turbo_t2i.json`
  3. 在节点编辑器中修改 prompt、参数
  4. 点击 Queue Prompt 生成

### 2. krea2_turbo_simple_api.json (简化版 - 已验证可用)
- **用途**: 最简生图流程（9个节点，无多余配置）
- **特性**: 直接可用，已通过 API 测试验证
- **节点说明**:
  - Load Diffusion Model: `krea2_turbo_fp8_scaled.safetensors`
  - Load CLIP: `qwen3vl_4b_fp8_scaled.safetensors` (type: krea2)
  - CLIP Text Encode ×2: 正面/负面 prompt
  - Empty Latent Image: 1024×1024
  - KSampler: steps=8, cfg=1.0, euler, simple
  - VAELoader: `qwen_image_vae.safetensors`
  - VAEDecode → SaveImage

## 快速开始

### 方法一：通过 ComfyUI UI（推荐）
1. 游戏本上打开 **Comfy Desktop**（D:\app\Comfy Desktop\）
2. 等待加载完成（约10-15秒）
3. 点击顶部菜单 → **Open** → 选择工作流文件
4. 修改 prompt 文本
5. 点击 **Queue Prompt** 开始生成

### 方法二：通过 API（适合批量/自动化）
```powershell
# 在游戏本上运行
$raw = Get-Content "D:\Comfy-Desktop\ComfyUI-Installs\Krea-2-Turbo\ComfyUI\user\default\workflows\krea2_turbo_simple_api.json" -Raw
$payload = "{`"prompt`": $raw}"
# ... 提交到 http://127.0.0.1:8188/api/prompt
```

## 参数说明

| 参数 | 推荐值 | 说明 |
|------|--------|------|
| Steps | 8 | Krea 2 Turbo 优化为 8 步 |
| CFG | 1.0 | 官方推荐 |
| Sampler | euler | |
| Scheduler | simple | |
| Resolution | 1024×1024 | 可改为其他比例 |
| Prompt | 你想要的内容 | 英文效果最佳 |

## 模型文件位置

所有模型在: `D:\Comfy-Desktop\ComfyUI-Shared\models\`
- `diffusion_models\krea2_turbo_fp8_scaled.safetensors` (12.24 GB)
- `text_encoders\qwen3vl_4b_fp8_scaled.safetensors` (4.88 GB)
- `vae\qwen_image_vae.safetensors` (242 MB)

## 性能参考

- **RTX 5070 Ti (12GB VRAM)**: 1024×1024 约 10-20 秒
- **首次加载**: 模型需加载到显存，约 30-60 秒
- **后续生成**: 模型已缓存，约 8-15 秒

## 注意事项

1. 首次运行会加载模型到显存，稍等片刻
2. 生成的图片保存在: `D:\Comfy-Desktop\ComfyUI-Shared\output\`
3. 工作流使用官方节点，无需安装额外 custom nodes
4. 如遇显存不足，可降低分辨率到 768×768