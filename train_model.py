"""
Model training script for the Credit Risk Intelligence System.
Trains an XGBoost classifier and saves the model, feature columns, and SHAP explainer.

Usage:
    py train_model.py
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, accuracy_score
import shap
import pickle

print("=" * 60)
print("  Credit Risk Model Training Pipeline")
print("=" * 60)

# ─── 1. Load & Prepare Data ────────────────────────────────────────────────────
print("\n[1/5] Loading dataset...")
df = pd.read_csv('data/credit_risk_dataset.csv')
print(f"      Dataset shape: {df.shape[0]} rows × {df.shape[1]} columns")

# Handle missing values
df['person_emp_length'].fillna(df['person_emp_length'].median(), inplace=True)
df['loan_int_rate'].fillna(df['loan_int_rate'].median(), inplace=True)

# One-hot encode categorical features
df_encoded = pd.get_dummies(df, drop_first=True)

# Drop loan_int_rate as requested by user (should only be used for pricing, not prediction)
X = df_encoded.drop(columns=['loan_status', 'loan_int_rate'], errors='ignore')
y = df_encoded['loan_status']

# ─── 2. Train/Test Split ───────────────────────────────────────────────────────
print("[2/5] Splitting data (80/20)...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"      Training: {X_train.shape[0]} samples | Testing: {X_test.shape[0]} samples")

# ─── 3. Train Model ────────────────────────────────────────────────────────────
print("[3/5] Training XGBoost classifier...")
model = XGBClassifier(random_state=42, use_label_encoder=False, eval_metric='logloss')
model.fit(X_train, y_train)

# Evaluate
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions) * 100
print(f"\n      Accuracy: {accuracy:.2f}%\n")
print(classification_report(y_test, predictions))

# ─── 4. Save Model & Columns ───────────────────────────────────────────────────
print("[4/5] Saving model artifacts...")

with open('models/xgboost_credit_model.pkl', 'wb') as f:
    pickle.dump(model, f)
print("      [OK] models/xgboost_credit_model.pkl")

with open('models/model_columns.pkl', 'wb') as f:
    pickle.dump(X.columns.tolist(), f)
print("      [OK] models/model_columns.pkl")

# ─── 5. Create & Save SHAP Explainer ───────────────────────────────────────────
print("[5/5] Creating SHAP TreeExplainer...")
explainer = shap.TreeExplainer(model)

with open('models/shap_explainer.pkl', 'wb') as f:
    pickle.dump(explainer, f)
print("      [OK] models/shap_explainer.pkl")

print("\n" + "=" * 60)
print("  All artifacts saved to models/. Ready to launch app.")
print("=" * 60)