"""
Centralized configuration for the Credit Risk Intelligence System.
All magic numbers, paths, thresholds, and feature metadata live here.
"""

import os

# ─── Paths ──────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'xgboost_credit_model.pkl')
COLUMNS_PATH = os.path.join(BASE_DIR, 'models', 'model_columns.pkl')
SHAP_EXPLAINER_PATH = os.path.join(BASE_DIR, 'models', 'shap_explainer.pkl')
DATASET_PATH = os.path.join(BASE_DIR, 'data', 'credit_risk_dataset.csv')

# ─── Hard Validation Rules ──────────────────────────────────────────────────────
VALIDATION = {
    'age_min': 18,
    'age_max': 100,
    'income_min': 1,          # Must be > 0
    'loan_amount_min': 1,     # Must be > 0
    'emp_length_min': 0,
    'int_rate_min': 0.0,
    'int_rate_max': 40.0,
    'cred_hist_min': 0,
}

# ─── Soft Warning Thresholds ────────────────────────────────────────────────────
WARNING_THRESHOLDS = {
    'loan_to_income_ratio': 2.0,       # Warn if loan > 200% of income
    'low_income_threshold': 15000,     # Dollar threshold for "low income"
    'low_income_high_loan': 10000,     # Loan amount that's disproportionate for low income
    'young_age_threshold': 25,         # Age below which long credit history is suspicious
    'young_credit_hist_max': 5,        # Max credit history years for young applicants
    'high_interest_rate': 20.0,        # Interest rate above which is flagged
}

# ─── Risk Tiers (by probability of default) ─────────────────────────────────────
RISK_TIERS = {
    'low':      (0, 20),
    'medium':   (20, 45),
    'high':     (45, 70),
    'critical': (70, 100),
}

# ─── Policy Thresholds ──────────────────────────────────────────────────────────
POLICY = {
    'auto_reject_prob': 70,       # Auto-reject above this probability
    'manual_review_prob': 35,     # Send to manual review above this
}

# ─── Feature Metadata ───────────────────────────────────────────────────────────
CATEGORICAL_FEATURES = {
    'person_home_ownership': ['RENT', 'OWN', 'MORTGAGE', 'OTHER'],
    'loan_intent': ['PERSONAL', 'EDUCATION', 'MEDICAL', 'VENTURE',
                    'HOMEIMPROVEMENT', 'DEBTCONSOLIDATION'],
    'cb_person_default_on_file': ['Y', 'N'],
}

NUMERIC_FEATURES = [
    'person_age', 'person_income', 'person_emp_length',
    'loan_amnt', 'loan_int_rate', 'cb_person_cred_hist_length',
    'cibil_score',
]

# Derived feature computed at prediction time
DERIVED_FEATURES = ['loan_percent_income']

# Human-readable labels for SHAP display
FEATURE_LABELS = {
    'person_age': 'Age',
    'person_income': 'Annual Income',
    'person_emp_length': 'Employment Length',
    'loan_amnt': 'Loan Amount',
    'loan_int_rate': 'Interest Rate',
    'loan_percent_income': 'Loan-to-Income Ratio',
    'cb_person_cred_hist_length': 'Credit History Length',
    'person_home_ownership': 'Home Ownership',
    'loan_intent': 'Loan Intent',
    'cb_person_default_on_file': 'Historical Default',
    'cibil_score': 'CIBIL Score',
}

# ─── Flask Settings ─────────────────────────────────────────────────────────────
DEBUG = True
PORT = 5000
SECRET_KEY = 'credit-risk-enterprise-2024'
