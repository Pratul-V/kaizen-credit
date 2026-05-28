"""
What-If Loan Simulator Route
"""

from flask import Blueprint, render_template, request, jsonify
from modules.predictor import predict
from modules.validator import validate_soft
from modules.pricing.pricing_engine import evaluate_application

simulate_bp = Blueprint('simulate', __name__)

@simulate_bp.route('/simulate')
def simulate_page():
    return render_template('simulate.html')

@simulate_bp.route('/api/simulate', methods=['POST'])
def api_simulate():
    data = request.json
    
    parsed = {
        'person_name': 'Simulator',
        'customer_id': 'SIM-001',
        'person_age': float(data.get('person_age', 30)),
        'person_income': float(data.get('person_income', 60000)),
        'person_emp_length': float(data.get('person_emp_length', 5)),
        'loan_amnt': float(data.get('loan_amnt', 15000)),
        'loan_int_rate': float(data.get('loan_int_rate', 10.0)),
        'cb_person_cred_hist_length': float(data.get('cb_person_cred_hist_length', 5)),
        'cibil_score': float(data.get('cibil_score', 750)),
        'person_home_ownership': data.get('person_home_ownership', 'RENT'),
        'loan_intent': data.get('loan_intent', 'PERSONAL'),
        'cb_person_default_on_file': data.get('cb_person_default_on_file', 'N'),
    }
    
    warnings = validate_soft(parsed)
    prediction_result = predict(parsed)
    policy = evaluate_application(parsed, prediction_result['probability'], warnings)
    
    # Strip complex objects like counter_offer if it fails serialization
    # but our policy dict is usually JSON serializable.
    return jsonify({
        'prediction': prediction_result['prediction'],
        'probability': prediction_result['probability'],
        'confidence': prediction_result.get('confidence', 50),
        'pricing': policy
    })
