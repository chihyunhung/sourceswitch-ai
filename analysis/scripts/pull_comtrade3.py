import json, time, urllib.request, urllib.parse, sys, os
BASE="https://comtradeapi.un.org/public/v1/preview/C/{freq}/HS"
CODES=json.load(open("data/codes3.json")) if os.path.exists("data/codes3.json") else {}
CODES={ "640411":"Sports footwear, textile uppers","640419":"Other footwear, textile uppers","640391":"Leather footwear covering ankle","620520":"Men's cotton shirts",
 "620630":"Women's cotton blouses","611030":"Man-made fibre sweaters","610462":"Women's cotton trousers (knit)","420212":"Suitcases/briefcases, plastic/textile",
 "420221":"Handbags, leather","871200":"Bicycles","940429":"Mattresses (other materials)","841451":"Table/floor fans"}
json.dump(CODES,open("data/codes3.json","w"))
def get(freq, period, cmd):
    q=dict(reporterCode=842, period=period, cmdCode=cmd, flowCode="M", includeDesc="true")
    url=BASE.format(freq=freq)+"?"+urllib.parse.urlencode(q)
    for attempt in range(6):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code==429: time.sleep(3); continue
            print("ERR",cmd,period,e.code,e.read()[:200], file=sys.stderr); return None
        except Exception as e:
            print("retry",cmd,period,e, file=sys.stderr); time.sleep(3)
    return None
outfile="data/comtrade_raw3.json"
out=json.load(open(outfile)) if os.path.exists(outfile) else {}
periods=[("A","2023"),("A","2024"),("A","2025")]+[("M",f"2026{m:02d}") for m in range(1,10)]
for freq,period in periods:
    for cmd in CODES:
        key=f"{cmd}_{period}"
        if key in out: continue
        d=get(freq,period,cmd)
        if d is not None:
            out[key]=d.get("data",[]); print(key,"rows",len(out[key]),"count",d.get("count"),flush=True)
            json.dump(out,open(outfile,"w"))
        time.sleep(2.2)
print("DONE")
