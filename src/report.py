"""
CorpDNA Report Formatter
------------------------
Formats a CorpDNAResult into clean markdown for display.
"""

from src.scoring import CorpDNAResult, DimensionResult
from datetime import datetime


def format_report(result: CorpDNAResult) -> str:
    """
    Format a complete CorpDNA result as markdown.

    Args:
        result: The CorpDNAResult to format

    Returns:
        Clean markdown string ready for display
    """
    date_str = datetime.now().strftime("%d %B %Y")

    lines = [
        "**CORPDNA INTELLIGENCE REPORT**",
        f"**Company:** {result.company_name} "
        f"({result.ticker}, {result.exchange})",
        f"**Generated:** {date_str}",
        "",
        "---",
        "",
    ]

    # Each dimension
    for dim in result.dimensions:
        lines += [
            f"**{dim.name.upper()}**",
            f"Assessment: {dim.label}",
            dim.reasoning,
            "",
            "---",
            "",
        ]

    # Score table
    lines += [
        "**OVERALL CORPDNA SCORE**",
        "",
        "| Dimension | Assessment | Score |",
        "|---|---|---|",
    ]

    for dim in result.dimensions:
        lines.append(f"| {dim.name} | {dim.label} | {dim.score}/2 |")

    lines.append(
        f"| **TOTAL** | | **{result.total_score}/10** |"
    )

    lines += [
        "",
        f"**Verdict:** {result.verdict}",
        "",
        "---",
        "",
        f"**CONFIDENCE:** {result.confidence.value}",
        "",
        "---",
        "",
        "**DISCLAIMER**",
        "This report is generated from publicly available information "
        "using AI research. It is for informational purposes only and "
        "does not constitute investment advice. Always conduct your own "
        "due diligence before making investment decisions.",
    ]

    return "\n".join(lines)


def format_quick_check(
    company_name: str,
    business_summary: str,
    strengths: list,
    concerns: list,
    verdict: str,
) -> str:
    """
    Format a quick check result (condensed version).

    Args:
        company_name: Company name
        business_summary: One paragraph on what the company does
        strengths: List of top 2 strengths
        concerns: List of top 2 concerns
        verdict: One sentence overall verdict

    Returns:
        Clean markdown string
    """
    lines = [
        f"**CORPDNA QUICK CHECK — {company_name}**",
        "",
        "**What they do:**",
        business_summary,
        "",
        "**Top strengths:**",
    ]
    for s in strengths[:2]:
        lines.append(f"- {s}")

    lines += ["", "**Top concerns:**"]
    for c in concerns[:2]:
        lines.append(f"- {c}")

    lines += [
        "",
        f"**Verdict:** {verdict}",
        "",
        "*Run /analyze for the full five-dimension report.*",
    ]

    return "\n".join(lines)
