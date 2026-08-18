# -*- coding: utf-8 -*-
"""
解析 opencode Go docs 文本 → 结构化 JSON 数据源 v2
支持分档价格 (≤ 272K / > 272K / Off-Peak / Peak)
输入: go_docs_full.txt (Playwright 抓取)
输出: data/go_data.json
"""
import json, os, re

SRC = r'C:\Users\Administrator\Desktop\传输\projects\atm-toolbox\go_docs_full.txt'
OUT_DIR = r'C:\Users\Administrator\Desktop\传输\projects\atm-toolbox\data'
os.makedirs(OUT_DIR, exist_ok=True)

def parse_money(s):
    """'$1.40' → 1.4 ; '$0.07' → 0.07 ; '-' → None"""
    s = s.strip().replace(',', '')
    if s in ('-', '', 'Free'):
        return None
    m = re.search(r'([\d.]+)', s)
    return float(m.group(1)) if m else None

def fmt_price(v):
    if v is None:
        return 'Free' if False else None
    return f'${v:g}'

with open(SRC, encoding='utf-8') as f:
    lines = [l.rstrip() for l in f.readlines()]

# ---------- 1. 请求数表 ----------
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

# ---------- 2. 价格表（支持分档行） ----------
price_rows = {}   # name -> {tiers: [{label, input, output, cache_read, cache_write, quota}], quotas: [..]}
i = 0
while i < len(lines):
    if lines[i].startswith('模型\t') and ('输入' in lines[i] or '输出' in lines[i]):
        i += 1
        while i < len(lines) and lines[i].strip() and '\t' in lines[i]:
            parts = lines[i].split('\t')
            if len(parts) >= 4:
                name = parts[0].strip()
                # 提取分档标签 (≤ 272K tokens) / (> 272K tokens) / (Off-Peak) / (Peak)
                m = re.search(r'\(([^)]+)\)\s*$', name)
                base = re.sub(r'\s*\([^)]+\)\s*$', '', name).strip()
                tier_label = m.group(1) if m else '默认'
                rec = {
                    'input': parse_money(parts[1]),
                    'output': parse_money(parts[2]),
                    'cache_read': parse_money(parts[3]),
                    'cache_write': parse_money(parts[4]) if len(parts) > 4 else None,
                    'quota': parse_money(parts[5]) if len(parts) > 5 else None,
                }
                if base not in price_rows:
                    price_rows[base] = {'tiers': {}}
                price_rows[base]['tiers'][tier_label] = rec
            i += 1
        break
    i += 1

# ---------- 3. 端点表 ----------
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

# ---------- 4. 隐私表 ----------
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

def norm(name):
    """归一化模型名：MiMo-V2.5 == MiMo V2.5"""
    return re.sub(r'[\s\-]+', '', name).lower()

# ---------- 组装配对 ----------
# 价格表/端点表/隐私表 名称可能与请求表不同（MiMo V2.5 vs MiMo-V2.5）
norm_price = {norm(k): v for k, v in price_rows.items()}
norm_ep = {norm(k): v for k, v in endpoint_rows.items()}
norm_pr = {norm(k): v for k, v in privacy_rows.items()}
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
    n = norm(name)
    m = {
        'name': name,
        'requests': req_rows.get(name, {}),
        'pricing': norm_price.get(n, {}),
        'endpoint': norm_ep.get(n, {}),
        'privacy': norm_pr.get(n, {}),
    }
    data['models'].append(m)

out = os.path.join(OUT_DIR, 'go_data.json')
with open(out, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(f"OK: {len(data['models'])} 个模型 -> {out}")

for m in data['models']:
    r = m['requests']
    tiers = m['pricing'].get('tiers', {})
    first = list(tiers.values())[0] if tiers else {}
    labels = '/'.join(tiers.keys())
    inp = first.get('input')
    outp = first.get('output')
    quota = first.get('quota')
    print(f"  {m['name']:22s} 5h={r.get('per_5h'):>6,}  in={fmt_price(inp) or '-':>7s}  out={fmt_price(outp) or '-':>7s}  q=${quota or '-'}  [{labels}]")