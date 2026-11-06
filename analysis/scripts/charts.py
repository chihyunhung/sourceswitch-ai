import pandas as pd, numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt, os
res=pd.read_csv("out/category_hypothesis_table.csv",dtype={"hs":str}); ann=pd.read_csv("out/partner_level_2023_2026.csv",dtype={"hs":str,"year":str})
C1,C2,C3,GRAY,INK,MUTED="#2a78d6","#eb6834","#1baf7a","#b8b7b2","#0b0b0b","#52514e"
plt.rcParams.update({"font.size":10,"axes.spines.top":False,"axes.spines.right":False,"axes.edgecolor":GRAY,"axes.labelcolor":MUTED,"xtick.color":MUTED,"ytick.color":MUTED,"figure.facecolor":"white"})
os.makedirs("out/charts",exist_ok=True)
m=res.dropna(subset=["d_share_24_25"]).copy()
# 1. scatter: 2024 cost gap vs China share change
fig,ax=plt.subplots(figsize=(8,5.2))
ax.axvline(22.8,color=GRAY,lw=1,ls="--"); ax.text(23.5,m.d_share_24_25.min(),"2025 avg. extra tariff on China\nvs. nearest competitor (≈23 pp)",color=MUTED,fontsize=8.5,va="bottom")
ax.axhline(0,color=GRAY,lw=0.8)
ax.scatter(m.abs_gap_nearest_pct,m.d_share_24_25,s=70,color=C1,edgecolor="white",lw=1.5,zorder=3)
ms=m.sort_values("abs_gap_nearest_pct").reset_index(drop=True)
for i,r in ms.iterrows(): ax.annotate(r.category,(r.abs_gap_nearest_pct,r.d_share_24_25),xytext=(7,(8 if i%2==0 else -11)),textcoords="offset points",fontsize=8,color=INK)
ax.set_xscale("symlog",linthresh=10); ax.set_xlabel("2024 unit-CIF gap, China vs nearest competitor (|%|, symlog)"); ax.set_ylabel("Change in China's U.S. import share, 2024→2025 (pp)")
ax.set_title("Small cost gaps did not predict bigger sourcing shifts",loc="left",fontsize=12,color=INK,fontweight="bold"); ax.grid(axis="y",color="#ececea",lw=0.6)
fig.tight_layout(); fig.savefig("out/charts/1_gap_vs_share_change.png",dpi=180); plt.close()
# 2. China share 2023/2024/2025/2026YTD dot-line by category
s=m.sort_values("cn_share_2024",ascending=True)
fig,ax=plt.subplots(figsize=(8,0.42*len(s)+1.6))
y=np.arange(len(s))
for i,(_,r) in enumerate(s.iterrows()):
    ax.plot([r.cn_share_2024,r.cn_share_2025],[i,i],color=GRAY,lw=2,zorder=1)
ax.scatter(s.cn_share_2024,y,color=GRAY,s=45,zorder=2,label="2024")
ax.scatter(s.cn_share_2025,y,color=C1,s=55,zorder=3,label="2025")
if s.cn_share_2026ytd.notna().any(): ax.scatter(s.cn_share_2026ytd,y,color=C2,s=55,marker="D",zorder=3,label="2026 YTD")
ax.set_yticks(y); ax.set_yticklabels(s.category); ax.set_xlabel("China share of U.S. import value (%)"); ax.legend(frameon=False,loc="lower right")
ax.set_title("China lost U.S. import share in every category in 2025",loc="left",fontsize=12,color=INK,fontweight="bold"); ax.grid(axis="x",color="#ececea",lw=0.6)
fig.tight_layout(); fig.savefig("out/charts/2_china_share_shift.png",dpi=180); plt.close()
# 3. showcase: landed cost per unit by origin under 3 tariff regimes for the smallest-gap flip candidate
cand=m[m.pred_flip_2025].sort_values("abs_gap_nearest_pct")
hs=cand.iloc[0].hs if len(cand) else m.iloc[0].hs
b=ann[(ann.hs==hs)&(ann.year=="2024")&(ann.share>=0.03)].sort_values("landed_R0").head(6)
fig,ax=plt.subplots(figsize=(8,4.6)); w=0.26; x=np.arange(len(b))
for k,(R,lab,col) in enumerate([("R0","2024 tariffs",GRAY),("R1","2025 avg. tariffs",C1),("R2","2026 current tariffs",C2)]):
    ax.bar(x+(k-1)*w,b[f"landed_{R}"],w*0.92,color=col,label=lab)
ax.set_xticks(x); ax.set_xticklabels(b.partner,rotation=0,fontsize=9); ax.set_ylabel(f"Est. landed cost per unit (USD, 2024 unit CIF × (1+tariff))"); ax.legend(frameon=False)
ax.set_title(f"{res.set_index('hs').category[hs]} (HS {hs}): who is cheapest shifts with the tariff regime",loc="left",fontsize=12,color=INK,fontweight="bold"); ax.grid(axis="y",color="#ececea",lw=0.6)
fig.tight_layout(); fig.savefig("out/charts/3_showcase_landed_cost.png",dpi=180); plt.close()
print("charts done; showcase hs",hs)
