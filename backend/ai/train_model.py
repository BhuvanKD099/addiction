"""
AddictionSense Baseline & Continuous Training Script
Trains Phase 1 Multimodal Addiction Screening and Phase 2 Relapse Risk Prediction Models.
"""

import os
import csv
import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

AI_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(AI_DIR))
DATASET_DIR = os.path.join(BASE_DIR, "database")

SCREENING_CSV = os.path.join(DATASET_DIR, "realtime_multimodal_screening_dataset.csv")
RELAPSE_CSV = os.path.join(DATASET_DIR, "realtime_relapse_dataset.csv")


def load_csv_dataset(csv_path, min_features=31):
    X, y = [], []
    if not os.path.exists(csv_path):
        print(f"Dataset file not found at: {csv_path}")
        return np.array(X), np.array(y)

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for row in reader:
            if len(row) >= (min_features + 1):
                try:
                    feats = [float(x) for x in row[:min_features]]
                    label = str(row[min_features]).strip().upper()
                    X.append(feats)
                    y.append(label)
                except Exception:
                    pass

    return np.array(X), np.array(y)


def train_models():
    print("--- 1. Training Phase 1: Multimodal Addiction Risk Screening Model ---")
    X1, y1 = load_csv_dataset(SCREENING_CSV, min_features=31)
    
    if len(X1) < 5:
        print(f"Warning: Insufficient samples in {SCREENING_CSV} ({len(X1)} samples found). Training requires at least 5 samples.")
        return

    stratify_y1 = y1 if len(np.unique(y1)) > 1 else None
    X1_train, X1_test, y1_train, y1_test = train_test_split(X1, y1, test_size=0.2, random_state=42, stratify=stratify_y1)

    scaler1 = StandardScaler()
    X1_train_scaled = scaler1.fit_transform(X1_train)
    X1_test_scaled = scaler1.transform(X1_test)

    rf_screening = RandomForestClassifier(n_estimators=120, max_depth=14, random_state=42, class_weight="balanced")
    rf_screening.fit(X1_train_scaled, y1_train)

    print("Screening Model Accuracy:")
    print(classification_report(y1_test, rf_screening.predict(X1_test_scaled)))

    with open(os.path.join(AI_DIR, "addiction_rf_model.pkl"), "wb") as f:
        pickle.dump(rf_screening, f)
    with open(os.path.join(AI_DIR, "scaler.pkl"), "wb") as f:
        pickle.dump(scaler1, f)

    print("--- 2. Training Phase 2: Relapse Prediction Model ---")
    X2, y2 = load_csv_dataset(RELAPSE_CSV, min_features=8)
    
    if len(X2) < 5:
        print(f"Warning: Insufficient samples in {RELAPSE_CSV} ({len(X2)} samples found). Skipping Relapse model training.")
    else:
        stratify_y2 = y2 if len(np.unique(y2)) > 1 else None
        X2_train, X2_test, y2_train, y2_test = train_test_split(X2, y2, test_size=0.2, random_state=101, stratify=stratify_y2)

        scaler2 = StandardScaler()
        X2_train_scaled = scaler2.fit_transform(X2_train)
        X2_test_scaled = scaler2.transform(X2_test)

        rf_relapse = RandomForestClassifier(n_estimators=120, max_depth=12, random_state=101, class_weight="balanced")
        rf_relapse.fit(X2_train_scaled, y2_train)

        print("Relapse Prediction Model Accuracy:")
        print(classification_report(y2_test, rf_relapse.predict(X2_test_scaled)))

        with open(os.path.join(AI_DIR, "relapse_rf_model.pkl"), "wb") as f:
            pickle.dump(rf_relapse, f)
        with open(os.path.join(AI_DIR, "relapse_scaler.pkl"), "wb") as f:
            pickle.dump(scaler2, f)

    print(f"All multimodal models trained & saved successfully in {AI_DIR}")

if __name__ == "__main__":
    train_models()

