import pandas as pd, numpy as np
from scipy.stats import spearmanr
def md_table(d):
    h='| '+' | '.join(d.columns)+' |\n|'+'---|'*len(d.columns)+'\n'
    return h+'\n'.join('| '+' | '.join('' if (isinstance(v,float) and np.isnan(v)) else str(v) for v in r)+' |' for r in d.itertuples(index=False))
res=pd.read_csv("out/category_hypothesis_table.csv",dtype={"hs":str}); m=res.dropna(subset=["d_share_24_25"]).copy()
rho_abs,p_abs=spearmanr(m.abs_gap_nearest_pct,m.d_share_24_25); rho_rel,p_rel=spearmanr(m.abs_gap_nearest_pct,m.rel_loss_24_25); rho_sh,p_sh=spearmanr(m.cn_share_2024,m.d_share_24_25)
pf=m[m.pred_flip_2025]; npf=m[~m.pred_flip_2025]
sc=pd.read_csv("out/shortlist_screening.csv",dtype={"hs":str})[["hs","category","score","c2_multi_origin","c3_scaled_similar_alt","c4_tariff_flips_rank","c5_switch_observed_2025","cn_share_2024","nearest_competitor","near_share_2024","abs_gap_nearest_pct","d_share_24_25"]]
sc.columns=["HS6","Category","Score","Multi-origin","Scaled similar alt.","Tariff flips rank","Switch observed","CN share 2024 %","Nearest competitor","Comp. share %","|Gap| %","Δ CN share 24→25 pp"]
t=m.sort_values("abs_gap_nearest_pct")[["hs","category","cn_share_2024","cn_u_cif_2024","nearest_competitor","near_u_cif_2024","gap_nearest_pct","cn_freight_pct","cn_tariff_2024","cn_tariff_late2025","cn_tariff_2026","pred_flip_2025","actual_rank_flip_2025","cn_share_2025","cn_share_2026ytd","d_share_24_25","rel_loss_24_25"]].copy()
t.columns=["HS6","Category","CN share 2024 %","CN unit CIF $","Nearest competitor","Comp. unit CIF $","Gap %","CN freight+ins %","CN tariff 2024 %","CN tariff 2025 avg %","CN tariff 2026 %","Predicted flip (2025)","Actual landed-rank flip (2025)","CN share 2025 %","CN share 2026YTD %","Δ share 24→25 pp","Rel. loss %"]
md=f"""# SourceSwitch AI — Hypothesis test (data as of {pd.Timestamp.today():%Y-%m-%d})

**Hypothesis.** Categories where the average import cost gap between source countries is small should see their cost ranking flip more easily when tariffs change.

**Data.** UN Comtrade (U.S. as reporter; same Census source as USITC DataWeb), HS6, general imports by origin: CIF value, FOB value and *reported* quantity, 2023–2025 annual plus 2026 monthly YTD. Unit CIF = CIF value ÷ quantity. Freight+insurance = CIF − FOB. Categories where the U.S. reports no quantity (toys, bags, plastic & steel kitchenware, games, lamps, bedding…) were **excluded** because Comtrade back-fills their quantity with a uniform estimated unit value, which makes every origin look identical. Tariffs: MFN from the USITC HTS REST API; Section 301 list rates (assumed from USTR lists); 2025 = time-weighted average of IEEPA fentanyl/reciprocal rates plus Section 232 furniture; 2026 = Section 301 forced-labor tariffs in force since 2026-07-24. See `tariff_assumptions.md`.

**Sample.** {len(m)} HS6 categories with reported quantities and China ≥3% share in 2024.

## Results

| Test | Result |
|---|---|
| 2024 cost gap (China vs nearest competitor) < 2025 extra-tariff differential (≈23 pp) → predicted rank flip | {len(pf)} of {len(m)} categories predicted to flip |
| Actual landed-cost rank flip in 2025 (2025 unit values + 2025 tariffs) | {int(m.actual_rank_flip_2025.sum())} of {len(m)} |
| China lost U.S. import share 2024→2025 | {(m.d_share_24_25<0).sum()} of {len(m)} categories; mean {m.d_share_24_25.mean():.1f} pp; mean relative loss {m.rel_loss_24_25.mean():.0f}% of 2024 share |
| Spearman: \\|gap\\| vs Δ China share (pp) | rho = {rho_abs:.2f}, p = {p_abs:.3f} (opposite sign to hypothesis) |
| Spearman: China 2024 share vs Δ China share (pp) | rho = {rho_sh:.2f}, p = {p_sh:.3f} (initial share dominates) |
| Spearman: \\|gap\\| vs *relative* share loss (controls for initial share) | rho = {rho_rel:.2f}, p = {p_rel:.3f} (no relationship) |
| Mean relative loss, predicted-flip vs no-flip group | {pf.rel_loss_24_25.mean():.0f}% vs {npf.rel_loss_24_25.mean():.0f}% |

**Verdict: not supported as stated.** With market-average unit values, small cost gaps did *not* predict larger sourcing shifts. Sourcing moved away from China in every category in 2025 regardless of the gap, and the biggest absolute moves were in categories where China was by far the cheapest per unit (headphones, upholstered seats) — which exposes the real problem: trade unit values mix product grades (Vietnam ships premium earbuds, China ships budget ones), so they cannot measure a supplier-level cost gap.

**What the data does support.**
1. The tariff differential China faced vs. its nearest competitor jumped from 0 pp (Section 301 only, already in the 2024 baseline) to ~{m.tariff_diff_vs_nearest_2025pp.mean():.0f} pp in 2025 (time-weighted), then collapsed back to ~{m.tariff_diff_vs_nearest_2026pp.mean():.0f} pp under the 2026 regime — yet 2026 YTD shares show no return to China. Switching is sticky.
2. In {len(pf)} of {len(m)} categories the 2024 cost gap was smaller than the 2025 tariff shock, so a tariff-only landed-cost model *would* have flipped the ranking — the break-even threshold is the right quantity for the tool to surface.
3. Freight+insurance is a small share of landed cost for these goods (China median {m.cn_freight_pct.median():.1f}% of FOB), so tariffs, not freight, drive the switching decision.

**Implication for the product.** Use trade data as a market benchmark for the *shortlist* (which origins have scale, what the tariff differential is), but compute the Stay / Switch / Renegotiate decision from the user's own supplier quotes — exactly the design in proposal section 5.

## How we narrow to showcase categories (screening funnel)

Each category gets one point per criterion; 5 = ideal showcase for the Stay / Switch / Renegotiate tool.

1. **Comparable data** — the U.S. reports a physical quantity for the HS6 line, so unit CIF can be compared across origins (kg-only lines are excluded).
2. **Real multi-origin market** — ≥3 origins with ≥3% share and China ≥5% share.
3. **Scaled, like-for-like alternative** — nearest competitor has ≥5% share and its unit CIF is within ±30% of China's (so the gap is cost, not product grade).
4. **Tariffs can flip the decision** — the 2024 gap is smaller than the 2025 tariff differential (≈23 pp), so the landed-cost ranking actually changes between regimes.
5. **Switching observed** — China's share fell in 2025.

{md_table(sc.round(1))}

**Recommended showcase set:** {", ".join(f"{r.Category} (HS {r.HS6})" for r in sc[sc.Score>=5].itertuples())} — all four are apparel/footwear lines where Bangladesh or Indonesia sits within 2–15% of China's unit cost, so the 2025 tariff differential flipped the ranking and the 2025 trade data confirms importers moved. Wooden furniture (HS 940360) is the best non-apparel backup (score 4).

## Category table (2024 baseline, sorted by gap)

{md_table(t.round(1))}

Screening table: `shortlist_screening.csv`. Charts: `charts/1_gap_vs_share_change.png`, `charts/2_china_share_shift.png`, `charts/3_showcase_landed_cost.png`. Partner-level data: `partner_level_2023_2026.csv`.
"""
open("out/FINDINGS.md","w").write(md); print(md[:1500])
