import pandas as pd, numpy as np, itertools, json
from scipy.stats import spearmanr, kendalltau, mannwhitneyu
CODES={}
for f in ["data/codes.json","data/codes2.json","data/codes3.json"]: CODES.update(json.load(open(f)))
ann=pd.read_csv("out/partner_level_2023_2026.csv",dtype={"hs":str,"year":str})
res=pd.read_csv("out/category_hypothesis_table.csv",dtype={"hs":str}).set_index("hs")
rows=[]
for hs,g in ann.groupby("hs"):
    top=g[(g.year=="2024")&(g.share>=0.03)].sort_values("share",ascending=False).head(6).iso.tolist()
    if len(top)<3: continue
    yrs=[y for y in ["2023","2024","2025","2026"] if (g.year==y).sum()>0]
    # rank vectors by unit CIF (no tariff) for the top origins
    rk={}
    for y in yrs:
        s=g[(g.year==y)&(g.iso.isin(top))].set_index("iso").u_cif
        if s.index.isin(top).sum()==len(top): rk[y]=s[top].rank().values
    # structural closeness in 2024: smallest adjacent gap among the sorted top origins, and gap between the two cheapest
    s24=g[(g.year=="2024")&(g.iso.isin(top))].sort_values("u_cif").u_cif.values
    adj=np.diff(s24)/s24[:-1]*100
    min_adj_gap=adj.min(); top2_gap=adj[0]
    # observed instability: 1 - Kendall tau between consecutive years, and whether the cheapest origin changed
    taus=[]; cheapest=[]
    for y in yrs:
        c=g[(g.year==y)&(g.iso.isin(top))].sort_values("u_cif")
        cheapest.append(c.iso.iloc[0] if len(c) else None)
    pairs=[(a,b) for a,b in zip(yrs[:-1],yrs[1:]) if a in rk and b in rk]
    for a,b in pairs: taus.append(kendalltau(rk[a],rk[b]).statistic)
    n_cheapest_changes=sum(1 for a,b in zip(cheapest[:-1],cheapest[1:]) if a and b and a!=b)
    # shock simulations on 2024 data: does the cheapest origin change?
    b24=g[(g.year=="2024")&(g.iso.isin(top))].copy()
    base=b24.sort_values("u_cif").iso.iloc[0]
    def cheapest_after(cost): return b24.assign(c=cost).sort_values("c").iso.iloc[0]
    frt=cheapest_after(b24.u_fob+(b24.u_cif-b24.u_fob)*1.86)      # ocean freight +86% (FBX $1,850 -> $3,440 in 2026)
    fx10=cheapest_after(b24.u_cif*np.where(b24.iso==base,1.10,1.0))  # cheapest origin's currency appreciates 10%
    tar10=cheapest_after(b24.u_cif*(1+b24.tar_R0/100)*np.where(b24.iso==base,1.10,1.0))  # +10pp tariff on cheapest origin
    rows.append(dict(hs=hs,category=CODES.get(hs,hs),n_top=len(top),min_adjacent_gap_pct=min_adj_gap,top2_gap_pct=top2_gap,
        cn_nearest_gap_pct=res.abs_gap_nearest_pct.get(hs,np.nan),years=len(yrs),
        mean_rank_instability=np.mean([1-t for t in taus]) if taus else np.nan,cheapest_changes=n_cheapest_changes,cheapest_by_year=" → ".join(c for c in cheapest if c),
        flip_freight86=frt!=base,flip_fx10=fx10!=base,flip_tariff10=tar10!=base))
d=pd.DataFrame(rows); d["flips_sim"]=d[["flip_freight86","flip_fx10","flip_tariff10"]].sum(axis=1)
d=d.sort_values("top2_gap_pct"); d.to_csv("out/sensitivity_table.csv",index=False)
pd.set_option("display.width",250)
print(d[["hs","category","top2_gap_pct","min_adjacent_gap_pct","mean_rank_instability","cheapest_changes","cheapest_by_year","flip_freight86","flip_fx10","flip_tariff10"]].round(2).to_string(index=False))
m=d.dropna(subset=["mean_rank_instability"])
print("\nn=",len(m))
print("Spearman(top-2 gap, rank instability)   rho=%.2f p=%.3f"%spearmanr(m.top2_gap_pct,m.mean_rank_instability))
print("Spearman(min adjacent gap, instability) rho=%.2f p=%.3f"%spearmanr(m.min_adjacent_gap_pct,m.mean_rank_instability))
print("Spearman(top-2 gap, #cheapest changes)  rho=%.2f p=%.3f"%spearmanr(m.top2_gap_pct,m.cheapest_changes))
small=m[m.top2_gap_pct<=10]; big=m[m.top2_gap_pct>10]
print(f"top-2 gap <=10%: n={len(small)}, cheapest origin changed in {small.cheapest_changes.gt(0).mean()*100:.0f}% of categories, mean instability {small.mean_rank_instability.mean():.2f}, sim flips {small.flips_sim.mean():.1f}/3")
print(f"top-2 gap  >10%: n={len(big)}, cheapest origin changed in {big.cheapest_changes.gt(0).mean()*100:.0f}% of categories, mean instability {big.mean_rank_instability.mean():.2f}, sim flips {big.flips_sim.mean():.1f}/3")
print("Mann-Whitney instability small<big p=%.3f"%mannwhitneyu(small.mean_rank_instability,big.mean_rank_instability,alternative="greater").pvalue)

# ---------- closeness ranking (the screening the product targets) + chart 4 ----------
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
d["china_in_top2"]=d.cheapest_by_year.str.split(" → ").str[1].eq("CHN") | d.hs.map(lambda h: res.cn_landed_rank_2024.get(h,9)<=2)
d["closeness_rank"]=d.top2_gap_pct.rank().astype(int)
d.sort_values("top2_gap_pct").to_csv("out/closeness_ranking.csv",index=False)
C1,C2,GRAY,INK,MUTED="#2a78d6","#eb6834","#b8b7b2","#0b0b0b","#52514e"
plt.rcParams.update({"font.size":10,"axes.spines.top":False,"axes.spines.right":False,"axes.edgecolor":GRAY,"axes.labelcolor":MUTED,"xtick.color":MUTED,"ytick.color":MUTED,"figure.facecolor":"white"})
p=d.sort_values("top2_gap_pct",ascending=False)
fig,ax=plt.subplots(figsize=(8.5,0.38*len(p)+1.6)); y=np.arange(len(p))
cols=[C1 if g<=10 else GRAY for g in p.top2_gap_pct]
ax.barh(y,p.top2_gap_pct.clip(upper=120),color=cols,height=0.62)
for i,(g,f) in enumerate(zip(p.top2_gap_pct,p.flips_sim)):
    ax.text(min(g,120)+1.5,i,f"{g:.0f}%  ·  flips in {int(f)}/3 shocks",va="center",fontsize=8,color=INK)
ax.axvline(10,color=C2,lw=1,ls="--"); ax.text(10.5,len(p)-0.4,"≤10% = target zone",color=C2,fontsize=8.5,va="top")
ax.set_yticks(y); ax.set_yticklabels(p.category); ax.set_xlim(0,165); ax.set_xlabel("2024 unit-CIF gap between the two cheapest major origins (%, capped at 120)")
ax.set_title("Near-tied origin costs: any shock flips the ranking",loc="left",fontsize=12,color=INK,fontweight="bold"); ax.grid(axis="x",color="#ececea",lw=0.6)
fig.tight_layout(); fig.savefig("out/charts/4_closeness_targets.png",dpi=180); plt.close(); print("chart 4 done")
