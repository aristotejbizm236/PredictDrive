import sys
sys.stdout.reconfigure(encoding='utf-8')

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import classification_report, accuracy_score
import xgboost as xgb
import joblib
import os

# --- CHEMIN ---

DATA_PATH = "backend/data/vehicles_train.csv"
MODELS_PATH = "backend/saved_models"

def load_and_prepare_data():
    print("Chargement du dataset...")
    df = pd.read_csv(DATA_PATH)
    print(f"Dataset charge : {len(df)} lignes, {len(df.columns)} colonnes")

    # --- ENCODAGE type_carburant (texte -> nombre) ---
    # essence -> 0 / diesel -> 1
    le = LabelEncoder()
    df["type_carburant"]= le.fit_transform(df["type_carburant"])

    # --- FEATURES (X) et CIBLE (Y) ---
    X = df.drop(columns =["etat"])
    y = df["etat"]

    # --- ENCODAGE de la cible ---
    le_target = LabelEncoder()
    y_encoded = le_target.fit_transform(y)

    print(f"\nClasses detectees : {list(le_target.classes_)}")

    # --- NORMALISATION des données ---
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X, X_scaled, y_encoded, le_target, scaler, le

def train_models():
    print("=" * 50)
    print("PREDICTDRIVE - Entrainement des modeles IA")
    print("=" * 50)

    # Charge et prépare les données
    X, X_scaled, y, le_target, scaler, le_carburant = load_and_prepare_data()

    # --- SPLIT : 80% entrainement / 20% test ---
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42
    )
    print(f"\nDonnees d'entrainement : {len(X_train)} vehicules")
    print(f"Donnees de test        : {len(X_test)} vehicules")

    # =========================================
    # MODELE 1 — XGBoost (Classification)
    # =========================================
    print("\n[1/3] Entrainement XGBoost...")
    xgb_model = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=6,
        learning_rate=0.1,
        random_state=42,
        eval_metric="mlogloss",
        verbosity=0
    )
    xgb_model.fit(X_train, y_train)
    y_pred_xgb = xgb_model.predict(X_test)
    acc_xgb = accuracy_score(y_test, y_pred_xgb)
    print(f"XGBoost - Accuracy : {acc_xgb * 100:.2f}%")
    print("\nRapport detaille XGBoost :")
    print(classification_report(y_test, y_pred_xgb,
          target_names=le_target.classes_))

    # =========================================
    # MODELE 2 — Random Forest
    # =========================================
    print("\n[2/3] Entrainement Random Forest...")
    rf_model = RandomForestClassifier(
        n_estimators=100,
        max_depth=8,
        random_state=42
    )
    rf_model.fit(X_train, y_train)
    y_pred_rf = rf_model.predict(X_test)
    acc_rf = accuracy_score(y_test, y_pred_rf)
    print(f"Random Forest - Accuracy : {acc_rf * 100:.2f}%")

    # =========================================
    # MODELE 3 — Isolation Forest (Anomalies)
    # =========================================
    print("\n[3/3] Entrainement Isolation Forest...")
    iso_model = IsolationForest(
        n_estimators=100,
        contamination=0.1,  # 10% de données considérées anormales
        random_state=42
    )
    iso_model.fit(X_scaled)  # Non supervisé : pas besoin de y
    print("Isolation Forest - Entrainement termine")

    # =========================================
    # SAUVEGARDE DES MODELES
    # =========================================
    print("\nSauvegarde des modeles...")
    os.makedirs(MODELS_PATH, exist_ok=True)

    joblib.dump(xgb_model,      f"{MODELS_PATH}/xgboost_model.pkl")
    joblib.dump(rf_model,       f"{MODELS_PATH}/randomforest_model.pkl")
    joblib.dump(iso_model,      f"{MODELS_PATH}/isoforest_model.pkl")
    joblib.dump(scaler,         f"{MODELS_PATH}/scaler.pkl")
    joblib.dump(le_target,      f"{MODELS_PATH}/label_encoder.pkl")
    joblib.dump(le_carburant,   f"{MODELS_PATH}/label_encoder_carburant.pkl")

    print("\nModeles sauvegardes dans backend/saved_models/")
    print(f"  - xgboost_model.pkl")
    print(f"  - randomforest_model.pkl")
    print(f"  - isoforest_model.pkl")
    print(f"  - scaler.pkl")
    print(f"  - label_encoder.pkl")
    print(f"  - label_encoder_carburant.pkl")

    # =========================================
    # RESUME FINAL
    # =========================================
    print("\n" + "=" * 50)
    print("RESUME DE L'ENTRAINEMENT")
    print("=" * 50)
    print(f"XGBoost     : {acc_xgb * 100:.2f}% de precision")
    print(f"RandomForest: {acc_rf * 100:.2f}% de precision")
    print("IsoForest   : Detecteur d'anomalies pret")
    print("=" * 50)
    print("Entrainement termine avec succes !")

if __name__ == "__main__":
    train_models()

