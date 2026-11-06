import pandas as pd, numpy as np
def md(d):
    return '| '+' | '.join(d.columns)+' |\n|'+'---|'*len(d.columns)+'\n'+'\n'.join('| '+' | '.join('' if (isinstance(v,float) and np.isnan(v)) else str(v) for v in r)+' |' for r in d.itertuples(index=False))
s=pd.read_csv("out/step1_unit_price_screening.csv",dtype={"hs":str}); sens=pd.read_csv("out/sensitivity_table.csv",dtype={"hs":str}).set_index("hs")
keep=s[s.keep]
t1=s[["hs","category","unit","n_major_origins","cheapest","second","top2_gap_pct","china_vs_nearest_gap_pct","china_share_2024_pct","keep"]].round(1)
t1.columns=["HS6","Category","Unit","Major origins","Cheapest origin","2nd cheapest","Top-2 gap %","China vs nearest %","China share %","Keep"]
t2=keep[["hs","category","unit_cif_by_origin_2024"]]; t2.columns=["HS6","Category","2024 unit CIF by origin (share)"]
k=sens.loc[keep.hs].reset_index()
t3=k[["hs","category","top2_gap_pct","flip_tariff10","flip_fx10","flip_freight86","cheapest_by_year"]].round(1)
t3.columns=["HS6","Category","Top-2 gap %","+10 pp tariff on cheapest flips?","+10% FX on cheapest flips?","Ocean freight +86% flips?","Cheapest origin 2023→2026"]
big=sens[~sens.index.isin(keep.hs)]
out=f"""# SourceSwitch AI — Analysis storyline (data as of {pd.Timestamp.today():%Y-%m-%d})

**Premise.** When the average import cost of a product is nearly the same across source countries, the sourcing ranking is fragile: a tariff change, a currency move or a freight swing can flip which origin is cheapest. Those are the categories where a Stay / Switch / Renegotiate tool earns its keep. So: **Step 1** screen real U.S. import data for categories whose cross-origin unit costs are close, **Step 2** show that those categories flip under realistic shocks while wide-gap categories do not, **Step 3** build the tool for the kept set.

**Data.** UN Comtrade (U.S. reporter; same Census source as USITC DataWeb), HS6 × origin, 2023–2025 annual + Jan–Feb 2026. Unit CIF = CIF value ÷ reported quantity; freight+insurance = CIF − FOB. Only lines where the U.S. reports a physical quantity are usable ({len(s)} of 36 pulled); toys, bags of 4202.92, kitchenware, games, lamps, bedding, porcelain and glassware report weight only and were dropped (Comtrade back-fills their quantity with one uniform unit value, so every origin looks identical). Tariffs: MFN from the USITC HTS API; Section 301 lists; 2025 time-weighted IEEPA rates; 2026 Section 301 forced-labor rates (see `tariff_assumptions.md`).

## Step 1 — Screen by unit-cost closeness (2024, top-6 origins with ≥3% share)

Metric: gap between the two cheapest major origins, and China vs its nearest competitor. **Keep rule: either gap ≤ 10%.**

{md(t1)}

**Kept ({len(keep)}):** {", ".join(f"{r.category} (HS {r.hs})" for r in keep.itertuples())}.

Unit costs behind the kept categories:

{md(t2)}

## Step 2 — Are near-tied categories really fragile? Shock simulation on 2024 costs

Three shocks applied to the cheapest origin: +10 pp tariff, +10% currency appreciation, and ocean freight +86% (FBX global index $1,850 → $3,440/FEU between Feb and Nov 2026).

{md(t3)}

- Kept (near-tied) categories flip in **{k.flips_sim.mean():.1f} of 3** shocks on average; wide-gap categories flip in **{big.flips_sim.mean():.1f} of 3**.
- Freight alone never flips a ranking: freight+insurance is only 4–12% of FOB for these goods, so an 86% freight jump moves landed cost by ~3–10%. Tariffs and FX are the levers that matter.
- Historical check (2023→2026 unit-cost rankings): the cheapest origin changed at least once in {int(sens.loc[keep.hs].cheapest_changes.gt(0).sum())} of {len(keep)} kept categories vs {int(big.cheapest_changes.gt(0).sum())} of {len(big)} wide-gap ones; with this sample size that is suggestive, not significant.

## Step 3 — What the tool should do for these categories

For a kept category the break-even tariff differential is small (2–10 pp), so the tool's job is to (1) take the importer's own supplier quotes (trade unit values are market averages that mix product grades), (2) apply the current tariff stack by origin, (3) report the break-even tariff / FX threshold and a Stay / Switch / Renegotiate flag. Showcase candidates: **Leather footwear (HS 640399, China vs Indonesia, 4% gap)** and **Cotton sweaters (HS 611020, Bangladesh vs China, 2% gap)**; Wooden bedroom furniture (HS 940350, Italy vs China 0.1% gap) is the furniture-themed backup.

## Caveats
- Unit values are HS6 market averages, not supplier quotes; closeness can hide product-mix differences.
- Comtrade's free quota ran out before all 2026 months were fetched; 2026 is Jan–Feb only, and 10 categories have 2023–2024 only.
- Tariff rates are reconstructed from CBP's Jan-2026 overview and broker trackers; spot-check before presenting.

Files: `step1_unit_price_screening.csv` (Step 1 table), `sensitivity_table.csv` / `closeness_ranking.csv` (Step 2), `charts/4_closeness_targets.png` (Step 1 chart), `charts/3_showcase_landed_cost.png`, `partner_level_2023_2026.csv` (origin-level detail), `appendix_hypothesis_test.md` (earlier test of the tariff-switching version of the hypothesis: not supported — share shifts were broad-based and unrelated to the gap).
"""
open("out/FINDINGS.md","w").write(out); print("report2 ok")
