"""
emi_calculator.py
Financial mathematics for loan calculations.
"""

def calculate_emi(principal, annual_rate, tenure_months):
    """
    Calculate Equated Monthly Installment (EMI).
    """
    if principal <= 0 or tenure_months <= 0:
        return 0.0
    if annual_rate <= 0:
        return principal / tenure_months
        
    r = (annual_rate / 100) / 12  # Monthly interest rate
    n = tenure_months
    
    # PMT Formula: P * r * (1 + r)^n / ((1 + r)^n - 1)
    emi = principal * r * ((1 + r) ** n) / (((1 + r) ** n) - 1)
    return round(emi, 2)

def calculate_dti(income, emi, other_monthly_debt=0):
    """
    Calculate Debt-to-Income ratio.
    """
    if income <= 0:
        return 1.0  # 100% or more
    monthly_income = income / 12
    return round((emi + other_monthly_debt) / monthly_income, 4)

def calculate_total_repayment(emi, tenure_months):
    """
    Calculate total amount to be repaid.
    """
    return round(emi * tenure_months, 2)

def calculate_total_interest(total_repayment, principal):
    """
    Calculate total interest to be paid.
    """
    return round(max(0, total_repayment - principal), 2)
