"""
Dashboard route — landing page with KPI cards and analytics overview.
"""

from flask import Blueprint, render_template
from modules.model_loader import get_global_feature_importance
from config import RISK_TIERS, POLICY, VALIDATION, WARNING_THRESHOLDS

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def index():
    """Render the main dashboard with System & Model Intelligence data."""
    feature_importance = get_global_feature_importance()
    
    return render_template(
        'dashboard.html', 
        feature_importance=feature_importance,
        risk_tiers=RISK_TIERS,
        policy=POLICY,
        validation=VALIDATION,
        warnings=WARNING_THRESHOLDS
    )
