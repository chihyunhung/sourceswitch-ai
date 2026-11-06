import json, time, urllib.request, urllib.parse, sys, os
BASE="https://comtradeapi.un.org/public/v1/preview/C/{freq}/HS"
CODES=json.load(open("data/codes2.json")) if os.path.exists("data/codes2.json") else {}
CODES={ "940171":"Upholstered seats, metal frame","940320":"Metal furniture (other)","610910":"Cotton T-shirts","620462":"Women's cotton trousers",
 "640299":"Footwear, rubber/plastic uppers (other)","420222":"Handbags, plastic/textile","691110":"Porcelain tableware","701337":"Glass drinking glasses",
 "950490":"Games (board, etc.)","940540":"Other electric lamps/lighting","940490":"Bedding/quilts/cushions","732399":"Iron/steel kitchenware (other)"}
json.dump(CODES,open("data/codes2.json","w"))
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
outfile="data/comtrade_raw2.json"
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
