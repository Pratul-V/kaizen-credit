"""
Singleton loader for the XGBoost model, feature columns, and SHAP explainer.
Loads pickle files once at import time and exposes them as module-level variables.
"""

import pickle
import logging
from config import MODEL_PATH, COLUMNS_PATH, SHAP_EXPLAINER_PATH

logger = logging.getLogger(__name__)

_model = None
_model_columns = None
_shap_explainer = None


def _load_pickle(path, label):
    """Safely load a pickle file with error handling."""
    try:
        with open(path, 'rb') as f:
            obj = pickle.load(f)
        logger.info(f"Loaded {label} from {path}")
        return obj
    except FileNotFoundError:
        logger.error(f"{label} not found at {path}. Run train_model.py first.")
        raise RuntimeError(f"{label} not found at {path}. Run train_model.py first.")
    except Exception as e:
        logger.error(f"Failed to load {label}: {e}")
        raise RuntimeError(f"Failed to load {label}: {e}")


def get_model():
    """Return the trained XGBoost model (lazy singleton)."""
    global _model
    if _model is None:
        _model = _load_pickle(MODEL_PATH, "XGBoost model")
    return _model


def get_model_columns():
    """Return the list of model feature columns (lazy singleton)."""
    global _model_columns
    if _model_columns is None:
        _model_columns = _load_pickle(COLUMNS_PATH, "Model columns")
    return _model_columns


def get_shap_explainer():
    """Return the SHAP TreeExplainer (lazy singleton)."""
    global _shap_explainer
    if _shap_explainer is None:
        _shap_explainer = _load_pickle(SHAP_EXPLAINER_PATH, "SHAP explainer")
    return _shap_explainer


def get_global_feature_importance():
    """Extract and aggregate global feature importances from the XGBoost model."""
    try:
        model = get_model()
        cols = get_model_columns()
        
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
        else:
            return []
            
        from config import FEATURE_LABELS
        
        agg_importances = {}
        for col, imp in zip(cols, importances):
            base_col = col
            for prefix in ['person_home_ownership_', 'loan_intent_', 'cb_person_default_on_file_']:
                if col.startswith(prefix):
                    base_col = prefix.rstrip('_')
                    break
            
            agg_importances[base_col] = agg_importances.get(base_col, 0) + float(imp)
            
        result = []
        for feature_key, imp in agg_importances.items():
            label = FEATURE_LABELS.get(feature_key, feature_key)
            result.append({
                'feature': label,
                'weight': round(imp * 100, 1)
            })
            
        result.sort(key=lambda x: x['weight'], reverse=True)
        return result[:8]
    except Exception as e:
        logger.error(f"Failed to get feature importances: {e}")
        return []
