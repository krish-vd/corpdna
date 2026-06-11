---
description: Generate a sophisticated PNG "Trend X-Ray" chart for a publicly listed company — revenue vs net profit, profit margin trend, debt-to-equity trend, and stock price trend over the last several years (or up to a year specified). Use when the user asks for a chart, graph, or visualization of a company's historical financials.
---

# CorpDNA — Trend X-Ray Visualization

If no company name is given in `$ARGUMENTS`, respond with exactly:

"Give me a publicly listed company name (and optionally a year) and I'll
generate its Trend X-Ray chart.
Example: /visualize Infosys
Example: /visualize Tata Motors FY23"

Otherwise, invoke the `corpdna` agent with `$ARGUMENTS` (company name, and
optional target year). The agent should:

1. Confirm the company is publicly listed (find its ticker).
2. Research 3-5 years of revenue, net profit, debt-to-equity, and stock
   price from Tier 1/2 sources, ending at the specified year (or the most
   recent completed period if no year is given).
3. Generate the Trend X-Ray PNG using `src/charts.py` as described in the
   "Trend X-Ray Chart" section of the corpdna agent.
4. Report the PNG path, what each panel shows, and the source(s) of the
   plotted data. If data for a series isn't found, that panel is skipped —
   never invent numbers to fill gaps.
