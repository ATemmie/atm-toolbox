# -*- coding: utf-8 -*-
"""
ATM 工具箱自动更新流水线
1. Playwright 抓取 opencode.ai Go 官方文档
2. 解析为 go_data.json
3. 与上一版对比，输出"变化摘要"（价格/限额变动）
4. commit + push 到 GitHub Pages 仓库

用法: python update_go.py [--push]
"""
import json, os, re, sys, subprocess, time

BASE = r'C:\Users\Administrator\Desktop\传输\projects\atm-toolbox'
DATA = os.path.join(BASE, 'data', 'go_data.json')
DOCS_TXT = os.path.join(BASE, 'go_docs_full.txt')
GIT_REPO = r'C:\Users\Administrator\Desktop\传输\projects\atm-toolbox'
PROXY = 'http://127.0.0.1:7890'

# ---------- 1. 抓取 ----------
def fetch():
    code = r'''
import sys
from playwright.sync_api import sync_playwright
URL = 'https://opencode.ai/docs/zh-cn/go/'
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, channel='msedge', args=['--no-sandbox'])
    ctx = browser.new_context(viewport={'width': 1280, 'height': 2000},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126.0 Safari/537.36',
        proxy={'server': 'http://127.0.0.1:7890'})
    page = ctx.new_page()
    page.goto(URL, wait_until='networkidle', timeout=60000)
    page.wait_for_timeout(2000)
    text = page.inner_text('body')
    with open(r''' + repr(DOCS_TXT) + r''', 'w', encoding='utf-8') as f:
        f.write(text)
    browser.close()
print('fetched', len(text))
'''
    r = subprocess.run([sys.executable, '-c', code], capture_output=True, text=True, timeout=180,
                       env={**os.environ, 'HTTPS_PROXY': PROXY, 'HTTP_PROXY': PROXY})
    if r.returncode != 0:
        raise RuntimeError(f'抓取失败: {r.stderr[-500:]}')
    print('✔ 抓取完成:', r.stdout.strip())

# ---------- 2. 解析 ----------
def parse_money(s):
    s = s.strip().replace(',', '')
    if s in ('-', '', 'Free'):
        return None
    m = re.search(r'([\d.]+)', s)
    return float(m.group(1)) if m else None

def norm(name):
    return re.sub(r'[\s\-]+', '', name).lower()

def parse():
    with open(DOCS_TXT, encoding='utf-8') as f:
        lines = [l.rstrip() for l in f.readlines()]

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

    price_rows = {}
    i = 0
    while i < len(lines):
        if lines[i].startswith('模型\t') and ('输入' in lines[i] or '输出' in lines[i]):
            i += 1
            while i < len(lines) and lines[i].strip() and '\t' in lines[i]:
                parts = lines[i].split('\t')
                if len(parts) >= 4:
                    name = parts[0].strip()
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

    norm_price = {norm(k): v for k, v in price_rows.items()}
    norm_ep = {norm(k): v for k, v in endpoint_rows.items()}
    norm_pr = {norm(k): v for k, v in privacy_rows.items()}

    models = []
    for name in req_rows:
        n = norm(name)
        models.append({
            'name': name,
            'requests': req_rows.get(name, {}),
            'pricing': norm_price.get(n, {}),
            'endpoint': norm_ep.get(n, {}),
            'privacy': norm_pr.get(n, {}),
        })

    return {
        'source': 'https://opencode.ai/docs/zh-cn/go/',
        'fetched_at': time.strftime('%Y-%m-%d'),
        'plan': {
            'name': 'OpenCode Go',
            'price_first_month_usd': 5,
            'price_monthly_usd': 10,
            'limits_usd': {'per_5h': 12, 'per_week': 30, 'per_month': 60},
            'note': '每月 $10，目标提供 6 倍使用额度。额度以美元价值定义。',
            'exceed_policy': '可在控制台启用"使用余额"，超出后回退到 Zen 余额；否则可继续使用免费模型。',
        },
        'models': models,
    }

# ---------- 3. 对比 ----------
def diff(old, new):
    if not old:
        return ['首次抓取，建立基线']
    changes = []
    old_m = {m['name']: m for m in old.get('models', [])}
    new_m = {m['name']: m for m in new.get('models', [])}
    for name, nm in new_m.items():
        om = old_m.get(name)
        if not om:
            changes.append(f'➕ 新增模型 {name}')
            continue
        # 价格对比（第一档）
        def first_tier(m):
            t = (m.get('pricing') or {}).get('tiers', {})
            return list(t.values())[0] if t else {}
        op, np_ = first_tier(om), first_tier(nm)
        for k in ('input', 'output'):
            o, n = op.get(k), np_.get(k)
            if o != n:
                changes.append(f'⚡ {name} {k}价: {o} → {n}')
        # 请求数对比
        for k in ('per_5h', 'per_month'):
            o = (om.get('requests') or {}).get(k)
            n = (nm.get('requests') or {}).get(k)
            if o != n:
                changes.append(f'⚡ {name} {k}: {o} → {n}')
    for name in old_m:
        if name not in new_m:
            changes.append(f'➖ 移除模型 {name}')
    return changes if changes else ['无变化']

def main():
    push = '--push' in sys.argv
    fetch()
    nd = parse()
    old = None
    if os.path.exists(DATA):
        with open(DATA, encoding='utf-8') as f:
            old = json.load(f)
    changes = diff(old, nd)
    print('--- 变化摘要 ---')
    for c in changes:
        print(' ', c)

    with open(DATA, 'w', encoding='utf-8') as f:
        json.dump(nd, f, ensure_ascii=False, indent=2)
    print(f'✔ 数据已更新: {len(nd["models"])} 模型 -> {DATA}')

    if not push:
        return 0
    env = {**os.environ, 'HTTPS_PROXY': PROXY, 'HTTP_PROXY': PROXY}
    stamp = time.strftime('%Y%m%d_%H%M%S')
    for cmd in [
        ['git', '-C', GIT_REPO, 'add', '-A'],
        ['git', '-C', GIT_REPO, 'commit', '-m', f'auto-update go data {stamp}'],
        ['git', '-C', GIT_REPO, 'push', 'origin', 'main'],
    ]:
        r = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=120)
        if r.returncode != 0 and 'nothing to commit' not in r.stderr:
            print(f'git: {r.stderr[:300]}')
            continue
    print('✔ 已 push')
    return 0

if __name__ == '__main__':
    sys.exit(main())