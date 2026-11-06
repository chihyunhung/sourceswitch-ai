import pandas as pd, numpy as np, json
CODES={}
for f in ["data/codes.json","data/codes2.json","data/codes3.json"]: CODES.update(json.load(open(f)))
ann=pd.read_csv("out/partner_level_2023_2026.csv",dtype={"hs":str,"year":str})
sens=pd.read_csv("out/sensitivity_table.csv",dtype={"hs":str}).set_index("hs")
rows=[]
for hs,g in ann[ann.year=="2024"].groupby("hs"):
    top=g[g.share>=0.03].sort_values("share",ascending=False).head(6)
    if len(top)<2: continue
    s=top.sort_values("u_cif")
    prices=" | ".join(f"{r.partner} ${r.u_cif:,.2f} ({r.share*100:.0f}%)" for r in s.itertuples())
    cn=top[top.iso=="CHN"]
    cn_gap=np.nan
    if len(cn):
        others=top[top.iso!="CHN"]; cn_gap=((others.u_cif-cn.u_cif.iloc[0]).abs()/cn.u_cif.iloc[0]).min()*100
    top2=(s.u_cif.iloc[1]-s.u_cif.iloc[0])/s.u_cif.iloc[0]*100
    rows.append(dict(hs=hs,category=CODES.get(hs,hs),unit=top.unit.iloc[0],n_major_origins=len(top),cheapest=s.partner.iloc[0],second=s.partner.iloc[1],
        top2_gap_pct=top2,china_vs_nearest_gap_pct=cn_gap,china_share_2024_pct=(cn.share.iloc[0]*100 if len(cn) else 0),
        unit_cif_by_origin_2024=prices,
        flips_in_3_shocks=int(sens.flips_sim.get(hs,0)) if hs in sens.index else np.nan))
d=pd.DataFrame(rows).sort_values("top2_gap_pct")
d["keep"]=(d.top2_gap_pct<=10)|(d.china_vs_nearest_gap_pct<=10)
d.to_csv("out/step1_unit_price_screening.csv",index=False)
pd.set_option("display.width",250); pd.set_option("display.max_colwidth",60)
print(d[["hs","category","unit","n_major_origins","cheapest","second","top2_gap_pct","china_vs_nearest_gap_pct","china_share_2024_pct","flips_in_3_shocks","keep"]].round(1).to_string(index=False))
print("\nKEEP:",d[d.keep].category.tolist())
