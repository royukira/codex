import subprocess, json, time, os, sys
BIN = os.environ.get('CODEX', '/Applications/ChatGPT.app/Contents/Resources/codex')
PROMPT = "福冈有什么好玩的地方"
cmd = [BIN, "exec", "-m", "gpt-5.6-luna", "-c", 'web_search="live"', "-c", 'features.standalone_web_search=true',
       "-C", "/tmp/codex-ws-test", "--skip-git-repo-check", "--ephemeral",
       "--ignore-user-config", "-s", "read-only", "--json", PROMPT]

t0 = time.time()
p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)
marks = []
for line in p.stdout:
    line = line.strip()
    if not line: continue
    el = time.time() - t0
    try: e = json.loads(line)
    except Exception: 
        print(f"Failed to parse line as JSON: {line}", file=sys.stderr)
        continue
    it = e.get('item') if isinstance(e.get('item'), dict) else {}
    marks.append((el, e.get('type','') + ('/' + it['type'] if it.get('type') else ''), e))
p.wait(timeout=600)

for el, label, _ in marks:
    print(f"{el:8.2f}s  {label}")
ws = [(el, e) for el, l, e in marks if l.endswith('/web_search')]
print(f"ws: {ws}")
if len(ws) >= 2:
    print(f"\n>>> 采集(web.run)耗时: {ws[1][0] - ws[0][0]:.2f}s")
print(f">>> 总墙上时间: {time.time()-t0:.2f}s")
