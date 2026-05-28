"""
counter_offer_engine.py
Generates intelligent counter-offers for loans that cannot be approved as-is.
"""
from modules.pricing.eligibility_engine import evaluate_affordability, get_max_affordable_emi, get_max_loan_amount
from modules.pricing.interest_optimizer import get_optimized_interest_rate
import math

def generate_counter_offer(risk_tier, form_data):
    """
    Generate a counter offer modifying the requested terms.
    """
    requested_amount = float(form_data.get('loan_amnt', 0))
    requested_rate = float(form_data.get('loan_int_rate', 0))
    annual_income = float(form_data.get('person_income', 0))
    # Default tenure is typically 36 months if not specified
    requested_tenure = 36
    
    revised_rate = get_optimized_interest_rate(risk_tier, requested_rate)
    
    # Set maximum allowed tenure based on risk
    if risk_tier == 'critical':
        max_tenure = 12
    elif risk_tier == 'high':
        max_tenure = 36
    else:
        max_tenure = 60
        
    revised_tenure = min(requested_tenure, max_tenure)
    
    # Check affordability at the revised rate and tenure
    affordability = evaluate_affordability(
        principal=requested_amount, 
        annual_rate=revised_rate, 
        tenure_months=revised_tenure, 
        annual_income=annual_income
    )
    
    revised_amount = requested_amount
    conditions = []
    
    # Force reductions based on risk
    if risk_tier == 'critical':
        risk_cap = requested_amount * 0.20
        if revised_amount > risk_cap:
            revised_amount = risk_cap
            conditions.append("Severe reduction in loan amount due to critical risk profile.")
            conditions.append("Mandatory 100% liquid collateral and co-signer required.")
    elif risk_tier == 'high':
        # High risk shouldn't get more than 60% of their requested amount (or whatever policy dictates)
        risk_cap = requested_amount * 0.6
        if revised_amount > risk_cap:
            revised_amount = risk_cap
            conditions.append("Significant reduction in loan amount due to risk profile.")
            
    elif risk_tier == 'medium':
        risk_cap = requested_amount * 0.85
        if revised_amount > risk_cap:
            revised_amount = risk_cap
            conditions.append("Slight reduction in approval amount based on risk assessment.")
            
    # Apply DTI caps
    if not affordability['is_affordable'] or revised_amount < requested_amount:
        max_emi = affordability['max_affordable_emi']
        dti_max_amount = get_max_loan_amount(max_emi, revised_rate, revised_tenure)
        if dti_max_amount < revised_amount:
            revised_amount = dti_max_amount
            conditions.append("Loan amount reduced to meet maximum Debt-to-Income requirements.")
            
    # Round amount down to nearest 100 for clean numbers
    revised_amount = math.floor(revised_amount / 100) * 100
    
    # Add other conditions
    if risk_tier in ['high', 'medium']:
        conditions.append("Additional income verification required.")
        
    if revised_amount <= 0:
        return None  # Cannot generate a viable counter-offer
        
    return {
        'loan_amount': revised_amount,
        'interest_rate': revised_rate,
        'tenure_months': revised_tenure,
        'conditions': conditions
    }
