"""
eligibility_engine.py
Calculates maximum affordable loans based on DTI policies.
"""
from modules.pricing.underwriting_rules import MAX_DTI, MAX_LOAN_AMOUNT
from modules.pricing.emi_calculator import calculate_emi

def get_max_affordable_emi(annual_income, other_monthly_debt=0):
    monthly_income = annual_income / 12
    max_total_debt = monthly_income * MAX_DTI
    max_emi = max(0, max_total_debt - other_monthly_debt)
    return max_emi

def get_max_loan_amount(max_emi, annual_rate, tenure_months):
    """
    Reverse calculation of PMT to find principal.
    P = EMI * ((1 + r)^n - 1) / (r * (1 + r)^n)
    """
    if max_emi <= 0:
        return 0.0
    if annual_rate <= 0:
        return min(max_emi * tenure_months, MAX_LOAN_AMOUNT)
        
    r = (annual_rate / 100) / 12
    n = tenure_months
    
    principal = max_emi * (((1 + r) ** n) - 1) / (r * ((1 + r) ** n))
    return min(round(principal, 2), MAX_LOAN_AMOUNT)

def evaluate_affordability(principal, annual_rate, tenure_months, annual_income, other_monthly_debt=0):
    emi = calculate_emi(principal, annual_rate, tenure_months)
    max_emi = get_max_affordable_emi(annual_income, other_monthly_debt)
    return {
        'is_affordable': emi <= max_emi,
        'requested_emi': emi,
        'max_affordable_emi': max_emi
    }
