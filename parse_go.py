# -*- coding: utf-8 -*-
"""
解析 opencode Go docs 文本 → 结构化 JSON 数据源
输入: go_docs_full.txt (Playwright 抓取)
输出: data/go_data.json
"""
import json, re, os

SRC = r'C:\Users\Administrator\Desktop\传输\projects\atm-toolbox\go_docs_full.txt'
OUT_DIR = r'C:\Users\Administrator\Desktop\传输\projects\atm-toolbox\data'
os.makedirs(OUT_DIR, exist_ok=True)

with open(SRC, encoding='utf-8') as f:
    lines = [l.rstrip() for l in f.readlines()]

# ---- 解析使用限制请求数表（MODEL / 每5小时 / 每周 / 每月）----
req_rows = {}
i = 0
while i < len(lines):
    if lines[i].startswith('MODEL\t') or '每 5 小时请求数' in lines[i]:
        i += 1
        while i < len(lines) and lines[i].strip() and '\t' in lines[i]:
            parts = lines[i].split('\t')
            if len(parts) >= 4:
                req_rows[parts[0].strip()] = {
                    'per_5h': int(parts[1].replace(',', '')),
                    'per_week': int(parts[2].replace(',', '')),
                    'per_month': int(parts[3].replace(',', '')),
                }
            i += 1
        break
    i += 1

# ---- 解析价格表（模型/输入/输出/缓存读取/缓存写入/使用额度）----
price_rows = {}
i = 0
while i < len(lines):
    if lines[i].startswith('模型\t') and ('输入' in lines[i] or '输出' in lines[i]):
        i += 1
        while i < len(lines) and lines[i].strip() and '\t' in lines[i]:
            parts = lines[i].split('\t')
            if len(parts) >= 5:
                name = parts[0].strip()
                price_rows[name] = {
                    'input': parts[1].strip(),
                    'output': parts[2].strip(),
                    'cache_read': parts[3].strip(),
                    'cache_write': parts[4].strip() if len(parts) > 4 and parts[4].strip() else None,
                    'quota_usd': parts[5].strip() if len(parts) > 5 and parts[5].strip() else None,
                }
            i += 1
        break
    i += 1

# ---- 解析端点表（模型 / 模型ID / 端点 / SDK）----
endpoint_rows = {}
i = 0
while i < len(lines):
    if lines[i].startswith('模型\t') and '模型 ID' in lines[i]:
        i += 1
        while i < len(lines) and lines[i].strip() and '\t' in lines[i]:
            parts = lines[i].split('\t')
            if len(parts) >= 3:
                endpoint_rows[parts[0].strip()] = {
                    'model_id': parts[1].strip(),
                    'endpoint': parts[2].strip(),
                }
            i += 1
        break
    i += 1

# ---- 解析隐私表（模型/模型训练/数据留存）----
privacy_rows = {}
i = 0
while i < len(lines):
    if lines[i].startswith('模型\t') and '数据留存' in lines[i]:
        i += 1
        while i < len(lines) and lines[i].strip() and '\t' in lines[i]:
            parts = lines[i].split('\t')
            if len(parts) >= 3:
                privacy_rows[parts[0].strip()] = {
                    'training': parts[1].strip(),
                    'retention': parts[2].strip(),
                }
            i += 1
        break
    i += 1

data = {
    'source': 'https://opencode.ai/docs/zh-cn/go/',
    'fetched_at': '2026-08-17',
    'plan': {
        'name': 'OpenCode Go',
        'price_first_month_usd': 5,
        'price_monthly_usd': 10,
        'limits_usd': {'per_5h': 12, 'per_week': 30, 'per_month': 60},
        'note': '每月 $10，目标提供 6 倍使用额度。额度以美元价值定义。',
        'exceed_policy': '可在控制台启用"使用余额"，超出后回退到 Zen 余额；否则可继续使用免费模型。',
    },
    'models': [],
}

for name in req_rows:
    m = {
        'name': name,
        'requests': req_rows.get(name, {}),
        'pricing': price_rows.get(name, {}),
        'endpoint': endpoint_rows.get(name, {}),
        'privacy': privacy_rows.get(name, {}),
    }
    data['models'].append(m)

out = os.path.join(OUT_DIR, 'go_data.json')
with open(out, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(f"OK: {len(data['models'])} 个模型 -> {out}")
for m in data['models']:
    r = m['requests']
    p = m['pricing']
    print(f"  {m['name']:22s} 5h={r.get('per_5h'):>6,}  in={p.get('input','?'):>7s}  out={p.get('output','?'):>7s}  quota=${p.get('quota_usd','-')}")