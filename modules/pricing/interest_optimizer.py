"""
interest_optimizer.py
Calculates risk-adjusted interest rates.
"""
from modules.pricing.underwriting_rules import BASE_INTEREST_RATES

def get_optimized_interest_rate(risk_tier, requested_rate):
    """
    Ensure the interest rate is appropriate for the given risk tier.
    """
    base_rate = BASE_INTEREST_RATES.get(risk_tier, 15.5)
    
    # We never want to offer a rate below our base risk-adjusted rate
    # However, if the user requested a higher rate, we can accept it or average it
    if requested_rate >= base_rate:
        return requested_rate
    
    # If requested is lower than our baseline, we counter with our baseline
    return base_rate
