"""
AddictionSense Parent Questionnaire & Cross-Verification Engine
Compares Patient self-reports against Parent/Guardian observations to detect
contradictions, compute response consistency scores, and adjust prediction confidence.
"""

import numpy as np

MAPPED_QUESTION_PAIRS = [
    {
        "topic": "Substance Cravings & Distress",
        "patient_q_idx": 0, # Patient Q1
        "parent_q_idx": 0,  # Parent Q1
        "patient_label": "Self-reported Cravings",
        "parent_label": "Observed Craving Episodes"
    },
    {
        "topic": "Secretive Behavior & Hiding Usage",
        "patient_q_idx": 4, # Patient Q5
        "parent_q_idx": 8,  # Parent Q9
        "patient_label": "Hiding Substance Use",
        "parent_label": "Secretive Behavior & Isolation"
    },
    {
        "topic": "Sleep Pattern & Disturbances",
        "patient_q_idx": 6, # Patient Q7
        "parent_q_idx": 2,  # Parent Q3
        "patient_label": "Self-reported Insomnia",
        "parent_label": "Observed Sleep Disruption"
    },
    {
        "topic": "Mood Swings & Emotional Instability",
        "patient_q_idx": 7, # Patient Q8
        "parent_q_idx": 6,  # Parent Q7
        "patient_label": "Self-reported Mood Swings",
        "parent_label": "Observed Emotional Instability"
    },
    {
        "topic": "Personal Hygiene & Self-Care",
        "patient_q_idx": 8, # Patient Q9
        "parent_q_idx": 7,  # Parent Q8
        "patient_label": "Self-reported Hygiene Neglect",
        "parent_label": "Observed Appearance Neglect"
    },
    {
        "topic": "Work / Daily Functioning Impact",
        "patient_q_idx": 11, # Patient Q12
        "parent_q_idx": 4,   # Parent Q5
        "patient_label": "Self-reported Work Impact",
        "parent_label": "Observed Performance Decline"
    }
]


def cross_verify_questionnaires(patient_responses, parent_responses):
    """
    Inputs:
        patient_responses: list of 15 ints (1 to 5)
        parent_responses: list of 10 ints (1 to 5)
    Returns:
        dict with patient_score, parent_score, consistency_score,
        confidence_adjustment_factor, conflicting_answers list.
    """
    if not isinstance(patient_responses, list) or len(patient_responses) < 15:
        patient_responses = [3] * 15
    if not isinstance(parent_responses, list) or len(parent_responses) < 10:
        parent_responses = [3] * 10

    patient_avg = float(np.mean(patient_responses[:15]))
    parent_avg = float(np.mean(parent_responses[:10]))

    patient_score = int(round(((patient_avg - 1.0) / 4.0) * 100))
    parent_score = int(round(((parent_avg - 1.0) / 4.0) * 100))

    conflicting_answers = []
    total_delta = 0
    max_delta = len(MAPPED_QUESTION_PAIRS) * 4.0

    for pair in MAPPED_QUESTION_PAIRS:
        p_val = patient_responses[pair["patient_q_idx"]]
        par_val = parent_responses[pair["parent_q_idx"]]
        delta = abs(p_val - par_val)
        total_delta += delta

        # Detect significant contradiction (Patient minimizes <=2 while Parent reports >=4)
        if p_val <= 2 and par_val >= 4:
            conflicting_answers.append({
                "topic": pair["topic"],
                "patient_statement": f"Reports minimal concern (Score: {p_val}/5)",
                "parent_observation": f"Observes high severity (Score: {par_val}/5)",
                "severity": "HIGH CONTRADICTION"
            })
        elif p_val >= 4 and par_val <= 2:
            conflicting_answers.append({
                "topic": pair["topic"],
                "patient_statement": f"Reports high distress (Score: {p_val}/5)",
                "parent_observation": f"Observes minimal outward signs (Score: {par_val}/5)",
                "severity": "MODERATE DISCREPANCY"
            })
        elif delta >= 3:
            conflicting_answers.append({
                "topic": pair["topic"],
                "patient_statement": f"Score: {p_val}/5",
                "parent_observation": f"Score: {par_val}/5",
                "severity": "MODERATE DISCREPANCY"
            })

    # Consistency Score (100 = perfect match, 0 = complete contradiction)
    consistency_score = int(round(max(0, min(100, 100 - (total_delta / max_delta) * 100))))

    # Confidence Penalty Factor (if consistency is low, reduce confidence)
    # Range: 0.60 (for 0% consistency) to 1.00 (for 100% consistency)
    confidence_factor = round(0.60 + 0.40 * (consistency_score / 100.0), 2)

    return {
        "patient_score": patient_score,
        "parent_score": parent_score,
        "consistency_score": consistency_score,
        "confidence_factor": confidence_factor,
        "conflicting_answers": conflicting_answers,
        "patient_avg": round(patient_avg, 2),
        "parent_avg": round(parent_avg, 2)
    }
