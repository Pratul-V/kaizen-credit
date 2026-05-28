"""
risk_engine.py
Evaluates risk tiers and policies.
"""
from modules.pricing.underwriting_rules import RISK_TIERS

def get_risk_tier(probability):
    for tier, (low, high) in RISK_TIERS.items():
        if low <= probability < high:
            return tier
    return 'critical'

def get_risk_metadata(risk_tier):
    meta = {
        'low': {
            'label': 'Low Risk',
            'color': '#10b981',
            'icon': '🟢',
            'css_class': 'tier-low',
            'explanation': "Applicant demonstrates strong repayment capability and stable financial behaviour. Full loan amount approved at preferred interest rates."
        },
        'medium': {
            'label': 'Moderate Risk',
            'color': '#f59e0b',
            'icon': '🟡',
            'css_class': 'tier-medium',
            'explanation': "Some financial risk indicators were identified. Loan terms have been moderately adjusted to align with lending policies."
        },
        'high': {
            'label': 'High Risk',
            'color': '#f97316',
            'icon': '🟠',
            'css_class': 'tier-high',
            'explanation': "Applicant exhibits elevated default probability. A reduced loan offer with revised pricing has been generated to minimize financial exposure."
        },
        'critical': {
            'label': 'Critical Risk',
            'color': '#ef4444',
            'icon': '🔴',
            'css_class': 'tier-critical',
            'explanation': "Risk profile exceeds acceptable lending thresholds. Alternative secured lending options may be required."
        }
    }
    return meta.get(risk_tier, meta['critical'])
