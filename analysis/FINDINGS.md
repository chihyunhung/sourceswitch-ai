# SourceSwitch AI — Analysis storyline (data as of 2026-11-06)

**Premise.** When the average import cost of a product is nearly the same across source countries, the sourcing ranking is fragile: a tariff change, a currency move or a freight swing can flip which origin is cheapest. Those are the categories where a Stay / Switch / Renegotiate tool earns its keep. So: **Step 1** screen real U.S. import data for categories whose cross-origin unit costs are close, **Step 2** show that those categories flip under realistic shocks while wide-gap categories do not, **Step 3** build the tool for the kept set.

**Data.** UN Comtrade (U.S. reporter; same Census source as USITC DataWeb), HS6 × origin, 2023–2025 annual + Jan–Feb 2026. Unit CIF = CIF value ÷ reported quantity; freight+insurance = CIF − FOB. Only lines where the U.S. reports a physical quantity are usable (23 of 36 pulled); toys, bags of 4202.92, kitchenware, games, lamps, bedding, porcelain and glassware report weight only and were dropped (Comtrade back-fills their quantity with one uniform unit value, so every origin looks identical). Tariffs: MFN from the USITC HTS API; Section 301 lists; 2025 time-weighted IEEPA rates; 2026 Section 301 forced-labor rates (see `tariff_assumptions.md`).

## Step 1 — Screen by unit-cost closeness (2024, top-6 origins with ≥3% share)

Metric: gap between the two cheapest major origins, and China vs its nearest competitor. **Keep rule: either gap ≤ 10%.**

| HS6 | Category | Unit | Major origins | Cheapest origin | 2nd cheapest | Top-2 gap % | China vs nearest % | China share % | Keep |
|---|---|---|---|---|---|---|---|---|---|
| 610910 | Cotton T-shirts | u | 6 | China | Bangladesh | 2.1 | 2.1 | 6.3 | True |
| 611020 | Cotton sweaters/pullovers | u | 6 | Bangladesh | Pakistan | 2.3 | 5.5 | 14.1 | True |
| 640399 | Leather footwear (other) | 2u | 6 | China | Indonesia | 3.7 | 3.7 | 18.9 | True |
| 610462 | Women's cotton trousers (knit) | u | 6 | China | Indonesia | 4.4 | 4.4 | 10.6 | True |
| 620630 | Women's cotton blouses | u | 6 | China | Bangladesh | 12.0 | 12.0 | 11.3 | False |
| 611030 | Man-made fibre sweaters | u | 6 | China | Honduras | 12.9 | 12.9 | 20.6 | False |
| 620342 | Men's cotton trousers | u | 6 | China | Bangladesh | 15.3 | 15.3 | 6.3 | False |
| 420221 | Handbags, leather | u | 6 | India | Cambodia | 17.3 |  | 0.0 | False |
| 940360 | Wooden furniture (other) | u | 6 | Canada | China | 17.9 | 15.2 | 16.1 | False |
| 640299 | Footwear, rubber/plastic uppers (other) | 2u | 5 | China | Cambodia | 28.1 | 28.1 | 53.0 | False |
| 940350 | Wooden bedroom furniture | u | 5 | Malaysia | China | 31.0 | 0.1 | 4.1 | True |
| 640411 | Sports footwear, textile uppers | 2u | 3 | China | Indonesia | 32.6 | 32.6 | 16.1 | False |
| 640419 | Other footwear, textile uppers | 2u | 4 | China | Cambodia | 35.2 | 35.2 | 56.6 | False |
| 640391 | Leather footwear covering ankle | 2u | 6 | Indonesia | China | 38.6 | 6.7 | 26.8 | True |
| 940429 | Mattresses (other materials) | u | 6 | Cambodia | Singapore | 44.3 |  | 0.0 | False |
| 950490 | Games (board, etc.) | u | 3 | China | Viet Nam | 45.7 | 45.7 | 74.4 | False |
| 620462 | Women's cotton trousers | u | 6 | China | Bangladesh | 53.1 | 53.1 | 16.8 | False |
| 940161 | Upholstered seats, wooden frame | u | 4 | China | Viet Nam | 92.8 | 92.8 | 26.9 | False |
| 420212 | Suitcases/briefcases, plastic/textile | u | 6 | China | Cambodia | 118.2 | 118.2 | 38.1 | False |
| 420222 | Handbags, plastic/textile | u | 6 | China | Viet Nam | 131.8 | 131.8 | 18.7 | False |
| 871200 | Bicycles | u | 4 | China | Cambodia | 324.6 | 324.6 | 41.9 | False |
| 940171 | Upholstered seats, metal frame | u | 5 | China | Viet Nam | 369.3 | 369.3 | 57.6 | False |
| 851830 | Headphones/earphones | u | 2 | China | Viet Nam | 380.7 | 380.7 | 48.3 | False |

**Kept (6):** Cotton T-shirts (HS 610910), Cotton sweaters/pullovers (HS 611020), Leather footwear (other) (HS 640399), Women's cotton trousers (knit) (HS 610462), Wooden bedroom furniture (HS 940350), Leather footwear covering ankle (HS 640391).

Unit costs behind the kept categories:

| HS6 | Category | 2024 unit CIF by origin (share) |
|---|---|---|
| 610910 | Cotton T-shirts | China $1.64 (6%) | Bangladesh $1.68 (11%) | Nicaragua $1.73 (13%) | India $1.97 (9%) | Honduras $2.03 (10%) | Viet Nam $2.74 (6%) |
| 611020 | Cotton sweaters/pullovers | Bangladesh $3.90 (7%) | Pakistan $3.99 (6%) | China $4.36 (14%) | Indonesia $4.60 (6%) | Viet Nam $4.81 (19%) | Cambodia $6.25 (9%) |
| 640399 | Leather footwear (other) | China $16.47 (19%) | Indonesia $17.08 (14%) | India $17.32 (4%) | Viet Nam $19.08 (39%) | Germany $43.28 (3%) | Italy $135.19 (9%) |
| 610462 | Women's cotton trousers (knit) | China $2.87 (11%) | Indonesia $2.99 (13%) | Bangladesh $3.02 (7%) | India $3.30 (6%) | Viet Nam $3.50 (30%) | Cambodia $5.18 (9%) |
| 940350 | Wooden bedroom furniture | Malaysia $50.81 (12%) | China $66.57 (4%) | Italy $66.61 (5%) | Viet Nam $120.36 (55%) | Indonesia $192.82 (5%) |
| 640391 | Leather footwear covering ankle | Indonesia $19.46 (12%) | China $26.96 (27%) | Viet Nam $28.76 (30%) | Bangladesh $33.05 (4%) | Cambodia $33.69 (7%) | Mexico $42.15 (5%) |

## Step 2 — Are near-tied categories really fragile? Shock simulation on 2024 costs

Three shocks applied to the cheapest origin: +10 pp tariff, +10% currency appreciation, and ocean freight +86% (FBX global index $1,850 → $3,440/FEU between Feb and Nov 2026).

| HS6 | Category | Top-2 gap % | +10 pp tariff on cheapest flips? | +10% FX on cheapest flips? | Ocean freight +86% flips? | Cheapest origin 2023→2026 |
|---|---|---|---|---|---|---|
| 610910 | Cotton T-shirts | 2.1 | True | True | False | CHN → CHN → CHN |
| 611020 | Cotton sweaters/pullovers | 2.3 | True | True | False | BGD → BGD → CHN → PAK |
| 640399 | Leather footwear (other) | 3.7 | True | True | False | CHN → CHN → CHN → CHN |
| 610462 | Women's cotton trousers (knit) | 4.4 | True | True | False | CHN → CHN |
| 940350 | Wooden bedroom furniture | 31.0 | False | False | False | MYS → MYS → MYS → ITA |
| 640391 | Leather footwear covering ankle | 38.6 | False | False | False | IDN → IDN |

- Kept (near-tied) categories flip in **1.3 of 3** shocks on average; wide-gap categories flip in **0.2 of 3**.
- Freight alone never flips a ranking: freight+insurance is only 4–12% of FOB for these goods, so an 86% freight jump moves landed cost by ~3–10%. Tariffs and FX are the levers that matter.
- Historical check (2023→2026 unit-cost rankings): the cheapest origin changed at least once in 2 of 6 kept categories vs 3 of 16 wide-gap ones; with this sample size that is suggestive, not significant.

## Step 3 — What the tool should do for these categories

For a kept category the break-even tariff differential is small (2–10 pp), so the tool's job is to (1) take the importer's own supplier quotes (trade unit values are market averages that mix product grades), (2) apply the current tariff stack by origin, (3) report the break-even tariff / FX threshold and a Stay / Switch / Renegotiate flag. Showcase candidates: **Leather footwear (HS 640399, China vs Indonesia, 4% gap)** and **Cotton sweaters (HS 611020, Bangladesh vs China, 2% gap)**; Wooden bedroom furniture (HS 940350, Italy vs China 0.1% gap) is the furniture-themed backup.

## Caveats
- Unit values are HS6 market averages, not supplier quotes; closeness can hide product-mix differences.
- Comtrade's free quota ran out before all 2026 months were fetched; 2026 is Jan–Feb only, and 10 categories have 2023–2024 only.
- Tariff rates are reconstructed from CBP's Jan-2026 overview and broker trackers; spot-check before presenting.

Files: `step1_unit_price_screening.csv` (Step 1 table), `sensitivity_table.csv` / `closeness_ranking.csv` (Step 2), `charts/4_closeness_targets.png` (Step 1 chart), `charts/3_showcase_landed_cost.png`, `partner_level_2023_2026.csv` (origin-level detail), `appendix_hypothesis_test.md` (earlier test of the tariff-switching version of the hypothesis: not supported — share shifts were broad-based and unrelated to the gap).

## Addendum (2026-11-06, merged with the USITC HTS10 dataset)

A teammate's dataset (`SourceSwitch_AI_Master_Review.xlsx`, `master_all_trade_observations.csv`: 49,913 USITC DataWeb observations, 13 curated HTS10 products in automotive parts, electronics and household products, with actual duties collected) was screened with the same rule (origins with ≥3% share; top-2 gap ≤20%; ≥3 origins within 20% of the cheapest) on all origins, not the pre-curated 3–4. Result: 7 near-tied, 5 multi-country: plastic brake hoses (8708.99.81), CNC controls (8537.10.91), heater parts (8516.90.05), bumper parts (8708.10.60), cast-iron suspension parts (8708.80.60). Aluminum road wheels miss by a hair (Morocco, 5% share, is cheapest; only Mexico within 20%). Combined target set: 9 categories in 5 industries. For HTS10 products the tariff applied in the tool is the 2025 effective duty paid per origin (calculated duties ÷ customs value), not a 2026 statutory rate. Files: `step1_hts10_screening_all_origins_ge3pct.csv`, `hts10_origins_ge3pct_2025.json`, `prototype_data_9_categories.json`.
