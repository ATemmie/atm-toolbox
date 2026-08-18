# -*- coding: utf-8 -*-
"""创建语音桥专用 webhook.site 邮箱 + 密钥"""
import urllib.request, json, base64, os

def post(url, data=None, headers=None):
    body = json.dumps(data).encode() if data is not None else None
    req = urllib.request.Request(url, data=body, method='POST' if data is not None else 'GET')
    req.add_header('User-Agent', 'hermes-voice-bridge')
    req.add_header('Accept', 'application/json')
    if body:
        req.add_header('Content-Type', 'application/json')
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode())

tok = post('https://webhook.site/token')
print("uuid:", tok['uuid'])
print("expires:", tok.get('expires_at', '?'))

key = base64.b64encode(os.urandom(32)).decode()
print("secret_b64:", key)

cfg = {
    'webhook_uuid': tok['uuid'],
    'secret_b64': key,
    'deliver': 'qqbot:9AD7BD464F622584A4ADBE96F6B3922A',
}
with open(r'C:\hermes\voice-bridge\config.json', 'w', encoding='utf-8') as f:
    json.dump(cfg, f, ensure_ascii=False, indent=2)
print("config 已保存")