# ATM 工具箱 (ATM Toolbox)

ATemmie 的个人手机工具箱 - **OpenCode Go 套餐监控** PWA

> iPhone Safari 打开 → "添加到主屏幕" → 像原生 App 一样用 🧰

## 功能（v1.0）

- 📊 **OpenCode Go 套餐监控**：订阅价格、使用限额（5小时/$12、周/$30、月/$60）
- 📋 **全模型价格表**：19 个 Go 模型每 1M tokens 输入/输出价 + 5小时/月请求数额度
- 🔍 搜索 + 排序（按价格/请求数）
- 🔄 自动更新：抓取官方文档 → 解析 → 变动检测 → push

## 使用

打开: https://atemmie.github.io/atm-toolbox/

iPhone: Safari 打开 → 分享 → "添加到主屏幕"

## 开发

```
python update_go.py          # 抓取+解析+对比（不 push）
python update_go.py --push   # 抓取+解析+push 到 GitHub Pages
python -m http.server 8123   # 本地预览
```

数据源: https://opencode.ai/docs/zh-cn/go/ (官方文档)

> 备份注意：数据以官方文档为准，本工具仅供个人参考。