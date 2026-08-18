# -*- coding: utf-8 -*-
"""生成工具箱用的用量摘要 JSON（从 ws_usage.json 提取占比/余额/明细）
输出: data/go_usage_summary.json（页面读取）
"""
import json, os, re, time

BASE = r'C:\Users\Administrator\Desktop\传输\projects\atm-toolbox'
SRC = os.path.join(BASE, 'data', 'ws_usage.json')
OUT = os.path.join(BASE, 'data', 'go_usage_summary.json')

try:
    with open(SRC, encoding='utf-8') as f:
        raw = json.load(f)
except Exception as e:
    print(f"读取失败: {e}")
    raise SystemExit(1)

# tabs 结构: raw['tabs']['使用量'/'计费'/'go 页面']
text_usage = raw.get('tabs', {}).get('使用量', '') or raw.get('text', '')
text_billing = raw.get('tabs', {}).get('计费', '')
text_go = raw.get('text', '')

summary = {
    'fetched_at': raw.get('fetched_at') or time.strftime('%Y-%m-%d %H:%M:%S'),
    'source': 'workspace console',
}

def extract_pct(text, label):
    m = re.search(label + r'\s*([\d.]+)\s*%', text)
    return float(m.group(1)) if m else None

def extract_reset(text, label):
    # 匹配 "重置于 XXX" 直到下一个标签/换行边界
    m = re.search(label + r'\s*[\d.]+\s*%\s*重置于\s*([\d\s\w小时分钟天]+?)(?=\n|$|\s*[^\d\s\w小时分钟天])', text)
    return m.group(1).strip() if m else None

# 占比（看 go 页面文本）
go_src = os.path.join(BASE, 'data', 'ws_go_page.json')
go_text = ''
try:
    with open(go_src, encoding='utf-8') as gf:
        go_text = json.load(gf).get('text', '')
except Exception:
    pass

for t in [go_text, text_go, text_usage]:
    if not t:
        continue
    rp = extract_pct(t, '滚动用量')
    if rp is not None:
        summary['rolling_pct'] = rp
        summary['rolling_reset'] = extract_reset(t, '滚动用量')
    wp = extract_pct(t, '每周用量')
    if wp is not None:
        summary['weekly_pct'] = wp
        summary['weekly_reset'] = extract_reset(t, '每周用量')
    mp = extract_pct(t, '每月用量')
    if mp is not None:
        summary['monthly_pct'] = mp
        summary['monthly_reset'] = extract_reset(t, '每月用量')
    break  # 只取第一个有数据的

# 余额
m = re.search(r'当前余额\s*\$?([\d.]+)', text_usage + text_billing)
if m:
    summary['balance_usd'] = float(m.group(1))

# 支付历史
m = re.search(r'支付 ID\s*(\S+)\s*\$?([\d.]+)', text_billing)
if m:
    summary['last_payment'] = {'id': m.group(1), 'amount_usd': float(m.group(2))}

# 使用历史明细（深挖每笔）
rows = re.findall(r'(\d+月\d+日\s*\S*)\t([\w.-]+)\t\n(\d+)\n\t\n(\d+)\n\tGo \(\$([\d.]+)\)', text_usage)
if rows:
    summary['recent_sessions'] = len(rows)
    total = sum(float(r[4]) for r in rows)
    summary['recent_total_cost_usd'] = round(total, 4)
    by_model = {}
    for r in rows:
        model = r[1]
        by_model.setdefault(model, {'sessions': 0, 'cost_usd': 0.0})
        by_model[model]['sessions'] += 1
        by_model[model]['cost_usd'] = round(by_model[model]['cost_usd'] + float(r[4]), 4)
    summary['by_model'] = by_model

with open(OUT, 'w', encoding='utf-8') as f:
    json.dump(summary, f, ensure_ascii=False, indent=2)
print("✔ 生成:", json.dumps(summary, ensure_ascii=False, indent=2)[:1200])