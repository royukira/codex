import json, sys, uuid, time, urllib.request, urllib.error

UA = "codex_cli_rs/0.153.0 (Macos 15.4.0; arm64) Terminal"   # 版本号改成你的
auth = json.load(open('/Users/roycheung/.codex/auth.json'))
tok, acct = auth['tokens']['access_token'], auth['tokens']['account_id']

def probe(commands, max_output_tokens=4096, model="gpt-5.6-luna"):
    body = {"id": str(uuid.uuid4()), "model": model, "commands": commands,
            "settings": {"external_web_access": True, "allowed_callers": ["direct"]},
            "max_output_tokens": max_output_tokens}
    for _ in range(6):
        try:
            req = urllib.request.Request(
                'https://chatgpt.com/backend-api/codex/alpha/search',
                data=json.dumps(body).encode(), method='POST',
                headers={'Authorization': f'Bearer {tok}', 'chatgpt-account-id': acct,
                         'originator': 'codex_cli_rs', 'User-Agent': UA,
                         'Content-Type': 'application/json'})
            t0 = time.time()
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.loads(r.read().decode(errors='replace')), time.time() - t0
        except Exception as e:
            print(f"  retry: {type(e).__name__}", file=sys.stderr); time.sleep(3)
    return None, None

if __name__ == '__main__':
    d, el = probe({"search_query": [{"q": "福冈有什么地方玩"}]})
    if d is None: raise SystemExit("all attempts failed")
    print(f"raw ouput: {json.dumps(d, ensure_ascii=False)}")
    out, res = d['output'], d.get('results') or []
    print(f"latency: {el:.2f}s")
    print(f"envelope keys: {sorted(d.keys())}")
    print(f"output: {len(out)} chars | results: {len(res)}")
    print(f"output[:300]:\n{out[:300]}")
    print(f"results[0]: {json.dumps(res[0], ensure_ascii=False)}")
