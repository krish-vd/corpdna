"""
CorpDNA Scoring Engine
----------------------
Defines how each dimension is scored and how the overall CorpDNA score
is computed. The actual research is done by Claude's web search — this
module defines the scoring framework that structures the assessment.

Key concept: MULTI-DIMENSIONAL ASSESSMENT
A company is not good or bad on a single axis. CorpDNA scores five
independent dimensions and combines them. A company can have great
financials but terrible management — the composite captures this nuance.
"""

from dataclasses import dataclass
from enum import Enum
from typing import List


class Assessment(Enum):
    """
    Assessment level for the four quality dimensions.
    (Risk dimension uses RiskLevel instead.)
    """
    STRONG = 2
    ADEQUATE = 1
    WEAK = 0


class RiskLevel(Enum):
    """
    Risk assessment. Note: LOW risk scores HIGH because low risk is good.
    """
    LOW = 2       # low risk = good = high score
    MODERATE = 1
    HIGH = 0      # high risk = bad = low score


class Confidence(Enum):
    """How much public data was available to support the analysis."""
    HIGH = "HIGH"       # large-cap, abundant data
    MEDIUM = "MEDIUM"   # mid-cap, moderate data
    LOWER = "LOWER"     # small-cap, sparse data


@dataclass
class DimensionResult:
    """
    Result of analyzing one dimension.

    Attributes:
        name: Dimension name
        score: 0, 1, or 2
        label: STRONG/ADEQUATE/WEAK or LOW/MODERATE/HIGH for risk
        reasoning: One sentence explaining the assessment
    """
    name: str
    score: int
    label: str
    reasoning: str


@dataclass
class CorpDNAResult:
    """
    The complete CorpDNA assessment.

    Attributes:
        company_name: Company analyzed
        ticker: Stock ticker symbol
        exchange: Stock exchange (NSE/BSE/NYSE/NASDAQ)
        dimensions: List of all five dimension results
        total_score: Sum of dimension scores, 0 to 10
        verdict: STRONG / MIXED / WEAK profile
        confidence: Data availability confidence level
    """
    company_name: str
    ticker: str
    exchange: str
    dimensions: List[DimensionResult]
    total_score: int
    verdict: str
    confidence: Confidence


# The five standard dimensions
DIMENSIONS = [
    "Business Model",
    "Financial Health",
    "Management Credibility",
    "Competitive Position",
    "Risk Profile",
]


def compute_verdict(total_score: int) -> str:
    """
    Convert a total score (0-10) into an overall verdict.

    Scoring logic:
        8-10 = STRONG PROFILE — healthy across most dimensions
        5-7  = MIXED PROFILE — strengths and concerns both present
        0-4  = WEAK PROFILE — significant concerns across dimensions

    Args:
        total_score: Sum of five dimension scores (0 to 10)

    Returns:
        Verdict string with explanation
    """
    if total_score >= 8:
        return (
            "STRONG PROFILE — healthy business model, sound financials, "
            "credible management, defensible competitive position, and "
            "manageable risk on public information."
        )
    elif total_score >= 5:
        return (
            "MIXED PROFILE — both strengths and concerns present. Some "
            "dimensions are solid while others warrant caution. Examine "
            "the weak areas before any decision."
        )
    else:
        return (
            "WEAK PROFILE — significant concerns across multiple "
            "dimensions. Multiple red flags present. Substantial caution "
            "and deeper due diligence strongly recommended."
        )


def build_result(
    company_name: str,
    ticker: str,
    exchange: str,
    dimensions: List[DimensionResult],
    confidence: Confidence,
) -> CorpDNAResult:
    """
    Assemble the final CorpDNA result from five dimension assessments.

    Args:
        company_name: Name of company
        ticker: Stock ticker
        exchange: Exchange name
        dimensions: List of exactly 5 DimensionResult objects
        confidence: Data availability confidence

    Returns:
        Complete CorpDNAResult with total score and verdict
    """
    total = sum(d.score for d in dimensions)
    verdict = compute_verdict(total)

    return CorpDNAResult(
        company_name=company_name,
        ticker=ticker,
        exchange=exchange,
        dimensions=dimensions,
        total_score=total,
        verdict=verdict,
        confidence=confidence,
    )
