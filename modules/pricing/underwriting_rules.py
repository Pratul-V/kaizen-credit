"""
underwriting_rules.py
Defines the business policies, risk thresholds, and limits.
"""

MAX_DTI = 0.40  # 40% maximum Debt-to-Income ratio

BASE_INTEREST_RATES = {
    'low': 9.5,
    'medium': 12.5,
    'high': 15.5,
    'critical': 19.5
}

MAX_LOAN_AMOUNT = 50000

RISK_TIERS = {
    'low': (0, 25),
    'medium': (25, 50),
    'high': (50, 75),
    'critical': (75, 100)
}
