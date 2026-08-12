"""
AddictionSense Advanced Multimodal Fusion Engine
Intelligently combines all available modalities:
- Patient Questionnaire (Dependency, Withdrawal, Daily Functioning)
- Parent Questionnaire (Observable Behavior, Aggression, Hygiene, Secretive)
- Face Analysis (Stress, Fatigue, Eye Openness, Blink Rate, Head Pose, Asymmetry, Micro-expressions)
- Eye Analysis (Fixation, Gaze Jitter, Pupil Variance)
- Hand Analysis (Tremor, Stability, Finger Consistency, Motor Abnormality, Restlessness)
- Voice Analysis (Pitch Variation, Voice Stress, Speaking Rate, Hesitation, Vocal Tremor)

Supports Modality-Dropout (missing sensor fallback) by dynamically re-weighting active modalities.
"""

import numpy as np


def compute_multimodal_fusion(
    patient_q_score=None,
    parent_q_score=None,
    face_score=None,
    eye_score=None,
    hand_score=None,
    voice_score=None,
    cross_verification_res=None
):
    """
    Inputs:
        Individual modality scores (0 to 100), or None if modality is missing.
    Returns:
        dict matching Section 14 requirement schema:
        {
            "risk_percentage": int,
            "risk_level": str ("Low", "Moderate", "High"),
            "confidence": int,
            "contributing_factors": list of str,
            "scores": {
                "questionnaire": int,
                "parent_questionnaire": int,
                "face": int,
                "eye": int,
                "hand": int,
                "voice": int
            }
        }
    """
    # Base default weights for full 6-modality pipeline
    base_weights = {
        "questionnaire": 0.25,
        "parent_questionnaire": 0.20,
        "face": 0.15,
        "eye": 0.10,
        "hand": 0.15,
        "voice": 0.15
    }

    # Collect available active modalities
    raw_scores = {
        "questionnaire": patient_q_score,
        "parent_questionnaire": parent_q_score,
        "face": face_score,
        "eye": eye_score,
        "hand": hand_score,
        "voice": voice_score
    }

    active_modalities = {k: v for k, v in raw_scores.items() if v is not None}

    # If no modalities provided, fallback to defaults
    if not active_modalities:
        active_modalities = {
            "questionnaire": 50,
            "face": 30
        }

    # Re-normalize active weights to sum to 1.0 (Modality-Dropout Robustness)
    total_active_weight = sum(base_weights[k] for k in active_modalities.keys())
    normalized_weights = {k: base_weights[k] / total_active_weight for k in active_modalities.keys()}

    # Compute fused weighted risk percentage
    fused_risk_pct = sum(active_modalities[k] * normalized_weights[k] for k in active_modalities.keys())
    risk_pct = int(round(max(0.0, min(100.0, fused_risk_pct))))

    # Determine Risk Level
    if risk_pct >= 65:
        risk_level = "High"
    elif risk_pct >= 35:
        risk_level = "Moderate"
    else:
        risk_level = "Low"

    # Base Confidence Calculation (higher with more active modalities)
    active_ratio = len(active_modalities) / len(base_weights)
    base_confidence = 75 + int(round(active_ratio * 20)) # 75% to 95%

    # Apply Cross-Verification Confidence Penalty if available
    confidence_penalty_factor = 1.0
    if cross_verification_res and "confidence_factor" in cross_verification_res:
        confidence_penalty_factor = cross_verification_res["confidence_factor"]

    final_confidence = int(round(max(40, min(99, base_confidence * confidence_penalty_factor))))

    # Identify Contributing Factors
    contributing_factors = []
    if raw_scores.get("questionnaire", 0) >= 60:
        contributing_factors.append("High behavioral dependency & craving score")
    if raw_scores.get("parent_questionnaire", 0) >= 60:
        contributing_factors.append("Parent observed severe behavioral changes & withdrawal")
    if raw_scores.get("face", 0) >= 55:
        contributing_factors.append("High facial fatigue & affective stress score")
    if raw_scores.get("eye", 0) >= 55:
        contributing_factors.append("Eye fatigue & micro-blink irregularity observed")
    if raw_scores.get("hand", 0) >= 45:
        contributing_factors.append("Hand tremor & motor restlessness detected")
    if raw_scores.get("voice", 0) >= 50:
        contributing_factors.append("Vocal acoustic stress & pitch instability detected")

    if cross_verification_res and cross_verification_res.get("conflicting_answers"):
        contributing_factors.append(f"Significant Parent-Patient response discrepancy ({len(cross_verification_res['conflicting_answers'])} contradictions flagged)")

    if not contributing_factors:
        contributing_factors.append("Biometric and behavioral markers within normal reference ranges")

    # Format final output dictionary matching Section 14 spec
    return {
        "risk_percentage": risk_pct,
        "risk_level": risk_level,
        "confidence": final_confidence,
        "contributing_factors": contributing_factors,
        "scores": {
            "questionnaire": int(round(raw_scores.get("questionnaire", 0) or 0)),
            "parent_questionnaire": int(round(raw_scores.get("parent_questionnaire", 0) or 0)),
            "face": int(round(raw_scores.get("face", 0) or 0)),
            "eye": int(round(raw_scores.get("eye", 0) or 0)),
            "hand": int(round(raw_scores.get("hand", 0) or 0)),
            "voice": int(round(raw_scores.get("voice", 0) or 0))
        }
    }
