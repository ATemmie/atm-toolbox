# -*- coding: utf-8 -*-
"""
ATM 工具箱 cron 总入口 v2
- 每 30 分钟: 用 Edge CDP 抓 workspace/go 用量 → 生成摘要 → push
- 每天 10 点: 抓官方价格 → push（有变动才通知）
用法: python auto_update_v2.py usage|price|all [--notify]
"""
import subprocess, sys, os, time

BASE = r'C:\Users\Administrator\Desktop\传输\projects\atm-toolbox'
PY = sys.executable
PROXY = 'http://127.0.0.1:7890'

def run(script, args, timeout=300):
    env = {**os.environ, 'HTTPS_PROXY': PROXY, 'HTTP_PROXY': PROXY}
    r = subprocess.run([PY, os.path.join(BASE, script), *args],
                       capture_output=True, text=True, env=env, timeout=timeout)
    return r.returncode, r.stdout.strip(), r.stderr.strip()

def push(msg):
    env = {**os.environ, 'HTTPS_PROXY': PROXY, 'HTTP_PROXY': PROXY}
    for cmd in [
        ['git', '-C', BASE, 'add', '-A'],
        ['git', '-C', BASE, 'commit', '-m', msg],
        ['git', '-C', BASE, 'push', 'origin', 'main'],
    ]:
        r = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=120)
        if r.returncode != 0 and 'nothing to commit' not in r.stderr:
            return r.stderr[:200]
    return None

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'all'
    notify = '--notify' in sys.argv
    changes = []

    if mode in ('usage', 'all'):
        # 1. 检查 Edge CDP 是否存活，不存活就跳过并提示（需用户登录态）
        try:
            import urllib.request
            r = urllib.request.urlopen('http://127.0.0.1:9223/json', timeout=5)
            cdp_alive = r.status == 200
        except Exception:
            cdp_alive = False
        if cdp_alive:
            rc, out, err = run('cdp_go_page.py', [])
            rc2, out2, err2 = run('make_ws_summary.py', [])
            push_err = push(f'usage auto {time.strftime("%Y%m%d_%H%M%S")}')
            if push_err:
                print(f'push: {push_err}')
            print(f'usage: rc={rc}/{rc2}')
        else:
            print('⚠️ Edge CDP 未运行 (9223) — 跳过用量抓取。启动: msedge --remote-debugging-port=9223 --user-data-dir=...')

    if mode in ('price', 'all'):
        rc, out, err = run('update_go.py', ['--push', '--quiet'], timeout=300)
        print(f'price: rc={rc}')

    if notify:
        # 只输出有意义的变动（价格变动时 update_go.py 会输出）
        pass
    return 0

if __name__ == '__main__':
    sys.exit(main())