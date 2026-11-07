# SourceSwitch AI — Presentation script, slides 1–6
About 380 words, roughly 2.5 minutes at a normal pace. Seconds per slide in brackets; Chinese cue in parentheses.

## Slide 1 · Cover (10 s)
Hi, we’re SourceSwitch AI. One question: when a tariff changes, should you change your supplier country? We built a tool that answers it, and we used real trade data to decide who needs it most.
（開場一句話點出問題與做法）

## Slide 2 · Problem + tool (35 s)
Over the past two years U.S. tariffs went from plus ten to plus one-forty-five percent and back, and about ninety-four percent of that cost landed on importers. Small businesses can’t push it back to suppliers or forward to customers. Every change forces the same question: stay, switch, or renegotiate?

SourceSwitch AI takes an importer’s own quotes, applies the tariff stack by country, and returns the landed cost side by side, the break-even tariff, and one clear flag.
（痛點：轉嫁不了；工具：報價進、旗標出）

## Slide 3 · Dataset (30 s)
Two sources. For consumer goods, UN Comtrade at the HS6 level: thirty-six categories, with CIF and FOB value and physical quantity per origin country. For industrial goods, USITC DataWeb at HTS10: nearly fifty thousand observations, and critically, the actual duties each country paid in 2025. Unit cost is value divided by quantity; landed cost is customs value times one plus tariff, plus freight.
（兩個資料集，一個有實繳關稅）

## Slide 4 · Screening (35 s)
Not every product needs this tool. If China is three hundred percent cheaper on headphones, no tariff changes the answer. So we screened both datasets with the same rule: keep categories where the two cheapest origins are within twenty percent, then keep the ones where three or more countries sit that close. Consumer goods: thirty-six, twenty-three comparable, seven near-tied, four multi-country. Industrial: thirteen curated, seven, five. Why closeness? Because the break-even tariff equals the cost gap. A four percent gap flips on a four-point tariff move.
（篩選邏輯一句話：損益兩平 = 成本差距）

## Slide 5 · Nine categories (25 s)
That leaves nine categories in five industries. Apparel and footwear where China, Indonesia and Bangladesh are within a few percent. Furniture. And on the industrial side, brake hoses, CNC controls, heater parts, bumpers and suspension parts, where the duty China actually paid in 2025 was thirty to fifty points above the cheapest rival. These importers are a few percent away from a different answer. They’re our first customers.
（九類、五產業，工業品有實繳關稅證據）

## Slide 6 · Demo hand-off (15 s)
Meet Jeannie. She runs a small clothing store, buys ten thousand cotton T-shirts an order from China, and the tariff just changed. Vietnam and Bangladesh are on her list. Let’s see what SourceSwitch tells her.
（交棒 demo）

## Backup
- Running long: on slide 4 read only the consumer-goods funnel numbers.
- If asked why 20%: “It is the range a realistic tariff or currency move can cover.”
- If asked about data limits: point to the appendix slide “Dataset limitations”.
