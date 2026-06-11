# CorpDNA

**Corporate Intelligence Agent — Claude Plugin**
Built by Krish Desai

CorpDNA builds a complete intelligence X-ray of any publicly listed company
in minutes — the kind of first-pass due diligence that normally takes an
analyst days. Business model health, financial red flags, management
credibility, competitive position, and an overall risk score.

**Public data only. No API keys. Works out of the box.**

---

## Why publicly listed companies only?

Listed companies have mandatory disclosure requirements — quarterly results,
annual reports, regulatory filings — that provide reliable public data.
This enables 80%+ assessment accuracy. Private companies lack this
disclosure, so accurate analysis would require paid data feeds. CorpDNA
chooses honesty over false coverage.

---

## Commands

Plugin commands are namespaced with the plugin name (`corpdna:`):

| Command | What it does |
|---|---|
| `/corpdna:analyze [company]` | Full five-dimension intelligence X-ray with score (includes a Trend X-Ray PNG) |
| `/corpdna:quick-check [company]` | Business summary + strengths + concerns in 60 sec |
| `/corpdna:visualize [company] [year]` | Generates a standalone Trend X-Ray PNG: revenue vs profit, margin trend, debt-to-equity trend, stock price — for the last 3-5 years up to the year you specify |

## Example

```
/corpdna:analyze Infosys
/corpdna:analyze Reliance Industries
/corpdna:analyze Apple
/corpdna:quick-check HDFC Bank
/corpdna:visualize Tata Motors FY23
```

---

## The Five Dimensions

1. **Business Model X-Ray** — what they do, how they make money, revenue quality
2. **Financial Health** — revenue trend, profitability, debt, margins
3. **Management Credibility** — leadership track record, governance, red flags
4. **Competitive Position** — moat, market share, competitive advantage
5. **Risk Factor Scan** — litigation, concentration, regulatory, macro risks

## Trend X-Ray Chart

Alongside Dimension 2 (and via `/visualize`), CorpDNA generates a
multi-panel PNG covering:

- Revenue vs Net Profit (last 3-5 fiscal years)
- Net Profit Margin trend
- Debt-to-Equity trend, with leverage thresholds marked
- Stock price trend

Only real numbers found via search are plotted — missing years are
skipped, never invented. Each chart includes a source note so you know
where the figures came from.

Requires `matplotlib` (a common, free Python package — no API key).
If it isn't installed: `pip install matplotlib`.

## Scoring

Each dimension scored STRONG (+2) / ADEQUATE (+1) / WEAK (0).
Total range: 0 to 10.
- 8-10 = STRONG PROFILE
- 5-7 = MIXED PROFILE
- 0-4 = WEAK PROFILE

Every report ends with an honest confidence statement based on how much
public data was available.

---

## Accuracy note

CorpDNA describes and assesses companies rather than predicting stock
prices. For large-cap listed companies with abundant public data, assessment
accuracy is high. For smaller companies with sparse data, the agent flags
lower confidence. This honesty is a core design principle.

---

## Setup

```bash
git clone https://github.com/krish-vd/corpdna
cd corpdna
```

Load the plugin (no install step needed — runs directly from the cloned folder):

```bash
claude --plugin-dir .
```

Then try `/corpdna:analyze Infosys` (run `/help` to confirm the commands
are listed under the `corpdna` namespace).

No API keys. The Trend X-Ray chart feature requires `matplotlib`
(`pip install matplotlib` if not already installed) — everything else has
zero dependencies.

---

## License

MIT
