# -*- coding: utf-8 -*-
"""完整拉取用量数据：summary + 30d 明细 + 月度数据 → data/go_usage.json
用法: python fetch_usage2.py [--push]
"""
import json, os, sys, time, subprocess, urllib.request, urllib.error

BASE = r'C:\Users\Administrator\Desktop\传输\projects\atm-toolbox'
COOKIE_FILE = BASE + r'\data\console_cookies.json'
OUT = BASE + r'\data\go_usage.json'
ORG = 'org_01M0A41EXB0YVXZ5A05Q7P1SGN'

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'
op = urllib.request.build_opener(urllib.request.ProxyHandler(
    {'http': 'http://127.0.0.1:7890', 'https': 'http://127.0.0.1:7890'}))

def load_cookies():
    if not os.path.exists(COOKIE_FILE):
        return None
    return json.load(open(COOKIE_FILE, encoding='utf-8'))

def get(path, ch=None, timeout=30):
    req = urllib.request.Request('https://opencode.ai' + path)
    req.add_header('User-Agent', UA)
    req.add_header('Accept', 'application/json, text/csv, */*')
    req.add_header('Origin', 'https://opencode.ai')
    req.add_header('Referer', 'https://opencode.ai/console/' + ORG)
    req.add_header('Cookie', ch)
    req.add_header('x-org-id', ORG)
    try:
        r = op.open(req, timeout=timeout)
        return r.status, r.read().decode('utf-8', 'ignore')
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8', 'ignore')
    except Exception as e:
        return -1, str(e)

def main():
    push = '--push' in sys.argv
    cookies = load_cookies()
    if not cookies:
        print('❌ 未找到登录会话，请先运行 login_console.py 登录')
        return 2
    ch = '; '.join(f"{c['name']}={c['value']}" for c in cookies if c.get('name'))

    results = {'fetched_at': time.strftime('%Y-%m-%d %H:%M:%S'), 'org_id': ORG}

    # 1. 汇总
    st, body = get('/console/api/usage/summary', ch)
    print(f"summary -> {st}: {body[:200]}")
    if st == 200:
        try:
            results['summary'] = json.loads(body)
        except Exception:
            results['summary_raw'] = body

    # 2. 30 天明细 CSV
    st, body = get('/console/api/usage/export?range=30d', ch, timeout=60)
    print(f"export 30d -> {st}: {len(body)} bytes")
    if st == 200:
        results['export_30d'] = body[:50000]

    # 3. 7 天
    st, body = get('/console/api/usage/export?range=7d', ch, timeout=60)
    print(f"export 7d -> {st}: {len(body)} bytes")
    if st == 200:
        results['export_7d'] = body[:50000]

    # 4. 常见范围汇总对比
    for rng in ['week', 'month']:
        st, body = get(f'/console/api/usage/export?range={rng}', ch, timeout=60)
        print(f"export {rng} -> {st}: {len(body)} bytes")
        if st == 200:
            results[f'export_{rng}'] = body[:50000]

    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n✔ 已保存 -> {OUT} ({os.path.getsize(OUT)} bytes)")

    # 简单汇总展示
    s = results.get('summary', {})
    if s:
        total_cost_dollar = int(s.get('totalCostMicroCents', 0)) / 1e6
        print(f"\n📊 用量汇总: 请求 {int(s.get('totalRequests', 0)):,} 次 | 输入 {int(s.get('totalInputTokens', 0)):,} tok | 输出 {int(s.get('totalOutputTokens', 0)):,} tok | 总花费 ${total_cost_dollar:.4f}")

    if push:
        env = {**os.environ, 'HTTPS_PROXY': 'http://127.0.0.1:7890', 'HTTP_PROXY': 'http://127.0.0.1:7890'}
        for cmd in [
            ['git', '-C', BASE, 'add', '-A'],
            ['git', '-C', BASE, 'commit', '-m', f'usage update {time.strftime("%Y%m%d_%H%M%S")}'],
            ['git', '-C', BASE, 'push', 'origin', 'main'],
        ]:
            r = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=120)
            if r.returncode != 0 and 'nothing to commit' not in r.stderr:
                print(f'git: {r.stderr[:150]}')
        print('✔ 已 push')
    return 0

if __name__ == '__main__':
    sys.exit(main())