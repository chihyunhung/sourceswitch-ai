# Tariff assumptions used in the analysis

All rates are additional ad-valorem duties on top of MFN (MFN from USITC HTS REST API, representative 8-digit line per HS6). Verify before quoting: these are reconstructed from CBP's "U.S. Tariff Overview" (updated 2026-01-14), trade-compliance trackers (Dimerco, Koalagains, Zonos, updated Sep–Oct 2026) and USTR Section 301 lists.

## Regime R0 — 2024 baseline
- China: Section 301 (List 1–3 = 25%: furniture 9401/9403, bags 4202, lamps 9405, kitchenware 7323/3924, porcelain 6911, glassware 7013; List 4A = 7.5%: apparel 61/62, most footwear 64, headphones 8518.30, games 9504; List 4B never implemented = 0%: toys 9503).
- All other origins: 0% additional. Mexico/Canada assumed USMCA-qualifying.

## Regime R1 — 2025, time-weighted average of the IEEPA era
- China: 301 + 34.3 pp average (fentanyl 10% from Feb 4, 20% from Mar 4; reciprocal 125% Apr 9–May 13, 10% from May 14; fentanyl cut to 10% Nov 10).
- Vietnam 11.5 (10% Apr 5–Aug 6, 20% from Aug 7); Indonesia/Malaysia/Thailand/Cambodia/Philippines 11.1 (10% then 19%); India 22.4 (10% → 25% Aug 7 → 50% Aug 27); Bangladesh/Sri Lanka/Taiwan 11.5; EU/Japan/Korea: 10% Apr–Aug then "higher of MFN or 15%"; UK 7.4 (10% from Apr 5); Brazil 24.2; Nicaragua 10.6; Mexico/Canada 0 (USMCA); all others 7.4 (10% from Apr 5).
- Section 232 upholstered wooden seats (9401.61): 25% on all origins from Oct 14, 2025 → 5.4 pp on a full-year basis. Unstacking rules approximated.

## Regime R2 — current, since 2026-07-24 (Section 301 "forced labor" tariffs replaced the Section 122 surcharge after IEEPA was struck down 2026-02-20)
- China: 301 + 12.5; Vietnam 12.5; Thailand 12.5; Indonesia/Malaysia/India/Cambodia 10; Mexico/Canada 0 (USMCA); EU/Taiwan all-in 10%; Japan/Korea all-in 12.5%; UK +10; Brazil 37.5; others 10 (assumed).
- 9401.61: Section 232 at 25% for all origins (China 25% 301 + 25% 232 = 50%; EU/JP/KR 15%; UK 10%). Section 232 goods are exempt from the 2026 Section 301 forced-labor tariffs.

## Known simplifications
- Unit values are market averages per HS6 and mix product grades; they are a benchmark, not a supplier quote.
- USMCA qualification assumed for Mexico/Canada; Section 301 exclusions and AD/CVD orders (e.g., wooden bedroom furniture from China, mattresses) are not modelled.
- Tariff coverage is by regime, not by entry date; 2026 YTD trade data (Jan–Sep where available) straddles the IEEPA → Section 122 → Section 301 transitions.
