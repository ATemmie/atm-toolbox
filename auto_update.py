# -*- coding: utf-8 -*-
"""
ATM 工具箱总更新脚本（cron 用）
1. 用量：每 30 分钟 - fetch_usage2.py --push（个人用量）
2. 价格：每天 - update_go.py --quiet --push（公开价格，有变动才通知）
用法: python auto_update.py usage|price|all [--notify]
"""
import subprocess, sys, os, time, json

BASE = r'C:\Users\Administrator\Desktop\传输\projects\atm-toolbox'
PY = sys.executable

def run(name, args, quiet=False):
    env = {**os.environ, 'HTTPS_PROXY': 'http://127.0.0.1:7890', 'HTTP_PROXY': 'http://127.0.0.1:7890'}
    r = subprocess.run([PY, os.path.join(BASE, args[0]), *args[1:]], capture_output=True, text=True, env=env, timeout=300)
    out = r.stdout.strip()
    if not quiet:
        if out: print(out[:800])
        if r.stderr.strip(): print('STDERR:', r.stderr.strip()[:400])
    return r.returncode, out

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'all'
    notify = '--notify' in sys.argv
    out = []

    if mode in ('usage', 'all'):
        rc, o = run('usage', ['fetch_usage2.py'])
        # 生成摘要供页面展示
        rc2, o2 = run('summary', ['make_usage_summary.py'], quiet=True)
        # 推送 JSON
        env = {**os.environ, 'HTTPS_PROXY': 'http://127.0.0.1:7890', 'HTTP_PROXY': 'http://127.0.0.1:7890'}
        stamp = time.strftime('%Y%m%d_%H%M%S')
        for cmd in [
            ['git', '-C', BASE, 'add', '-A'],
            ['git', '-C', BASE, 'commit', '-m', f'usage auto {stamp}'],
            ['git', '-C', BASE, 'push', 'origin', 'main'],
        ]:
            r = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=120)
            if r.returncode != 0 and 'nothing to commit' not in r.stderr:
                print(f'git: {r.stderr[:150]}')
        out.append(f"usage: rc={rc}")

    if mode in ('price', 'all'):
        rc, o = run('price', ['update_go.py', '--push', '--quiet'], quiet=True)
        out.append(f"price: rc={rc}")

    # 通知（只有有内容才输出，cron 静默规则）
    if notify and any('changed' in x or '变动' in x for x in out):
        print('⚠️ 套餐数据有变动！')
        for x in out: print(x)
    return 0

if __name__ == '__main__':
    sys.exit(main())