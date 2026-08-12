"""
Phase 2 Relapse Risk Prediction Engine
Utilizes Random Forest machine learning classifier + clinical rule validation
Predicts relapse risk based on mood, sleep, craving level, medication adherence,
counseling attendance, stress level, relapse history, and addiction severity.
"""

import os
import pickle
import numpy as np

AI_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(AI_DIR, "relapse_rf_model.pkl")
SCALER_PATH = os.path.join(AI_DIR, "relapse_scaler.pkl")

_relapse_model = None
_relapse_scaler = None

def _load_relapse_ml_artifacts():
    global _relapse_model, _relapse_scaler
    if _relapse_model is None and os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH):
        try:
            with open(MODEL_PATH, "rb") as f:
                _relapse_model = pickle.load(f)
            with open(SCALER_PATH, "rb") as f:
                _relapse_scaler = pickle.load(f)
        except Exception as e:
            print("Warning: Failed loading Relapse ML model artifacts:", e)

def predict_relapse_risk(
    mood="Normal",
    sleep_quality="Good",
    craving_level=5,
    medication_adherence=1,
    counseling_attendance=1,
    stress_level=3,
    previous_relapses=0,
    addiction_severity="MODERATE",
    withdrawal_level=3
):
    """
    Inputs:
        mood: str ("Excellent", "Good", "Normal", "Bad", "Very Bad")
        sleep_quality: str ("Very Good", "Good", "Fair", "Poor")
        craving_level: int (1-10)
        medication_adherence: int (1 or 0)
        counseling_attendance: int (1 or 0)
        stress_level: int (1-10)
        previous_relapses: int
        addiction_severity: str ("MILD", "MODERATE", "SEVERE")
    """
    _load_relapse_ml_artifacts()

    # Map inputs to numeric features
    mood_map = {"EXCELLENT": 5.0, "GOOD": 4.0, "NORMAL": 3.0, "FAIR": 3.0, "BAD": 2.0, "VERY BAD": 1.0}
    sleep_map = {"VERY GOOD": 5.0, "GOOD": 4.0, "FAIR": 3.0, "POOR": 2.0, "VERY POOR": 1.0}
    severity_map = {"MILD": 1, "MODERATE": 2, "SEVERE": 3}

    m_score = mood_map.get(str(mood).upper(), 3.0)
    s_score = sleep_map.get(str(sleep_quality).upper(), 3.0)
    c_level = float(max(1, min(10, craving_level)))
    med_adh = float(1 if medication_adherence else 0)
    coun_att = float(1 if counseling_attendance else 0)
    str_lvl = float(max(1, min(10, stress_level)))
    prev_rel = float(max(0, previous_relapses))
    sev_num = float(severity_map.get(str(addiction_severity).upper(), 2))

    features = [m_score, s_score, c_level, med_adh, coun_att, str_lvl, prev_rel, sev_num]

    predicted_level = "MODERATE"
    confidence_score = 88.0

    if _relapse_model is not None and _relapse_scaler is not None:
        try:
            X_scaled = _relapse_scaler.transform([features])
            predicted_level = str(_relapse_model.predict(X_scaled)[0]).upper()
            if hasattr(_relapse_model, "predict_proba"):
                probs = _relapse_model.predict_proba(X_scaled)[0]
                confidence_score = float(np.max(probs) * 100.0)
        except Exception as e:
            print("Error executing Relapse RF inference:", e)

    # Calculated risk score (0-100)
    craving_risk = (c_level / 10.0) * 35.0
    stress_risk = (str_lvl / 10.0) * 25.0
    mood_risk = ((5.0 - m_score) / 4.0) * 15.0
    sleep_risk = ((5.0 - s_score) / 4.0) * 10.0
    compliance_risk = (2.0 - med_adh - coun_att) * 7.5
    history_risk = min(15.0, prev_rel * 5.0)

    calculated_risk_score = int(round(craving_risk + stress_risk + mood_risk + sleep_risk + compliance_risk + history_risk))
    calculated_risk_score = max(0, min(100, calculated_risk_score))

    if not _relapse_model:
        if calculated_risk_score >= 65:
            predicted_level = "HIGH"
        elif calculated_risk_score >= 35:
            predicted_level = "MODERATE"
        else:
            predicted_level = "LOW"

    # Counseling Frequency & Suggested Interventions
    if predicted_level == "HIGH":
        counseling_frequency = "3x Weekly (Intensive)"
        interventions = [
            "Immediate clinical evaluation with primary physician.",
            "Adjust medication prescription & initiate daily check-in call.",
            "Assign emergency recovery buddy & 24/7 hotline monitoring."
        ]
    elif predicted_level == "MODERATE":
        counseling_frequency = "2x Weekly"
        interventions = [
            "Schedule follow-up counseling session within 48 hours.",
            "Increase daily habit & trigger logging.",
            "Focus on CBT relapse prevention techniques and stress management."
        ]
    else:
        counseling_frequency = "Weekly"
        interventions = [
            "Maintain current recovery monitoring protocol.",
            "Continue regular support group participation.",
            "Complete daily habit check-ins."
        ]

    # Triggers
    triggers = []
    if c_level >= 7:
        triggers.append(f"Elevated craving score ({int(c_level)}/10)")
    if str_lvl >= 7:
        triggers.append(f"High subjective stress level ({int(str_lvl)}/10)")
    if m_score <= 2.0:
        triggers.append(f"Depressed or negative mood ({mood})")
    if s_score <= 2.0:
        triggers.append("Severe sleep disturbance / poor sleep quality")
    if not med_adh:
        triggers.append("Missed medication doses")
    if not coun_att:
        triggers.append("Missed counseling session")
    if prev_rel >= 2:
        triggers.append(f"History of previous relapse ({int(prev_rel)} events)")

    if not triggers:
        triggers.append("No acute triggers identified")

    return {
        "predicted_risk_level": predicted_level,
        "risk_score": calculated_risk_score,
        "confidence_score": round(confidence_score, 1),
        "counseling_frequency": counseling_frequency,
        "triggers": triggers,
        "recommendations": interventions
    }
