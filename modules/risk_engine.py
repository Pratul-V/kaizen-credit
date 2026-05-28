"""
Policy & Risk Engine — pure business rule logic separated from ML model.
Determines policy actions and risk tiers based on prediction results and warnings.
"""

from config import RISK_TIERS, POLICY


def get_risk_tier(probability):
    """
    Classify a default probability into a risk tier.
    
    Args:
        probability: float (0-100)
    
    Returns:
        dict with 'tier', 'label', 'color', 'icon'
    """
    tiers = {
        'low': {
            'label': 'Low Risk',
            'color': '#10b981',
            'icon': '🟢',
            'css_class': 'tier-low',
        },
        'medium': {
            'label': 'Medium Risk',
            'color': '#f59e0b',
            'icon': '🟡',
            'css_class': 'tier-medium',
        },
        'high': {
            'label': 'High Risk',
            'color': '#f97316',
            'icon': '🟠',
            'css_class': 'tier-high',
        },
        'critical': {
            'label': 'Critical Risk',
            'color': '#ef4444',
            'icon': '🔴',
            'css_class': 'tier-critical',
        },
    }

    for tier_key, (low, high) in RISK_TIERS.items():
        if low <= probability < high:
            return {'tier': tier_key, **tiers[tier_key]}
    
    # Fallback for 100%
    return {'tier': 'critical', **tiers['critical']}


def evaluate_policy(prediction, probability, warnings):
    """
    Determine the policy action based on model prediction, probability,
    and business rule warnings.
    
    Args:
        prediction: int (0 or 1)
        probability: float (0-100)
        warnings: list[str]
    
    Returns:
        dict with:
            - action: str (AUTO-APPROVED, MANUAL REVIEW, REJECTED)
            - label: str (display label with icon)
            - css_class: str
            - reason: str (explanation of the decision)
            - risk_tier: dict (from get_risk_tier)
    """
    risk_tier = get_risk_tier(probability)

    # High-risk prediction → Reject
    if prediction == 1:
        if probability >= POLICY['auto_reject_prob']:
            return {
                'action': 'REJECTED',
                'label': '🚨 REJECTED',
                'css_class': 'policy-reject',
                'reason': (
                    f'AI model predicts HIGH default risk at {probability}% probability. '
                    f'Exceeds auto-reject threshold of {POLICY["auto_reject_prob"]}%.'
                ),
                'risk_tier': risk_tier,
            }
        else:
            return {
                'action': 'REJECTED',
                'label': '🚨 REJECTED',
                'css_class': 'policy-reject',
                'reason': (
                    f'AI model predicts default with {probability}% probability.'
                ),
                'risk_tier': risk_tier,
            }

    # Low-risk prediction with warnings → Manual Review
    if warnings:
        return {
            'action': 'MANUAL REVIEW',
            'label': '⚠️ MANUAL REVIEW REQUIRED',
            'css_class': 'policy-manual',
            'reason': (
                f'AI model predicts low risk ({probability}% default probability), '
                f'but {len(warnings)} business rule warning(s) flagged for human review.'
            ),
            'risk_tier': risk_tier,
        }

    # Low-risk with medium probability → Manual Review
    if probability >= POLICY['manual_review_prob']:
        return {
            'action': 'MANUAL REVIEW',
            'label': '⚠️ MANUAL REVIEW REQUIRED',
            'css_class': 'policy-manual',
            'reason': (
                f'Default probability ({probability}%) exceeds manual review threshold '
                f'of {POLICY["manual_review_prob"]}%, despite low-risk prediction.'
            ),
            'risk_tier': risk_tier,
        }

    # Clean approval
    return {
        'action': 'AUTO-APPROVED',
        'label': '✅ AUTO-APPROVED',
        'css_class': 'policy-approve',
        'reason': (
            f'AI model predicts low default risk ({probability}% probability). '
            f'No business rule warnings detected. Application auto-approved.'
        ),
        'risk_tier': risk_tier,
    }
