"""
SHAP API — returns SHAP explanation data as JSON for client-side visualization.
"""

from flask import Blueprint, request, jsonify
from modules.validator import parse_numeric_fields, validate_hard
from modules.predictor import predict

shap_bp = Blueprint('shap', __name__, url_prefix='/api')


@shap_bp.route('/shap', methods=['POST'])
def shap_explain():
    """
    Accept form data via JSON POST, return SHAP values for the prediction.
    Used by the client-side SHAP chart for async rendering.
    """
    raw_data = request.get_json(silent=True) or request.form.to_dict()

    parsed, parse_error = parse_numeric_fields(raw_data)
    if parse_error:
        return jsonify({'error': parse_error}), 400

    errors = validate_hard(parsed)
    if errors:
        return jsonify({'error': errors}), 400

    result = predict(parsed)

    return jsonify({
        'prediction': result['prediction'],
        'probability': result['probability'],
        'base_value': result['base_value'],
        'shap_values': result['shap_values'],
    })
