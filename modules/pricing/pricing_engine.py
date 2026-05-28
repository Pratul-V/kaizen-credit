"""
pricing_engine.py
The core orchestrator for risk evaluation, counter offers, and financial calculations.
"""
from modules.pricing.risk_engine import get_risk_tier, get_risk_metadata
from modules.pricing.counter_offer_engine import generate_counter_offer
from modules.pricing.emi_calculator import calculate_emi, calculate_total_interest, calculate_total_repayment, calculate_dti

def evaluate_application(form_data, prediction_prob, warnings):
    """
    Evaluate the application, generating counter-offers if necessary.
    """
    # 1. Determine Risk Tier
    risk_tier = get_risk_tier(prediction_prob)
    risk_meta = get_risk_metadata(risk_tier)
    
    requested_amount = float(form_data.get('loan_amnt', 0))
    requested_rate = float(form_data.get('loan_int_rate', 0))
    annual_income = float(form_data.get('person_income', 0))
    requested_tenure = 36 # Assume 36 months if not on form
    
    # 2. Original Financials
    original_emi = calculate_emi(requested_amount, requested_rate, requested_tenure)
    original_dti = calculate_dti(annual_income, original_emi)
    
    original_financials = {
        'loan_amount': requested_amount,
        'interest_rate': requested_rate,
        'tenure_months': requested_tenure,
        'emi': original_emi,
        'total_repayment': calculate_total_repayment(original_emi, requested_tenure),
        'total_interest': calculate_total_interest(calculate_total_repayment(original_emi, requested_tenure), requested_amount),
        'dti': original_dti
    }
    
    # 3. Decision Logic
    action = 'APPROVED'
    counter_offer = None
    
    # We trigger a counter offer if:
    # - Risk is medium or high
    # - Warnings exist requiring mitigation
    # - Original DTI is too high (> 0.40)
    needs_counter = (risk_tier in ['medium', 'high', 'critical']) or (len(warnings) > 0) or (original_dti > 0.40)
    
    if needs_counter:
        counter_offer_terms = generate_counter_offer(risk_tier, form_data)
        if counter_offer_terms:
            action = 'COUNTER-OFFER'
            # Calculate financials for counter offer
            c_amount = counter_offer_terms['loan_amount']
            c_rate = counter_offer_terms['interest_rate']
            c_tenure = counter_offer_terms['tenure_months']
            c_emi = calculate_emi(c_amount, c_rate, c_tenure)
            c_dti = calculate_dti(annual_income, c_emi)
            
            counter_offer = {
                'loan_amount': c_amount,
                'interest_rate': c_rate,
                'tenure_months': c_tenure,
                'emi': c_emi,
                'total_repayment': calculate_total_repayment(c_emi, c_tenure),
                'total_interest': calculate_total_interest(calculate_total_repayment(c_emi, c_tenure), c_amount),
                'dti': c_dti,
                'conditions': counter_offer_terms['conditions']
            }
        else:
            # If we needed a counter but couldn't generate one, reject
            action = 'REJECTED'
            
    # Compile the final result
    result = {
        'action': action,
        'risk_tier': risk_tier,
        'risk_metadata': risk_meta,
        'original_terms': original_financials,
        'counter_offer': counter_offer,
        'warnings': warnings
    }
    
    return result
