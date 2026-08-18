# -*- coding: utf-8 -*-
"""
ATM 工具箱 cron 总入口 v2
- 每 3 分钟: 用 Edge CDP 抓 workspace/go 用量 → 生成摘要 → push
- 每天 10 点: 抓官方价格 → push（有变动才通知）
用法: python auto_update_v2.py usage|price|all [--notify]
成功时静默（cron no_agent 模式下空 stdout = 不推送，避免刷屏）；
失败时输出错误 → 会作为告警推送给用户。
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
        # 1. 检查 Edge CDP 是否存活，不存活则尝试拉起（复制 profile + 调试端口）
        try:
            import urllib.request
            r = urllib.request.urlopen('http://127.0.0.1:9223/json', timeout=5)
            cdp_alive = r.status == 200
        except Exception:
            cdp_alive = False
        if not cdp_alive:
            print('Edge CDP 未运行，尝试启动…')
            import subprocess as sp
            edge = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
            if not os.path.exists(edge):
                edge = r'C:\Program Files\Microsoft\Edge\Application\msedge.exe'
            profile = r'C:\Users\Administrator\AppData\Local\Microsoft\Edge\User Data Copy'
            if not os.path.exists(profile):
                # 从默认 profile 复制一份（保留登录态）
                src = r'C:\Users\Administrator\AppData\Local\Microsoft\Edge\User Data\Default'
                os.makedirs(profile + r'\Default', exist_ok=True)
                for item in os.listdir(src):
                    s = os.path.join(src, item)
                    d = os.path.join(profile + r'\Default', item)
                    try:
                        if os.path.isdir(s):
                            import shutil
                            if not os.path.exists(d):
                                shutil.copytree(s, d)
                        else:
                            if not os.path.exists(d):
                                shutil.copy2(s, d)
                    except Exception:
                        pass
            sp.Popen([edge, '--remote-debugging-port=9223',
                      f'--user-data-dir={profile}',
                      '--no-first-run', '--no-default-browser-check',
                      'https://opencode.ai/workspace/wrk_01KYD365FD37BNQMKJGEG16M1C/go'],
                     creationflags=0x08000000)  # CREATE_NO_WINDOW
            time.sleep(12)
            try:
                r = urllib.request.urlopen('http://127.0.0.1:9223/json', timeout=5)
                cdp_alive = r.status == 200
                if cdp_alive:
                    print('CDP 启动成功')
            except Exception:
                cdp_alive = False
        if cdp_alive:
            # 抓取失败自动重试（最多 3 次），不静默吃旧数据
            rc, out, err = 1, '', ''
            for attempt in range(1, 4):
                rc, out, err = run('cdp_go_page.py', [])
                if rc == 0:
                    break
                time.sleep(8)
            if rc != 0:
                # 失败：输出错误 → cron no_agent 会作为告警推送
                print(f'❌ 用量抓取失败（3 次重试均失败）: {err[:300]}')
            else:
                rc2, out2, err2 = run('make_ws_summary.py', [])
                push_err = push(f'usage auto {time.strftime("%Y%m%d_%H%M%S")}')
                if push_err:
                    print(f'⚠️ 用量数据已抓取但推送失败: {push_err}')
        else:
            print('⚠️ Edge CDP 仍不可用 — 可能需要手动登录 opencode 一次')

    if mode in ('price', 'all'):
        rc, out, err = run('update_go.py', ['--push', '--quiet'], timeout=300)
        if rc != 0:
            print(f'⚠️ 价格更新失败 rc={rc}: {err[:200]}')

    if notify:
        # 只输出有意义的变动（价格变动时 update_go.py 会输出）
        pass
    return 0

if __name__ == '__main__':
    sys.exit(main())