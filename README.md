# SourceSwitch AI

UCLA Anderson MSBA Vibathon 2026 · Theme 6: Landed Cost

Should a tariff change change your supplier country? SourceSwitch AI screens U.S. import data for product categories where source countries are close on cost, then gives small importers a Stay / Switch / Renegotiate decision with a break-even tariff.

## Links

- **Live prototype:** https://chihyunhung.github.io/sourceswitch-ai/ (GitHub Pages; source: [`prototype/index.html`](prototype/index.html))
- **Pitch deck:** https://claude.ai/artifact/ACNnENnr1Zzc1Hx63xu39L (PDF: [`SourceSwitch_AI_Pitch.pdf`](SourceSwitch_AI_Pitch.pdf))

## Repo map

- `prototype/` — the decision tool (single HTML file, no build step)
- `analysis/FINDINGS.md` — analysis storyline and results
- `analysis/scripts/` — data pulls (UN Comtrade, USITC HTS), screening, sensitivity and charts
- `analysis/charts/` — figures used in the deck
- `analysis/tariff_assumptions.md` — how tariff rates were reconstructed
- `SourceSwitch_AI_Master_Review.xlsx` — master review workbook

Data: UN Comtrade 2024 (HS6) and USITC DataWeb 2025 (HTS10). Tariffs reconstructed from CBP and USTR notices; guidance, not customs advice.
