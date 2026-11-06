# SourceSwitch AI — Hypothesis test (data as of 2026-11-06)

**Hypothesis.** Categories where the average import cost gap between source countries is small should see their cost ranking flip more easily when tariffs change.

**Data.** UN Comtrade (U.S. as reporter; same Census source as USITC DataWeb), HS6, general imports by origin: CIF value, FOB value and *reported* quantity, 2023–2025 annual plus 2026 monthly YTD. Unit CIF = CIF value ÷ quantity. Freight+insurance = CIF − FOB. Categories where the U.S. reports no quantity (toys, bags, plastic & steel kitchenware, games, lamps, bedding…) were **excluded** because Comtrade back-fills their quantity with a uniform estimated unit value, which makes every origin look identical. Tariffs: MFN from the USITC HTS REST API; Section 301 list rates (assumed from USTR lists); 2025 = time-weighted average of IEEPA fentanyl/reciprocal rates plus Section 232 furniture; 2026 = Section 301 forced-labor tariffs in force since 2026-07-24. See `tariff_assumptions.md`.

**Sample.** 12 HS6 categories with reported quantities and China ≥3% share in 2024.

## Results

| Test | Result |
|---|---|
| 2024 cost gap (China vs nearest competitor) < 2025 extra-tariff differential (≈23 pp) → predicted rank flip | 5 of 12 categories predicted to flip |
| Actual landed-cost rank flip in 2025 (2025 unit values + 2025 tariffs) | 3 of 12 |
| China lost U.S. import share 2024→2025 | 12 of 12 categories; mean -7.8 pp; mean relative loss -32% of 2024 share |
| Spearman: \|gap\| vs Δ China share (pp) | rho = -0.83, p = 0.001 (opposite sign to hypothesis) |
| Spearman: China 2024 share vs Δ China share (pp) | rho = -0.86, p = 0.000 (initial share dominates) |
| Spearman: \|gap\| vs *relative* share loss (controls for initial share) | rho = -0.03, p = 0.931 (no relationship) |
| Mean relative loss, predicted-flip vs no-flip group | -33% vs -32% |

**Verdict: not supported as stated.** With market-average unit values, small cost gaps did *not* predict larger sourcing shifts. Sourcing moved away from China in every category in 2025 regardless of the gap, and the biggest absolute moves were in categories where China was by far the cheapest per unit (headphones, upholstered seats) — which exposes the real problem: trade unit values mix product grades (Vietnam ships premium earbuds, China ships budget ones), so they cannot measure a supplier-level cost gap.

**What the data does support.**
1. The tariff differential China faced vs. its nearest competitor jumped from 0 pp (Section 301 only, already in the 2024 baseline) to ~23 pp in 2025 (time-weighted), then collapsed back to ~1 pp under the 2026 regime — yet 2026 YTD shares show no return to China. Switching is sticky.
2. In 5 of 12 categories the 2024 cost gap was smaller than the 2025 tariff shock, so a tariff-only landed-cost model *would* have flipped the ranking — the break-even threshold is the right quantity for the tool to surface.
3. Freight+insurance is a small share of landed cost for these goods (China median 6.7% of FOB), so tariffs, not freight, drive the switching decision.

**Implication for the product.** Use trade data as a market benchmark for the *shortlist* (which origins have scale, what the tariff differential is), but compute the Stay / Switch / Renegotiate decision from the user's own supplier quotes — exactly the design in proposal section 5.

## How we narrow to showcase categories (screening funnel)

Each category gets one point per criterion; 5 = ideal showcase for the Stay / Switch / Renegotiate tool.

1. **Comparable data** — the U.S. reports a physical quantity for the HS6 line, so unit CIF can be compared across origins (kg-only lines are excluded).
2. **Real multi-origin market** — ≥3 origins with ≥3% share and China ≥5% share.
3. **Scaled, like-for-like alternative** — nearest competitor has ≥5% share and its unit CIF is within ±30% of China's (so the gap is cost, not product grade).
4. **Tariffs can flip the decision** — the 2024 gap is smaller than the 2025 tariff differential (≈23 pp), so the landed-cost ranking actually changes between regimes.
5. **Switching observed** — China's share fell in 2025.

| HS6 | Category | Score | Multi-origin | Scaled similar alt. | Tariff flips rank | Switch observed | CN share 2024 % | Nearest competitor | Comp. share % | |Gap| % | Δ CN share 24→25 pp |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 610910 | Cotton T-shirts | 5 | True | True | True | True | 6.3 | Bangladesh | 10.9 | 2.1 | -2.1 |
| 640399 | Leather footwear (other) | 5 | True | True | True | True | 18.9 | Indonesia | 14.0 | 3.7 | -5.6 |
| 611020 | Cotton sweaters/pullovers | 5 | True | True | True | True | 14.1 | Indonesia | 6.2 | 5.5 | -5.4 |
| 620342 | Men's cotton trousers | 5 | True | True | True | True | 6.3 | Bangladesh | 34.5 | 15.3 | -2.9 |
| 940360 | Wooden furniture (other) | 4 | True | False | True | True | 16.1 | Italy | 4.8 | 5.9 | -3.0 |
| 640299 | Footwear, rubber/plastic uppers (other) | 3 | True | False | False | True | 53.0 | Cambodia | 3.5 | 28.1 | -13.4 |
| 950490 | Games (board, etc.) | 3 | True | False | False | True | 74.4 | Viet Nam | 5.1 | 45.7 | -6.9 |
| 940161 | Upholstered seats, wooden frame | 3 | True | False | False | True | 26.9 | Viet Nam | 45.8 | 92.8 | -11.5 |
| 420222 | Handbags, plastic/textile | 3 | True | False | False | True | 18.7 | Viet Nam | 5.9 | 131.8 | -6.8 |
| 940171 | Upholstered seats, metal frame | 3 | True | False | False | True | 57.6 | Viet Nam | 13.0 | 369.3 | -6.9 |
| 940350 | Wooden bedroom furniture | 2 | False | False | False | True | 4.1 | Italy | 5.0 | 0.1 | -1.6 |
| 620462 | Women's cotton trousers | 2 | True | False | False | False | 16.8 | Bangladesh | 19.0 | 53.1 |  |
| 851830 | Headphones/earphones | 2 | False | False | False | True | 48.3 | Viet Nam | 43.3 | 380.7 | -27.8 |

**Recommended showcase set:** Cotton T-shirts (HS 610910), Leather footwear (other) (HS 640399), Cotton sweaters/pullovers (HS 611020), Men's cotton trousers (HS 620342) — all four are apparel/footwear lines where Bangladesh or Indonesia sits within 2–15% of China's unit cost, so the 2025 tariff differential flipped the ranking and the 2025 trade data confirms importers moved. Wooden furniture (HS 940360) is the best non-apparel backup (score 4).

## Category table (2024 baseline, sorted by gap)

| HS6 | Category | CN share 2024 % | CN unit CIF $ | Nearest competitor | Comp. unit CIF $ | Gap % | CN freight+ins % | CN tariff 2024 % | CN tariff 2025 avg % | CN tariff 2026 % | Predicted flip (2025) | Actual landed-rank flip (2025) | CN share 2025 % | CN share 2026YTD % | Δ share 24→25 pp | Rel. loss % |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 940350 | Wooden bedroom furniture | 4.1 | 66.6 | Italy | 66.6 | 0.1 | 11.7 | 25.0 | 59.3 | 37.5 | False | False | 2.5 | 2.2 | -1.6 | -39.1 |
| 610910 | Cotton T-shirts | 6.3 | 1.6 | Bangladesh | 1.7 | 2.1 | 6.3 | 24.0 | 58.3 | 36.5 | True | True | 4.2 |  | -2.1 | -32.8 |
| 640399 | Leather footwear (other) | 18.9 | 16.5 | Indonesia | 17.1 | 3.7 | 3.7 | 16.0 | 50.3 | 28.5 | True | False | 13.3 | 12.2 | -5.6 | -29.8 |
| 611020 | Cotton sweaters/pullovers | 14.1 | 4.4 | Indonesia | 4.6 | 5.5 | 5.6 | 24.0 | 58.3 | 36.5 | True | True | 8.7 | 7.4 | -5.4 | -38.3 |
| 940360 | Wooden furniture (other) | 16.1 | 18.6 | Italy | 17.5 | -5.9 | 20.6 | 25.0 | 59.3 | 37.5 | True | False | 13.1 | 15.2 | -3.0 | -18.5 |
| 620342 | Men's cotton trousers | 6.3 | 5.2 | Bangladesh | 6.0 | 15.3 | 4.9 | 24.1 | 58.4 | 36.6 | True | False | 3.4 | 2.2 | -2.9 | -45.8 |
| 640299 | Footwear, rubber/plastic uppers (other) | 53.0 | 6.0 | Cambodia | 7.7 | 28.1 | 5.7 | 27.5 | 61.8 | 40.0 | False | False | 39.6 |  | -13.4 | -25.3 |
| 950490 | Games (board, etc.) | 74.4 | 4.8 | Viet Nam | 6.9 | 45.7 | 7.8 | 7.5 | 41.8 | 20.0 | False | True | 67.5 |  | -6.9 | -9.3 |
| 940161 | Upholstered seats, wooden frame | 26.9 | 72.5 | Viet Nam | 139.7 | 92.8 | 20.5 | 25.0 | 64.7 | 50.0 | False | False | 15.3 | 9.1 | -11.5 | -42.9 |
| 420222 | Handbags, plastic/textile | 18.7 | 3.9 | Viet Nam | 9.1 | 131.8 | 7.2 | 42.6 | 76.9 | 55.1 | False | False | 11.9 |  | -6.8 | -36.5 |
| 940171 | Upholstered seats, metal frame | 57.6 | 20.8 | Viet Nam | 97.4 | 369.3 | 17.7 | 25.0 | 59.3 | 37.5 | False | False | 50.7 | 49.0 | -6.9 | -12.0 |
| 851830 | Headphones/earphones | 48.3 | 10.4 | Viet Nam | 50.0 | 380.7 | 2.6 | 7.5 | 41.8 | 20.0 | False | False | 20.5 | 17.6 | -27.8 | -57.6 |

Screening table: `shortlist_screening.csv`. Charts: `charts/1_gap_vs_share_change.png`, `charts/2_china_share_shift.png`, `charts/3_showcase_landed_cost.png`. Partner-level data: `partner_level_2023_2026.csv`.
