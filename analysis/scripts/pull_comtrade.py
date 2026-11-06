import json, time, urllib.request, urllib.parse, sys, os
BASE="https://comtradeapi.un.org/public/v1/preview/C/{freq}/HS"
CODES=json.load(open("data/codes.json")) if os.path.exists("data/codes.json") else {}
CODES={ "940360":"Wooden furniture (other)","940161":"Upholstered seats, wooden frame","940350":"Wooden bedroom furniture",
 "950300":"Toys","640399":"Leather footwear (other)","420292":"Bags/cases, plastic or textile outer","392410":"Plastic tableware/kitchenware",
 "611020":"Cotton sweaters/pullovers","620342":"Men's cotton trousers","940520":"Electric table/desk/bedside lamps",
 "732393":"Stainless steel kitchenware","851830":"Headphones/earphones"}
json.dump(CODES,open("data/codes.json","w"))
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
outfile="data/comtrade_raw.json"
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
