# AddictionSense – AI Drug Addiction Detection & Rehabilitation Recovery Management System

AddictionSense is an enterprise-grade, full-stack hybrid web platform and clinical decision support system designed for rehabilitation centers, hospitals, counselors, patients, and guardians. It integrates **Phase 1 AI Addiction Risk Screening** with **Phase 2 Rehabilitation & Relapse Monitoring**.

---

## 🌟 Key Features & Technical Capabilities

### 1. Real-Time Dataset Collection & Model Retraining (Section 13)
- **Explicit User Consent Enforcement**: Secure dataset collection ingests data only after explicit user consent (`user_consent == True`).
- **Data Validation & Deduplication**: Removes corrupted/incomplete samples and prevents duplicate entries using MD5 hash checking of feature vectors.
- **Dataset Versioning**: Maintains version metadata in `database/dataset_metadata.json` (e.g. `v1.0.0`, `v1.0.1`).
- **Safe Zero-Downtime Model Promotion**: `retrain_model.py` evaluates candidate models against production models and promotes the candidate ONLY if performance criteria are satisfied; otherwise, the previous best-performing model is preserved.
- **Evaluation Reports**: Generates Accuracy, Precision, Recall, F1-Score, Confusion Matrix, and ROC-AUC metrics.

### 2. Advanced Multimodal Detection Engine (Section 14)
- **Modality-Dropout Robust Multimodal Fusion**: Intelligently combines all available modalities:
  - **Patient Questionnaire**: Dependency, daily functioning, withdrawal, psychological markers.
  - **Parent / Guardian Questionnaire**: Observable behaviors, aggression, sleep pattern, hygiene, financial changes, secretive behavior.
  - **Face & Eye Analysis**: Facial stress, fatigue, eye openness, blink frequency, head pose jitter, facial asymmetry, micro-expressions.
  - **Hand Motor Analysis**: Tremor intensity, hand stability, motor control abnormalities, restlessness.
  - **Voice Acoustics**: Pitch variation, vocal stress, speaking rate, hesitation, vocal tremor.
- **Dynamic Sensor Fallback**: If one or more modalities are unavailable (e.g., camera off or mic quiet), normalizes active modality weights for reliable risk prediction.

### 3. Parent Questionnaire & Cross-Verification Engine (Section 15)
- **Observable Behavior Focus**: 10 targeted questions answered by parent, guardian, or spouse.
- **Cross-Verification Engine**:
  - Compares Patient self-reports against Parent observations.
  - Computes `consistency_score` (0–100%).
  - Detects explicit contradictions (e.g., Patient: "No cravings" vs Parent: "Frequent craving distress observed").
  - Dynamically reduces overall confidence score when consistency drops.
  - Generates `conflicting_answers` list for clinicians.

---

## 📁 System Architecture & Directory Structure

```
AddictionSense/
├── backend/
│   ├── ai/
│   │   ├── addictionsense_engine.py   # Phase 1 Multimodal AI Screening Engine
│   │   ├── relapse_predictor.py       # Phase 2 Relapse Risk Predictor
│   │   ├── dataset_manager.py         # Section 13 Dataset Ingestion, Validation & Versioning
│   │   ├── train_model.py             # Multimodal Baseline Dataset & Model Generator
│   │   ├── retrain_model.py           # Safe Zero-Downtime Retraining & Evaluation Reporter
│   │   ├── cross_verification.py      # Section 15 Parent-Patient Cross-Verification Engine
│   │   └── multimodal_fusion.py       # Section 14 Modality-Dropout Multimodal Fusion Engine
│   ├── routes/
│   │   ├── addictionsense.py          # /addictionsense endpoints (detect, analyze-face, etc.)
│   │   ├── ai.py                      # /ai endpoints (retrain, dataset-info, download-dataset)
│   │   ├── patients.py, doctors.py, auth.py, appointments.py, relapse.py, etc.
│   ├── utils/
│   │   └── database.py                # Hybrid MySQL / SQLite Fallback Driver
│   └── app.py                         # Main Flask Application Entry Point
├── frontend/
│   ├── addictionsense.html            # AI Multimodal Screening & Cross-Verification Page
│   ├── ai_management.html             # Real-Time Dataset Ingestion & AI Retraining Hub
│   ├── dashboard.html, patients.html, progress.html, counselling.html, relapse.html, etc.
│   └── js/
│       ├── addictionsense.js, counselling.js, patient.js, etc.
└── database/
    ├── schema.sql, seed.sql
    ├── realtime_multimodal_screening_dataset.csv
    ├── realtime_relapse_dataset.csv
    └── dataset_metadata.json
```

---

## 🚀 Quick Start Guide

### 1. Run Application
```bash
.\run_app.bat
```
- App Server: `http://127.0.0.1:5000`
- Web Portal: `frontend/login.html` or `frontend/dashboard.html`

### 2. Default Test Credentials
- **Admin**: `admin@recovery.org` / `password123`
- **Doctor**: `sarah.jenkins@hospital.org` / `password123`
- **Counselor**: `lisa.ray@counseling.org` / `password123`
- **Patient**: `john.doe@gmail.com` / `password123`

---

## 🔌 API Reference

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `POST /addictionsense/detect` | `POST` | Advanced Multimodal AI Screening (Patient Q + Parent Q + Biometrics + Consent) |
| `POST /ai/retrain/screening` | `POST` | Safe Model Retraining Pipeline (Accuracy, Precision, Recall, F1, ROC-AUC, Confusion Matrix) |
| `GET /ai/dataset-info` | `GET` | Returns dataset versioning metadata and sample counts |
| `GET /ai/download-dataset/<type>` | `GET` | Export real-time CSV datasets (`screening` or `relapse`) |
