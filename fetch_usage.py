# -*- coding: utf-8 -*-
"""
OpenCode 控制台用量抓取脚本
读 console_cookies.json（登录助手保存的会话）→ 调 /console/api/v1/usage/export → 存 usage_data.json
用法: python fetch_usage.py [--push]
"""
import json, os, sys, time, subprocess, urllib.request

BASE = r'C:\Users\Administrator\Desktop\传输\projects\atm-toolbox'
COOKIE_FILE = os.path.join(BASE, 'data', 'console_cookies.json')
USAGE_FILE = os.path.join(BASE, 'data', 'usage_data.json')
PROXY = 'http://127.0.0.1:7890'
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'

def load_cookies():
    if not os.path.exists(COOKIE_FILE):
        return None
    with open(COOKIE_FILE, encoding='utf-8') as f:
        return json.load(f)

def cookie_header(cookies):
    parts = []
    for c in cookies:
        if c.get('name') and c.get('value'):
            parts.append(f"{c['name']}={c['value']}")
    return '; '.join(parts)

def get(path, cookies, method='GET', payload=None):
    url = 'https://opencode.ai' + path
    data = json.dumps(payload).encode() if payload else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header('User-Agent', UA)
    req.add_header('Accept', 'application/json')
    req.add_header('Origin', 'https://opencode.ai')
    req.add_header('Referer', 'https://opencode.ai/console')
    req.add_header('Cookie', cookie_header(cookies))
    if payload:
        req.add_header('Content-Type', 'application/json')
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({'http': PROXY, 'https': PROXY}))
    try:
        r = opener.open(req, timeout=20)
        return r.status, r.read().decode('utf-8', 'ignore')
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8', 'ignore')

def main():
    push = '--push' in sys.argv
    cookies = load_cookies()
    if not cookies:
        print('❌ 未找到登录会话。请先在电脑旁运行: python login_console.py 完成一次登录')
        return 2

    results = {}
    # 1) usage export
    st, body = get('/console/api/v1/usage/export', cookies)
    print(f"usage/export -> {st}")
    if st == 200:
        try:
            results['usage'] = json.loads(body)
            print(json.dumps(results['usage'], ensure_ascii=False)[:800])
        except Exception:
            results['usage_raw'] = body[:2000]
    else:
        print(f"  body: {body[:200]}")
        if st == 401:
            print('⚠️ 会话过期，需要重新登录 (login_console.py)')
            return 3

    # 2) usage 摘要端点
    for p in ['/console/api/usage', '/console/api/billing']:
        st, body = get(p, cookies)
        print(f"{p} -> {st}")
        if st == 200:
            try:
                results[p.split('/')[-1]] = json.loads(body)
                print(json.dumps(results[p.split('/')[-1]], ensure_ascii=False)[:500])
            except Exception:
                pass

    # 3) 试试无 v1 前缀的 export 相关
    st, body = get('/console/api/v1/usage/export', cookies, method='POST', payload={'format': 'json'})
    print(f"usage/export POST -> {st}: {body[:200]}")

    results['fetched_at'] = time.strftime('%Y-%m-%d %H:%M:%S')
    with open(USAGE_FILE, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n✔ 已保存 -> {USAGE_FILE}")

    if push and os.path.exists(r'C:\Users\Administrator\Desktop\传输\projects\atm-toolbox\.git'):
        env = {**os.environ, 'HTTPS_PROXY': PROXY, 'HTTP_PROXY': PROXY}
        repo = BASE
        for cmd in [
            ['git', '-C', repo, 'add', '-A'],
            ['git', '-C', repo, 'commit', '-m', f'usage update {time.strftime("%Y%m%d_%H%M%S")}'],
            ['git', '-C', repo, 'push', 'origin', 'main'],
        ]:
            r = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=120)
            if r.returncode != 0 and 'nothing to commit' not in r.stderr:
                print(f'git: {r.stderr[:200]}')
    return 0

if __name__ == '__main__':
    sys.exit(main())