# -*- coding: utf-8 -*-
"""把 go_usage.json 也做成公开数据，供工具箱页面展示（从 go_usage.json 提取摘要）"""
import json, os, time, sys

BASE = r'C:\Users\Administrator\Desktop\传输\projects\atm-toolbox'
SRC = os.path.join(BASE, 'data', 'go_usage.json')
OUT = os.path.join(BASE, 'data', 'go_usage_summary.json')

with open(SRC, encoding='utf-8') as f:
    raw = json.load(f)

s = raw.get('summary', {})
summary = {
    'fetched_at': raw.get('fetched_at', ''),
    'totalRequests': int(s.get('totalRequests', 0) or 0),
    'totalInputTokens': int(s.get('totalInputTokens', 0) or 0),
    'totalOutputTokens': int(s.get('totalOutputTokens', 0) or 0),
    'totalCacheReadTokens': int(s.get('totalCacheReadTokens', 0) or 0),
    'totalCostUsd': round(int(s.get('totalCostMicroCents', 0) or 0) / 1e6, 6),
}

# 解析 CSV 明细 → 按模型聚合
def parse_csv(csv_text):
    if not csv_text:
        return []
    lines = csv_text.strip().split('\n')
    if len(lines) < 2:
        return []
    header = lines[0].split(',')
    rows = []
    for ln in lines[1:]:
        cells = ln.split(',')
        if len(cells) >= len(header):
            row = dict(zip(header, cells))
            rows.append(row)
    return rows

rows30 = parse_csv(raw.get('export_30d', ''))
rows7 = parse_csv(raw.get('export_7d', ''))

def agg(rows):
    by_model = {}
    total_cost = 0
    total_in = 0
    total_out = 0
    for r in rows:
        m = r.get('model', 'unknown')
        if m not in by_model:
            by_model[m] = {'requests': 0, 'input_tokens': 0, 'output_tokens': 0, 'cost_usd': 0.0}
        by_model[m]['requests'] += 1
        by_model[m]['input_tokens'] += int(r.get('input_tokens', 0) or 0)
        by_model[m]['output_tokens'] += int(r.get('output_tokens', 0) or 0)
        cost = int(r.get('cost_micro_cents', 0) or 0) / 1e6
        by_model[m]['cost_usd'] += cost
        total_cost += cost
        total_in += int(r.get('input_tokens', 0) or 0)
        total_out += int(r.get('output_tokens', 0) or 0)
    return by_model, total_cost, total_in, total_out

b30, c30, i30, o30 = agg(rows30)
b7, c7, i7, o7 = agg(rows7)

summary['detail_30d'] = {
    'requests': len(rows30),
    'totalCostUsd': round(c30, 6),
    'inputTokens': i30,
    'outputTokens': o30,
    'by_model': {k: {**v, 'cost_usd': round(v['cost_usd'], 6)} for k, v in b30.items()},
}
summary['detail_7d'] = {
    'requests': len(rows7),
    'totalCostUsd': round(c7, 6),
    'inputTokens': i7,
    'outputTokens': o7,
}

with open(OUT, 'w', encoding='utf-8') as f:
    json.dump(summary, f, ensure_ascii=False, indent=2)
print(f"✔ 摘要已生成 -> {OUT}")
print(json.dumps(summary, ensure_ascii=False, indent=2)[:1000])