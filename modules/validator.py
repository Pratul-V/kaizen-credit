"""
Enterprise-grade input validation for credit risk applications.
Separates hard errors (block prediction) from soft warnings (flag for review).
"""

from config import VALIDATION, WARNING_THRESHOLDS


def validate_hard(form_data):
    """
    Hard validation — any error here blocks the prediction entirely.
    
    Args:
        form_data: dict with parsed numeric values and raw string fields.
    
    Returns:
        list[str]: List of error messages. Empty list means all checks passed.
    """
    errors = []
    
    name = form_data.get('person_name', '')
    cust_id = form_data.get('customer_id', '')

    if not name or (isinstance(name, str) and not name.strip()):
        errors.append("Invalid Input: Applicant Name is required.")
    if not cust_id or (isinstance(cust_id, str) and not cust_id.strip()):
        errors.append("Invalid Input: Customer ID is required.")
        
    age = form_data.get('person_age', 0)
    income = form_data.get('person_income', 0)
    emp_length = form_data.get('person_emp_length', 0)
    loan_amnt = form_data.get('loan_amnt', 0)
    cred_hist_length = form_data.get('cb_person_cred_hist_length', 0)
    int_rate = form_data.get('loan_int_rate', 0)
    cibil_score = form_data.get('cibil_score', 0)

    # Age range check
    if age < VALIDATION['age_min'] or age > VALIDATION['age_max']:
        errors.append(
            f"Invalid Input: Age ({age}) must be between "
            f"{VALIDATION['age_min']} and {VALIDATION['age_max']}."
        )

    # Income must be positive
    if income < VALIDATION['income_min']:
        errors.append("Invalid Input: Annual Income must be greater than 0.")

    # Loan amount must be positive
    if loan_amnt < VALIDATION['loan_amount_min']:
        errors.append("Invalid Input: Loan Amount must be greater than 0.")

    # Employment length cannot exceed working years
    if age >= VALIDATION['age_min'] and emp_length > (age - VALIDATION['age_min']):
        errors.append(
            f"Invalid Input: Employment length ({emp_length} yrs) exceeds "
            f"realistic working age for a {age}-year-old."
        )

    # Credit history length cannot exceed years since age of majority
    if age >= VALIDATION['age_min'] and cred_hist_length > (age - VALIDATION['age_min']):
        errors.append(
            f"Invalid Input: Credit history length ({cred_hist_length} yrs) exceeds "
            f"realistic credit age for a {age}-year-old."
        )
        
    # DTI check
    if income > 0 and (loan_amnt / income) > 0.60:
        errors.append(
            f"Invalid Input: Debt-to-Income (DTI) ratio exceeds 60% "
            f"(Suspicious DTI for requested loan)."
        )

    # Interest rate sanity check
    if int_rate < VALIDATION['int_rate_min'] or int_rate > VALIDATION['int_rate_max']:
        errors.append(
            f"Invalid Input: Interest rate ({int_rate}%) must be between "
            f"{VALIDATION['int_rate_min']}% and {VALIDATION['int_rate_max']}%."
        )

    # CIBIL Score check
    if cibil_score < VALIDATION.get('cibil_min', 300) or cibil_score > VALIDATION.get('cibil_max', 900):
        if cibil_score != -1 and cibil_score != 0: # -1/0 allowed for no history
            errors.append(
                f"Invalid Input: CIBIL score ({cibil_score}) must be between 300 and 900, or 0/-1 for no history."
            )

    return errors


def validate_soft(form_data):
    """
    Soft validation — generates advisory warnings that flag suspicious patterns
    but do NOT block the prediction.
    
    Args:
        form_data: dict with parsed numeric values.
    
    Returns:
        list[str]: List of warning messages.
    """
    warnings = []
    t = WARNING_THRESHOLDS

    age = form_data.get('person_age', 0)
    income = form_data.get('person_income', 0)
    loan_amnt = form_data.get('loan_amnt', 0)
    cred_hist_length = form_data.get('cb_person_cred_hist_length', 0)
    int_rate = form_data.get('loan_int_rate', 0)

    # Loan-to-income ratio
    if income > 0 and loan_amnt > (t['loan_to_income_ratio'] * income):
        warnings.append(
            f"Loan amount (₹{loan_amnt:,.0f}) exceeds "
            f"{int(t['loan_to_income_ratio'] * 100)}% of annual income (₹{income:,.0f})."
        )

    # Disproportionate request
    if income < t['low_income_threshold'] and loan_amnt > t['low_income_high_loan']:
        warnings.append(
            "Disproportionate request: Very low income with large loan request."
        )

    # Suspiciously long credit history for young applicants
    if age < t['young_age_threshold'] and cred_hist_length > t['young_credit_hist_max']:
        warnings.append(
            f"Suspiciously long credit history ({cred_hist_length} yrs) "
            f"for applicant's age ({age})."
        )

    # High interest rate indicator
    if int_rate > t['high_interest_rate']:
        warnings.append(
            f"High-risk indicator: Requested interest rate ({int_rate}%) "
            f"is extremely high (>{t['high_interest_rate']}%)."
        )

    return warnings


def parse_numeric_fields(raw_form):
    """
    Parse raw form strings into typed numeric values.
    
    Args:
        raw_form: dict of raw string values from request.form
    
    Returns:
        tuple: (parsed_dict, error_message_or_None)
    """
    try:
        parsed = {
            'person_name': raw_form.get('person_name', '').strip(),
            'customer_id': raw_form.get('customer_id', '').strip(),
            'person_age': float(raw_form.get('person_age', 0)),
            'person_income': float(raw_form.get('person_income', 0)),
            'person_emp_length': float(raw_form.get('person_emp_length', 0)),
            'loan_amnt': float(raw_form.get('loan_amnt', 0)),
            'loan_int_rate': float(raw_form.get('loan_int_rate', 0)),
            'cb_person_cred_hist_length': float(raw_form.get('cb_person_cred_hist_length', 0)),
            'cibil_score': float(raw_form.get('cibil_score', 0)),
            # Categorical fields pass through as strings
            'person_home_ownership': raw_form.get('person_home_ownership', 'RENT'),
            'loan_intent': raw_form.get('loan_intent', 'PERSONAL'),
            'cb_person_default_on_file': raw_form.get('cb_person_default_on_file', 'N'),
        }
        return parsed, None
    except (ValueError, TypeError) as e:
        return None, (
            "Invalid Format: Please ensure all numeric fields contain "
            "valid numbers without special characters."
        )
