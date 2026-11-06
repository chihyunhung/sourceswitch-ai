import json, pandas as pd, numpy as np, os, glob
from scipy.stats import spearmanr, mannwhitneyu
raw={}; CODES={}
for f in ["data/comtrade_raw.json","data/comtrade_raw2.json","data/comtrade_raw3.json"]:
    if os.path.exists(f): raw.update(json.load(open(f)))
for f in ["data/codes.json","data/codes2.json","data/codes3.json"]:
    if os.path.exists(f): CODES.update(json.load(open(f)))
# ---------- tariff assumptions (see README) ----------
MFN={"940360":0,"940161":0,"940350":0,"950300":0,"640399":8.5,"420292":17.6,"392410":6.5,"611020":16.5,"620342":16.6,"940520":3.9,"732393":2.0,"851830":0,
     "940171":0,"940320":0,"610910":16.5,"620462":16.6,"640299":20,"420222":17.6,"691110":8,"701337":22.5,"950490":0,"940540":3.9,"940490":6,"732399":3.4,"640411":20,"640419":20,"640391":8.5,"620520":19.7,"620630":15.4,"611030":32,"610462":14.9,"420212":20,"420221":9,"871200":11,"940429":6,"841451":4.7}
S301={"940360":25,"940161":25,"940350":25,"950300":0,"640399":7.5,"420292":25,"392410":25,"611020":7.5,"620342":7.5,"940520":25,"732393":25,"851830":7.5,
      "940171":25,"940320":25,"610910":7.5,"620462":7.5,"640299":7.5,"420222":25,"691110":25,"701337":25,"950490":7.5,"940540":25,"940490":25,"732399":25,"640411":7.5,"640419":7.5,"640391":7.5,"620520":7.5,"620630":7.5,"611030":7.5,"610462":7.5,"420212":25,"420221":25,"871200":25,"940429":25,"841451":25}
S232_FURN={"940161"}
EU={"ITA","DEU","POL","FRA","ESP","PRT","ROU","LTU","NLD","DNK","SWE","AUT","BEL","CZE","HUN","SVK","SVN","HRV","BGR","IRL","FIN","GRC","LVA","EST","LUX"}
def extra_tariff(iso, hs, regime):
    mfn=MFN[hs]; s301=S301[hs]; furn=hs in S232_FURN
    if regime=="R0": return s301 if iso=="CHN" else 0
    if regime=="R1":  # 2025 time-weighted average extra tariff (IEEPA fentanyl+reciprocal, Sec 232 furniture from Oct 14)
        furn_add=25*79/365 if furn else 0   # Sec 232 25% for 79 days of 2025, all origins
        if iso=="CHN": return s301+34.3+furn_add   # Feb4 10%, Mar4 20%, Apr9-May13 145%, May14 30%, Nov10 20%
        tbl={"VNM":11.5,"IDN":11.1,"MYS":11.1,"THA":11.1,"KHM":11.1,"PHL":11.1,"IND":22.4,"BGD":11.5,"PAK":11.1,"LKA":11.5,"S19":11.5,"TWN":11.5,"MEX":0,"CAN":0,"GBR":7.4,"TUR":7.4,"BRA":24.2,"NIC":10.6,"HND":7.4,"GTM":7.4,"SLV":7.4,"DOM":7.4,"HTI":7.4,"EGY":7.4,"JOR":7.4,"PER":7.4,"COL":7.4}
        if iso in tbl: return tbl[iso]+furn_add
        if iso in EU or iso in {"JPN","KOR","CHE"}: return 10*124/365+max(0,15-mfn)*147/365+furn_add
        return 7.4+furn_add   # 10% baseline reciprocal from Apr 5
    if regime=="R2":
        if furn:
            if iso=="CHN": return s301+25
            if iso in EU or iso in {"JPN","KOR"}: return 15
            if iso=="GBR": return 10
            return 25
        tbl={"CHN":s301+12.5,"VNM":12.5,"THA":12.5,"IDN":10,"MYS":10,"IND":10,"KHM":10,"MEX":0,"CAN":0,"GBR":10,"BRA":37.5}
        if iso in tbl: return tbl[iso]
        if iso in EU or iso=="S19": return max(0,10-mfn)
        if iso in {"JPN","KOR"}: return max(0,12.5-mfn)
        return 10
rows=[]
for key,data in raw.items():
    hs,period=key.split("_")
    for r in data:
        if r["partnerCode"]==0: continue
        rows.append(dict(hs=hs,period=period,year=period[:4],iso=r["partnerISO"],partner=r["partnerDesc"],qty=(r["qty"] or 0) if not r["isQtyEstimated"] else 0,
                         unit=r.get("qtyUnitAbbr"),cif=r["cifvalue"] or 0,fob=r["fobvalue"] or 0))
df=pd.DataFrame(rows); df.loc[df.iso=="S19","partner"]="Taiwan"
YTD_MONTHS={"202601","202602"}
df=df[(df.period.str.len()==4)|(df.period.isin(YTD_MONTHS))]
months=sorted({p for p in df.period if len(p)==6}); print("2026 months:",months)
ann=df.groupby(["hs","year","iso","partner"],as_index=False).agg(qty=("qty","sum"),cif=("cif","sum"),fob=("fob","sum"),unit=("unit","first"))
tot=ann.groupby(["hs","year"])[["cif"]].sum().rename(columns={"cif":"tot_cif"}); ann=ann.join(tot,on=["hs","year"]); ann["share"]=ann.cif/ann.tot_cif
qcov=(ann[ann.qty>0].groupby(["hs","year"]).cif.sum()/tot.tot_cif).rename("qcov"); ann=ann.join(qcov,on=["hs","year"])
valid_hs=sorted(set(ann[(ann.year=="2024")&(ann.qcov>=0.9)].hs))
dropped={h:CODES[h] for h in CODES if h not in valid_hs}
print("valid categories:",len(valid_hs),"dropped (no reported quantity / no data):",dropped)
ann=ann[(ann.hs.isin(valid_hs))&(ann.qty>0)].copy()
ann["u_cif"]=ann.cif/ann.qty; ann["u_fob"]=ann.fob/ann.qty; ann["frt_pct"]=(ann.u_cif-ann.u_fob)/ann.u_fob
for R in ["R0","R1","R2"]:
    ann[f"tar_{R}"]=[MFN[h]+extra_tariff(i,h,R) for h,i in zip(ann.hs,ann.iso)]; ann[f"landed_{R}"]=ann.u_cif*(1+ann[f"tar_{R}"]/100)
ann["category"]=ann.hs.map(CODES)
out=[]
for hs in valid_hs:
    b=ann[(ann.hs==hs)&(ann.year=="2024")&(ann.share>=0.03)].copy()
    if "CHN" not in set(b.iso) or len(b)<2: continue
    cn=b[b.iso=="CHN"].iloc[0]; alts=b[b.iso!="CHN"].copy()
    alts["absgap"]=(alts.u_cif-cn.u_cif).abs()/cn.u_cif
    near=alts.sort_values("absgap").iloc[0]; cheap=alts.sort_values("u_cif").iloc[0]
    gap_near=(near.u_cif-cn.u_cif)/cn.u_cif*100
    # tariff differential actually imposed on China vs the nearest competitor, 2024 -> late 2025 / 2026 (pp)
    dtar_R1=(cn.tar_R1-cn.tar_R0)-(near.tar_R1-near.tar_R0); dtar_R2=(cn.tar_R2-cn.tar_R0)-(near.tar_R2-near.tar_R0)
    def rank_cn(R):
        s=b.sort_values(f"landed_{R}"); return list(s.iso).index("CHN")+1, s.iloc[0].partner
    def sh(y):
        x=ann[(ann.hs==hs)&(ann.year==y)&(ann.iso=="CHN")]; return float(x.share.iloc[0])*100 if len(x) else np.nan
    r0,r1,r2=rank_cn("R0"),rank_cn("R1"),rank_cn("R2")
    out.append(dict(hs=hs,category=CODES[hs],unit=cn.unit,n_origins_ge3pct=len(b),cn_share_2024=cn.share*100,cn_u_cif_2024=cn.u_cif,cn_freight_pct=cn.frt_pct*100,
        nearest_competitor=near.partner,near_share_2024=near.share*100,near_u_cif_2024=near.u_cif,gap_nearest_pct=gap_near,abs_gap_nearest_pct=abs(gap_near),
        cheapest_origin_2024=cheap.partner,cheapest_u_cif_2024=cheap.u_cif,
        mfn=MFN[hs],s301_china=S301[hs],cn_tariff_2024=cn.tar_R0,cn_tariff_late2025=cn.tar_R1,cn_tariff_2026=cn.tar_R2,
        tariff_diff_vs_nearest_2025pp=dtar_R1,tariff_diff_vs_nearest_2026pp=dtar_R2,
        cn_landed_rank_2024=r0[0],cn_landed_rank_2025=r1[0],cn_landed_rank_2026=r2[0],cheapest_landed_2024=r0[1],cheapest_landed_2025=r1[1],cheapest_landed_2026=r2[1],
        pred_flip_2025=r1[0]>r0[0],pred_flip_2026=r2[0]>r0[0],
        cn_share_2023=sh("2023"),cn_share_2025=sh("2025"),cn_share_2026ytd=sh("2026")))
res=pd.DataFrame(out)
res["d_share_23_24"]=res.cn_share_2024-res.cn_share_2023; res["d_share_24_25"]=res.cn_share_2025-res.cn_share_2024; res["d_share_24_26"]=res.cn_share_2026ytd-res.cn_share_2024
res["excess_drop_24_25"]=res.d_share_24_25-res.d_share_23_24
res=res.sort_values("abs_gap_nearest_pct")
os.makedirs("out",exist_ok=True); ann.to_csv("out/partner_level_2023_2026.csv",index=False); res.to_csv("out/category_hypothesis_table.csv",index=False)
pd.set_option("display.width",260); pd.set_option("display.max_columns",40)
print(res[["hs","category","cn_share_2024","cn_u_cif_2024","nearest_competitor","near_u_cif_2024","gap_nearest_pct","tariff_diff_vs_nearest_2025pp","cn_landed_rank_2024","cn_landed_rank_2025","cn_landed_rank_2026","pred_flip_2025","d_share_23_24","d_share_24_25","d_share_24_26","excess_drop_24_25"]].round(1).to_string())
print("\n--- tests ---")
for col in ["d_share_24_25","d_share_24_26","excess_drop_24_25"]:
    m=res.dropna(subset=[col])
    if len(m)>3:
        rho,p=spearmanr(m.abs_gap_nearest_pct,m[col]); print(f"{col}: Spearman(|gap|, dChinaShare) rho={rho:.2f} p={p:.3f} n={len(m)}")
        a=m[m.pred_flip_2025][col]; bb=m[~m.pred_flip_2025][col]
        if len(a)>1 and len(bb)>1: print(f"   predicted-flip group mean={a.mean():.1f}pp (n={len(a)}) vs no-flip mean={bb.mean():.1f}pp (n={len(bb)}); Mann-Whitney p={mannwhitneyu(a,bb,alternative='less').pvalue:.3f}")

# ---------- extra diagnostics: what actually predicts China's share loss? ----------
vn=ann[(ann.year=="2024")&(ann.iso=="VNM")].set_index("hs").share*100
res["vn_share_2024"]=res.hs.map(vn).fillna(0)
# actual landed-cost rank of China in 2025 using 2025 unit values + 2025 avg tariffs
def actual_rank(hs,year,R):
    b=ann[(ann.hs==hs)&(ann.year==year)&(ann.share>=0.03)].sort_values(f"landed_{R}")
    return (list(b.iso).index("CHN")+1) if "CHN" in set(b.iso) else np.nan
res["cn_actual_rank_2025"]=[actual_rank(h,"2025","R1") for h in res.hs]
res["actual_rank_flip_2025"]=res.cn_actual_rank_2025>res.cn_landed_rank_2024
res.to_csv("out/category_hypothesis_table.csv",index=False)
m=res.dropna(subset=["d_share_24_25"])
if len(m)>3:
    for x in ["abs_gap_nearest_pct","cn_share_2024","vn_share_2024","tariff_diff_vs_nearest_2025pp"]:
        rho,p=spearmanr(m[x],m.d_share_24_25); print(f"Spearman({x}, dChinaShare 24->25) rho={rho:.2f} p={p:.3f} n={len(m)}")
    print("predicted flips (2024 gap < 2025 tariff differential):",int(m.pred_flip_2025.sum()),"of",len(m),"| actual rank flips 2025:",int(m.actual_rank_flip_2025.sum()))
    print("mean China share change 24->25: %.1f pp; categories with China share loss: %d of %d"%(m.d_share_24_25.mean(),(m.d_share_24_25<0).sum(),len(m)))
res["rel_loss_24_25"]=res.d_share_24_25/res.cn_share_2024*100   # % of China's 2024 share lost
res["rel_loss_24_26"]=res.d_share_24_26/res.cn_share_2024*100
res.to_csv("out/category_hypothesis_table.csv",index=False)
m=res.dropna(subset=["rel_loss_24_25"])
if len(m)>3:
    print("\n--- relative loss (share change as % of 2024 share) ---")
    for x in ["abs_gap_nearest_pct","cn_share_2024","vn_share_2024","s301_china"]:
        rho,p=spearmanr(m[x],m.rel_loss_24_25); print(f"Spearman({x}, relLoss 24->25) rho={rho:.2f} p={p:.3f} n={len(m)}")
    a=m[m.pred_flip_2025].rel_loss_24_25; bb=m[~m.pred_flip_2025].rel_loss_24_25
    print(f"predicted-flip group mean rel loss={a.mean():.1f}% (n={len(a)}) vs no-flip={bb.mean():.1f}% (n={len(bb)})")
    print(m[["category","cn_share_2024","abs_gap_nearest_pct","pred_flip_2025","d_share_24_25","rel_loss_24_25"]].round(1).to_string())

# ---------- screening funnel: narrow to showcase categories ----------
sc=res.copy()
sc["c1_quantity_reported"]=True
sc["c2_multi_origin"]=(sc.n_origins_ge3pct>=3)&(sc.cn_share_2024>=5)
sc["c3_scaled_similar_alt"]=(sc.near_share_2024>=5)&(sc.abs_gap_nearest_pct<=30)
sc["c4_tariff_flips_rank"]=sc.pred_flip_2025
sc["c5_switch_observed_2025"]=sc.d_share_24_25<0
sc["score"]=sc[["c1_quantity_reported","c2_multi_origin","c3_scaled_similar_alt","c4_tariff_flips_rank","c5_switch_observed_2025"]].sum(axis=1)
sc["data_2025"]=sc.d_share_24_25.notna()
sc=sc.sort_values(["score","abs_gap_nearest_pct"],ascending=[False,True])
sc[["hs","category","score","c2_multi_origin","c3_scaled_similar_alt","c4_tariff_flips_rank","c5_switch_observed_2025","data_2025","cn_share_2024","nearest_competitor","near_share_2024","abs_gap_nearest_pct","tariff_diff_vs_nearest_2025pp","d_share_24_25","rel_loss_24_25"]].to_csv("out/shortlist_screening.csv",index=False)
print("\n--- screening funnel ---")
print(sc[["hs","category","score","c2_multi_origin","c3_scaled_similar_alt","c4_tariff_flips_rank","c5_switch_observed_2025","cn_share_2024","nearest_competitor","near_share_2024","abs_gap_nearest_pct","d_share_24_25"]].round(1).to_string(index=False))
