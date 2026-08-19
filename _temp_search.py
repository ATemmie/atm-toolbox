import urllib.request

req = urllib.request.Request('https://www.canirun.ai/model/deepseek-r1-1.5b', headers={'User-Agent': 'Mozilla/5.0'})
resp = urllib.request.urlopen(req, timeout=15)
content = resp.read().decode('utf-8', errors='replace')
# Print from 3000 to 8000
print(content[3000:8000])
