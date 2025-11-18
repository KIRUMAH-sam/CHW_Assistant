# backend/utils/ml_model.py
import os
import joblib
import numpy as np

MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'ml', 'model.pkl')

try:
    model = joblib.load(MODEL_PATH)
    MODEL_LOADED = True
except Exception as e:
    model = None
    MODEL_LOADED = False
    # In production log this exception. For now, fallback to rules-only if model missing.

def featurize(features: dict):
    """
    Ensure feature vector ordering matches the trained model.
    Example expected order: age_months, fever, cough, difficulty_breathing, temp_c
    """
    return np.array([[ 
        features.get('age_months', 0),
        features.get('fever', 0),
        features.get('cough', 0),
        features.get('difficulty_breathing', 0),
        features.get('temp_c', 0.0)
    ]])

def predict_risk(features: dict):
    if not MODEL_LOADED:
        # fallback: simple heuristic risk
        score = 0.0
        score += 0.3 if features.get('difficulty_breathing') else 0.0
        score += 0.25 if features.get('fever') and features.get('temp_c',0) >= 39 else 0.0
        score += 0.15 if features.get('cough') and features.get('age_months',0) < 12 else 0.0
        return round(min(score, 0.99), 3)
    X = featurize(features)
    proba = model.predict_proba(X)[0][1]
    return round(float(proba), 3)
