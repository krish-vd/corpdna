"""
Utility Functions for CorpDNA
------------------------------
"""

import re
from datetime import datetime


def clean_company_name(name: str) -> str:
    """
    Strip legal suffixes for cleaner web searches.

    Examples:
        'Reliance Industries Ltd.' -> 'Reliance Industries'
        'Apple Inc.' -> 'Apple'
    """
    suffixes = [
        r'\bltd\.?\b', r'\blimited\b', r'\binc\.?\b',
        r'\bcorp\.?\b', r'\bcorporation\b', r'\bplc\b',
    ]
    cleaned = name.strip()
    for suffix in suffixes:
        cleaned = re.sub(suffix, '', cleaned, flags=re.IGNORECASE).strip()
    return cleaned.strip(' .,')


def detect_exchange(name: str) -> str:
    """
    Heuristic to guess which exchange a company is likely listed on.
    Helps the agent target the right search sources.

    Returns: 'NSE/BSE' for Indian, 'NYSE/NASDAQ' for US, 'UNKNOWN' otherwise
    """
    indian_signals = [
        'india', 'indian', 'bharat', 'reliance', 'tata', 'infosys',
        'wipro', 'hdfc', 'icici', 'adani', 'bajaj', 'mahindra',
        'zomato', 'paytm', 'nykaa', 'ltd', 'limited',
    ]
    if any(s in name.lower() for s in indian_signals):
        return "NSE/BSE"
    return "UNKNOWN"


def format_date() -> str:
    """Return current date in readable format."""
    return datetime.now().strftime("%d %B %Y")


def current_year() -> int:
    """Return the current calendar year dynamically."""
    return datetime.now().year


def current_indian_fy() -> str:
    """
    Return the current Indian financial year label dynamically.

    Indian FY runs April to March. If the current month is Jan/Feb/Mar,
    we are still in the FY that started the previous April.

    Examples:
        A date in July 2026 -> 'FY27' (FY April 2026 to March 2027)
        A date in February 2026 -> 'FY26' (FY April 2025 to March 2026)

    Returns:
        FY label as a string, e.g. 'FY27'
    """
    now = datetime.now()
    if now.month >= 4:  # April onwards = new FY
        fy_end_year = now.year + 1
    else:  # Jan, Feb, Mar = still previous FY
        fy_end_year = now.year
    return f"FY{str(fy_end_year)[-2:]}"


def most_recent_completed_fy() -> str:
    """
    Return the most recent COMPLETED Indian financial year.
    This is the FY whose data would actually be available in filings.

    Examples:
        A date in July 2026 -> 'FY26' (FY ending March 2026 is complete)
        A date in February 2026 -> 'FY25' (FY ending March 2025 is complete)

    Returns:
        FY label as a string, e.g. 'FY26'
    """
    now = datetime.now()
    if now.month >= 4:
        fy_end_year = now.year
    else:
        fy_end_year = now.year - 1
    return f"FY{str(fy_end_year)[-2:]}"
