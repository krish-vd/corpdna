"""
CorpDNA Trend Chart Generator
------------------------------
Renders a multi-panel "Trend X-Ray" PNG from historical financial data
the agent has gathered via web search. Pure matplotlib, no API keys,
no network calls — this module only visualizes numbers it is given.

Design principle: GARBAGE IN, GARBAGE OUT IS VISIBLE
Every number plotted must trace back to a real source the agent found.
This module does not estimate, interpolate missing years, or invent data —
it plots exactly what it is handed and skips panels with insufficient data.

Usage (CLI):
    python3 src/charts.py --data-file data.json --output corpdna_chart.png

data.json shape:
{
  "company_name": "Infosys",
  "ticker": "INFY",
  "exchange": "NSE/BSE",
  "years": ["FY22", "FY23", "FY24", "FY25", "FY26"],
  "revenue": [121641, 146767, 153670, 162990, null],
  "net_profit": [22110, 24108, 26233, 26283, null],
  "debt_to_equity": [0.09, 0.10, 0.08, 0.07, null],
  "stock_price": [1450, 1320, 1580, 1620, 1750],
  "currency": "INR Cr",
  "source_note": "Figures from company annual reports / Screener.in, cross-checked.",
  "generated_for_year": "FY26"
}

Any of revenue / net_profit / debt_to_equity / stock_price may be omitted
or contain nulls for years where data was not found. Panels for series
with fewer than 2 valid points are skipped.
"""

import argparse
import json
import sys
import textwrap
from datetime import datetime


def _valid_series(years, values):
    """Return (years, values) filtered to entries where value is not None."""
    pairs = [(y, v) for y, v in zip(years, values or []) if v is not None]
    if len(pairs) < 2:
        return [], []
    ys, vs = zip(*pairs)
    return list(ys), list(vs)


def generate_trend_chart(data: dict, output_path: str) -> str:
    """
    Generate a multi-panel CorpDNA Trend X-Ray PNG.

    Args:
        data: Dict matching the shape documented in the module docstring.
        output_path: File path to write the PNG to.

    Returns:
        The output_path, on success.

    Raises:
        ValueError: if no plottable series are found at all.
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.ticker as mticker

    company = data.get("company_name", "Unknown Company")
    ticker = data.get("ticker", "—")
    exchange = data.get("exchange", "—")
    currency = data.get("currency", "")
    years = data.get("years", [])
    source_note = data.get("source_note", "")
    generated_for_year = data.get("generated_for_year", "")

    revenue_y, revenue_v = _valid_series(years, data.get("revenue"))
    profit_y, profit_v = _valid_series(years, data.get("net_profit"))
    de_y, de_v = _valid_series(years, data.get("debt_to_equity"))
    price_y, price_v = _valid_series(years, data.get("stock_price"))

    # Margin derived only where both revenue and profit exist for the same year
    margin_y, margin_v = [], []
    if revenue_y and profit_y:
        rev_map = dict(zip(revenue_y, revenue_v))
        prof_map = dict(zip(profit_y, profit_v))
        for y in years:
            if y in rev_map and y in prof_map and rev_map[y]:
                margin_y.append(y)
                margin_v.append(round(100 * prof_map[y] / rev_map[y], 2))

    panels = []
    if revenue_y or profit_y:
        panels.append("revenue_profit")
    if margin_y and len(margin_y) >= 2:
        panels.append("margin")
    if de_y:
        panels.append("debt_equity")
    if price_y:
        panels.append("stock_price")

    if not panels:
        raise ValueError(
            "No plottable series found — at least two years of data for "
            "one of revenue, net_profit, debt_to_equity, or stock_price "
            "is required."
        )

    plt.style.use("seaborn-v0_8-darkgrid")
    n = len(panels)
    cols = 2
    rows = (n + 1) // 2
    fig, axes = plt.subplots(rows, cols, figsize=(13, 5.2 * rows))
    fig.patch.set_facecolor("#0f1115")
    if n == 1:
        axes = [axes]
    else:
        axes = axes.flatten()

    accent = "#3ddc97"
    accent2 = "#f25f5c"
    accent3 = "#5fa8d3"
    text_color = "#e6e6e6"

    for ax in axes:
        ax.set_facecolor("#1a1d23")
        ax.tick_params(colors=text_color)
        for spine in ax.spines.values():
            spine.set_color("#3a3f4b")
        ax.title.set_color(text_color)
        ax.xaxis.label.set_color(text_color)
        ax.yaxis.label.set_color(text_color)

    idx = 0

    if "revenue_profit" in panels:
        ax = axes[idx]
        idx += 1
        width = 0.38
        rev_map = dict(zip(revenue_y, revenue_v))
        prof_map = dict(zip(profit_y, profit_v))
        combined_years = [y for y in years if y in rev_map or y in prof_map]
        x = range(len(combined_years))
        all_values = []
        if revenue_y:
            rev_bar_v = [rev_map.get(y, float("nan")) for y in combined_years]
            all_values += [v for v in rev_bar_v if v == v]
            ax.bar(
                [i - width / 2 for i in x], rev_bar_v, width=width,
                label=f"Revenue ({currency})" if currency else "Revenue",
                color=accent3,
            )
        if profit_y:
            prof_bar_v = [prof_map.get(y, float("nan")) for y in combined_years]
            all_values += [v for v in prof_bar_v if v == v]
            ax.bar(
                [i + width / 2 for i in x], prof_bar_v, width=width,
                label=f"Net Profit ({currency})" if currency else "Net Profit",
                color=accent,
            )
        ax.set_xticks(list(x))
        ax.set_xticklabels(combined_years)
        if all_values:
            ax.set_ylim(0, max(all_values) * 1.18)
        ax.set_title("Revenue vs Net Profit", fontsize=13, fontweight="bold")
        ax.legend(facecolor="#1a1d23", labelcolor=text_color, edgecolor="#3a3f4b", loc="upper right")
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))

    if "margin" in panels:
        ax = axes[idx]
        idx += 1
        ax.plot(margin_y, margin_v, marker="o", linewidth=2.5, color=accent,
                markersize=8, markerfacecolor="#0f1115", markeredgewidth=2)
        span = max(margin_v) - min(margin_v) or 1
        ax.set_ylim(min(margin_v) - 0.25 * span, max(margin_v) + 0.25 * span)
        for x, y in zip(margin_y, margin_v):
            ax.annotate(f"{y:.1f}%", (x, y), textcoords="offset points",
                         xytext=(0, 12), ha="center", color=text_color, fontsize=9)
        ax.set_title("Net Profit Margin Trend (%)", fontsize=13, fontweight="bold")
        ax.set_ylabel("Margin %")

    if "debt_equity" in panels:
        ax = axes[idx]
        idx += 1
        colors = [accent2 if v > 1.0 else accent for v in de_v]
        ax.bar(de_y, de_v, color=colors)
        ax.axhline(1.0, color="#f2b134", linestyle="--", linewidth=1.5,
                    label="Elevated leverage threshold (1.0)")
        ax.axhline(2.0, color=accent2, linestyle="--", linewidth=1.5,
                    label="High leverage threshold (2.0)")
        top = max(2.0, max(de_v)) * 1.35
        ax.set_ylim(0, top)
        ax.set_title("Debt-to-Equity Ratio Trend", fontsize=13, fontweight="bold")
        ax.set_ylabel("D/E ratio")
        ax.legend(facecolor="#1a1d23", labelcolor=text_color, edgecolor="#3a3f4b",
                  fontsize=8, loc="upper right")

    if "stock_price" in panels:
        ax = axes[idx]
        idx += 1
        ax.plot(price_y, price_v, marker="o", linewidth=2.5, color=accent3,
                markersize=8, markerfacecolor="#0f1115", markeredgewidth=2)
        ax.fill_between(range(len(price_y)), price_v, color=accent3, alpha=0.12)
        ax.set_title("Stock Price Trend", fontsize=13, fontweight="bold")
        ax.set_ylabel("Price")

    # Hide any unused axes (when n is odd)
    for j in range(idx, len(axes)):
        axes[j].axis("off")

    title_year = f" — Trend through {generated_for_year}" if generated_for_year else ""
    fig.suptitle(
        f"CorpDNA Trend X-Ray: {company} ({ticker}, {exchange}){title_year}",
        fontsize=16, fontweight="bold", color=text_color, y=0.99,
    )

    footer = source_note or "Source: figures gathered via CorpDNA web research — verify against primary filings."
    footer += f"  |  Generated {datetime.now().strftime('%d %B %Y')}"
    footer = footer.replace("$", r"\$")
    wrapped = textwrap.wrap(footer, width=140)
    bottom_margin = 0.02 + 0.014 * len(wrapped)
    for i, line in enumerate(reversed(wrapped)):
        fig.text(0.5, 0.005 + i * 0.016, line, ha="center", fontsize=8.5, color="#9aa0ab")

    fig.tight_layout(rect=[0, bottom_margin, 1, 0.96])
    fig.savefig(output_path, dpi=200, facecolor=fig.get_facecolor())
    plt.close(fig)
    return output_path


def _main():
    parser = argparse.ArgumentParser(description="Generate a CorpDNA Trend X-Ray PNG.")
    parser.add_argument("--data-file", help="Path to a JSON file with chart data.")
    parser.add_argument("--data-json", help="Inline JSON string with chart data.")
    parser.add_argument("--output", required=True, help="Output PNG path.")
    args = parser.parse_args()

    if args.data_file:
        with open(args.data_file, "r") as f:
            data = json.load(f)
    elif args.data_json:
        data = json.loads(args.data_json)
    else:
        parser.error("Provide --data-file or --data-json")

    try:
        path = generate_trend_chart(data, args.output)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Chart written to {path}")


if __name__ == "__main__":
    _main()
