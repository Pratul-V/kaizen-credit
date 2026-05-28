"""
Prediction engine — handles feature encoding, model inference, and SHAP explanations.
"""

import pandas as pd
import numpy as np
from modules.model_loader import get_model, get_model_columns, get_shap_explainer
from config import FEATURE_LABELS


def predict(form_data):
    """
    Run the XGBoost model on parsed form data and compute SHAP explanations.
    
    Args:
        form_data: dict with parsed numeric + categorical values
    
    Returns:
        dict with keys:
            - prediction: int (0 = low risk, 1 = high risk)
            - probability: float (0-100, probability of default)
            - shap_values: list of (feature_label, shap_value, feature_value) tuples
            - base_value: float (SHAP base value / expected value)
    """
    model = get_model()
    model_columns = get_model_columns()

    # Build the input DataFrame
    income = form_data['person_income']
    loan_amnt = form_data['loan_amnt']

    input_dict = {
        'person_age': [form_data['person_age']],
        'person_income': [income],
        'person_home_ownership': [form_data['person_home_ownership']],
        'person_emp_length': [form_data['person_emp_length']],
        'loan_intent': [form_data['loan_intent']],
        'cibil_score': [form_data['cibil_score']],
        'loan_amnt': [loan_amnt],
        'cb_person_default_on_file': [form_data['cb_person_default_on_file']],
        'cb_person_cred_hist_length': [form_data['cb_person_cred_hist_length']],
        'loan_percent_income': [loan_amnt / income if income > 0 else 0],
    }

    input_df = pd.DataFrame(input_dict)
    input_encoded = pd.get_dummies(input_df)
    input_encoded = input_encoded.reindex(columns=model_columns, fill_value=0)

    # Model prediction
    prediction = int(model.predict(input_encoded)[0])
    probability = round(float(model.predict_proba(input_encoded)[0][1]) * 100, 2)
    confidence = round(max(probability, 100 - probability), 1)

    # SHAP explanation
    shap_data = _compute_shap(input_encoded, form_data)

    return {
        'prediction': prediction,
        'probability': probability,
        'confidence': confidence,
        'shap_values': shap_data['shap_values'],
        'base_value': shap_data['base_value'],
    }


def _compute_shap(input_encoded, form_data):
    """
    Compute SHAP values for a single prediction.
    
    Returns:
        dict with:
            - shap_values: list of (label, shap_value, display_value) sorted by abs impact
            - base_value: float
    """
    try:
        explainer = get_shap_explainer()
        shap_vals = explainer.shap_values(input_encoded)
        
        # shap_vals may be a list (for multi-output) or ndarray
        if isinstance(shap_vals, list):
            shap_vals = shap_vals[1]  # Class 1 (default) SHAP values
        
        shap_array = shap_vals[0] if shap_vals.ndim > 1 else shap_vals
        feature_names = input_encoded.columns.tolist()
        
        # Get base value
        base_value = float(explainer.expected_value)
        if isinstance(explainer.expected_value, (list, np.ndarray)):
            base_value = float(explainer.expected_value[1])

        # Aggregate one-hot encoded SHAP values back to original features
        aggregated = _aggregate_shap_values(shap_array, feature_names, form_data)

        # Sort by absolute SHAP value (most impactful first)
        aggregated.sort(key=lambda x: abs(x['value']), reverse=True)

        return {
            'shap_values': aggregated[:10],  # Top 10 features
            'base_value': round(base_value, 4),
        }
    except Exception as e:
        import logging
        logging.getLogger(__name__).warning(f"SHAP computation failed: {e}")
        return {'shap_values': [], 'base_value': 0.0}


def _aggregate_shap_values(shap_array, feature_names, form_data):
    """
    Aggregate SHAP values for one-hot encoded features back to their
    original categorical feature names.
    
    For example, loan_grade_B, loan_grade_C, etc. → "Loan Grade"
    """
    # Map one-hot column names to original feature names
    original_feature_map = {}
    for col_name, shap_val in zip(feature_names, shap_array):
        # Find the base feature name (before the one-hot suffix)
        base_name = _get_base_feature(col_name)
        if base_name not in original_feature_map:
            original_feature_map[base_name] = 0.0
        original_feature_map[base_name] += float(shap_val)

    # Build result with human-readable labels and display values
    result = []
    for feature_key, shap_val in original_feature_map.items():
        label = FEATURE_LABELS.get(feature_key, feature_key)
        display_value = _get_display_value(feature_key, form_data)
        rule = _map_shap_to_rule(feature_key, shap_val, display_value, label)
        result.append({
            'feature': label,
            'value': round(shap_val, 4),
            'display': display_value,
            'rule': rule
        })

    return result


def _get_base_feature(encoded_col_name):
    """Map a one-hot encoded column name back to the original feature name."""
    # Known categorical prefixes from config
    cat_prefixes = [
        'person_home_ownership_', 'loan_intent_',
        'cb_person_default_on_file_',
    ]
    for prefix in cat_prefixes:
        if encoded_col_name.startswith(prefix):
            return prefix.rstrip('_')
    return encoded_col_name


def _get_display_value(feature_key, form_data):
    """Get a human-readable display value for a feature."""
    value = form_data.get(feature_key)
    if value is None:
        # Check for computed features
        if feature_key == 'loan_percent_income':
            income = form_data.get('person_income', 1)
            loan = form_data.get('loan_amnt', 0)
            return f"{(loan / income * 100) if income > 0 else 0:.1f}%"
        return "—"
    
    if isinstance(value, float):
        if value == int(value):
            return str(int(value))
        return f"{value:.1f}"
    return str(value)


def _map_shap_to_rule(feature_key, shap_val, display_value, label):
    """Map raw SHAP values into simple human-readable rules."""
    direction = "Increased risk" if shap_val > 0 else "Decreased risk"
    
    # Generic rule for small impact
    if abs(shap_val) < 0.1:
        return f"{label} ({display_value}) has minimal impact"
        
    if feature_key == 'loan_percent_income':
        if shap_val > 0:
            return f"High DTI ({display_value}) → {direction}"
        else:
            return f"Low DTI ({display_value}) → {direction}"
    elif feature_key == 'person_income':
        if shap_val > 0:
            return f"Lower income ({display_value}) → {direction}"
        else:
            return f"Higher income ({display_value}) → {direction}"
    elif feature_key == 'cibil_score':
        if shap_val > 0:
            return f"Low CIBIL score ({display_value}) → {direction}"
        else:
            return f"Good CIBIL score ({display_value}) → {direction}"
    else:
        return f"{label} ({display_value}) → {direction}"

