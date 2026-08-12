"""
AddictionSense Phase 1 AI Multimodal Screening Engine
Combines:
- Patient Questionnaire (15 questions)
- Parent / Guardian Questionnaire (10 questions)
- Multimodal Affect & Biometrics (Face, Eye, Hand Tremor, Voice Acoustics)
- Cross-Verification Engine (Patient vs Parent Contradictions & Consistency Score)
- Modality-Dropout Robust Multimodal Fusion Engine
"""

import os
import pickle
import numpy as np
from ai.cross_verification import cross_verify_questionnaires
from ai.multimodal_fusion import compute_multimodal_fusion

AI_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(AI_DIR, "addiction_rf_model.pkl")
SCALER_PATH = os.path.join(AI_DIR, "scaler.pkl")

_model = None
_scaler = None

def _load_ml_artifacts():
    global _model, _scaler
    if _model is None and os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH):
        try:
            with open(MODEL_PATH, "rb") as f: _model = pickle.load(f)
            with open(SCALER_PATH, "rb") as f: _scaler = pickle.load(f)
        except Exception as e:
            print("Warning: Failed loading Phase 1 ML artifacts:", e)

def predict_addiction_risk(
    q_responses=None,
    parent_q_responses=None,
    smile_score=0.75,
    eye_openness=0.82,
    blink_rate=16.0,
    facial_stress=0.25,
    voice_stress=0.25,
    hand_tremor=0.15,
    user_consent=False
):
    _load_ml_artifacts()

    # Sanitize Patient Questionnaire
    if not isinstance(q_responses, list) or len(q_responses) < 15:
        base_p = [int(x) for x in q_responses] if isinstance(q_responses, list) else []
        while len(base_p) < 15: base_p.append(3)
        q_responses = base_p[:15]
    else:
        q_responses = [int(max(1, min(5, v))) for v in q_responses[:15]]

    # Sanitize Parent Questionnaire
    if not isinstance(parent_q_responses, list) or len(parent_q_responses) < 10:
        base_par = [int(x) for x in parent_q_responses] if isinstance(parent_q_responses, list) else []
        while len(base_par) < 10: base_par.append(3)
        parent_q_responses = base_par[:10]
    else:
        parent_q_responses = [int(max(1, min(5, v))) for v in parent_q_responses[:10]]

    # 1. Run Parent-Patient Cross-Verification Engine (Section 15)
    cross_res = cross_verify_questionnaires(q_responses, parent_q_responses)

    # 2. Compute Individual Modality Sub-Scores (0 to 100)
    patient_q_score = cross_res["patient_score"]
    parent_q_score = cross_res["parent_score"]

    face_score = int(round(facial_stress * 100.0))
    eye_score = int(round((1.0 - eye_openness) * 60.0 + (min(50.0, blink_rate) / 50.0) * 40.0))
    hand_score = int(round(hand_tremor * 100.0))
    voice_score = int(round(voice_stress * 100.0))

    # 3. Run Modality-Dropout Robust Multimodal Fusion Engine (Section 14)
    fusion_res = compute_multimodal_fusion(
        patient_q_score=patient_q_score,
        parent_q_score=parent_q_score,
        face_score=face_score,
        eye_score=eye_score,
        hand_score=hand_score,
        voice_score=voice_score,
        cross_verification_res=cross_res
    )

    # 4. Optional Random Forest ML Inference Check
    predicted_level = fusion_res["risk_level"]
    risk_score = fusion_res["risk_percentage"]
    confidence_score = fusion_res["confidence"]

    if _model is not None and _scaler is not None:
        try:
            features = q_responses + parent_q_responses + [
                smile_score, eye_openness, blink_rate, facial_stress, voice_stress, hand_tremor
            ]
            X_scaled = _scaler.transform([features])
            rf_pred = str(_model.predict(X_scaled)[0]).upper()
            if hasattr(_model, "predict_proba"):
                probs = _model.predict_proba(X_scaled)[0]
                rf_conf = int(round(float(np.max(probs) * 100.0) * cross_res["confidence_factor"]))
                confidence_score = max(40, min(99, rf_conf))
            if rf_pred in ["HIGH", "MODERATE", "LOW"]:
                predicted_level = rf_pred.capitalize()
        except Exception as e:
            print("RF inference fallback note:", e)

    # 5. Format AI Clinical Explanation
    explanation = (
        f"Multimodal AI fusion indicates a {predicted_level} Risk of addiction ({risk_score}% severity, {confidence_score}% confidence). "
        f"Patient Questionnaire Score: {patient_q_score}%, Parent Observation Score: {parent_q_score}% (Response Consistency: {cross_res['consistency_score']}%). "
        f"Biometric affect indicators: Facial stress {face_score}%, Vocal tremor {voice_score}%, Hand motor instability {hand_score}%."
    )

    # Triggers & Recommendations
    triggers = list(fusion_res["contributing_factors"])
    recommendations = []
    if predicted_level in ["High", "Moderate", "HIGH", "MODERATE"]:
        recommendations.append("Register as a patient in Rehabilitation System for active clinical tracking.")
        recommendations.append("Schedule an initial consultation with an Addiction Psychiatrist.")
        recommendations.append("Initiate daily habit tracking and medication management plan.")
        recommendations.append("Connect with emergency helpline (1800-11-0031) or 24/7 counseling support.")
    else:
        recommendations.append("Maintain active healthy lifestyle and daily wellness practices.")
        recommendations.append("Participate in community awareness and peer support groups.")
        recommendations.append("Re-assess monthly or if craving symptoms emerge.")

    # Combined Structured Response Matching Sections 14 & 15 Specs
    return {
        "risk_percentage": risk_score,
        "risk_level": predicted_level,
        "confidence": confidence_score,
        "patient_score": patient_q_score,
        "parent_score": parent_q_score,
        "consistency_score": cross_res["consistency_score"],
        "conflicting_answers": cross_res["conflicting_answers"],
        "contributing_factors": triggers,
        "scores": fusion_res["scores"],
        "ai_explanation": explanation,
        "triggers": triggers,
        "recommendations": recommendations,
        "predicted_risk_level": predicted_level.upper(),
        "risk_score": risk_score,
        "confidence_score": confidence_score,
        "questionnaire_avg": cross_res["patient_avg"],
        "parent_questionnaire_avg": cross_res["parent_avg"],
        "facial_stress_score": face_score,
        "voice_stress_score": voice_score,
        "hand_tremor_score": hand_score,
        "blink_rate": round(blink_rate, 1),
        "smile_score": round(smile_score, 2),
        "eye_openness": round(eye_openness, 2)
    }
