import joblib
import numpy as np

MODELS_PATH = "saved_models"

def load_models():
    models = {
        "xgboost":      joblib.load(f"{MODELS_PATH}/xgboost_model.pkl"),
        "randomforest": joblib.load(f"{MODELS_PATH}/randomforest_model.pkl"),
        "isoforest":    joblib.load(f"{MODELS_PATH}/isoforest_model.pkl"),
        "scaler":       joblib.load(f"{MODELS_PATH}/scaler.pkl"),
        "le_target":    joblib.load(f"{MODELS_PATH}/label_encoder.pkl"),
        "le_carburant": joblib.load(f"{MODELS_PATH}/label_encoder_carburant.pkl"),
    }
    return models

def get_pieces_a_verifier(vehicle_data: dict) -> list:
    pieces = []
    if vehicle_data["temperature_moteur"] > 105:
        pieces.append("Systeme de refroidissement")
    if vehicle_data["pression_huile"] < 1.5:
        pieces.append("Circuit huile / filtre a huile")
    if vehicle_data["tension_batterie"] < 12.0:
        pieces.append("Batterie / Alternateur")
    if vehicle_data["kilometrage"] > 150000 and vehicle_data["nbre_entretiens"] < 5:
        pieces.append("Courroie de distribution")
    if vehicle_data["regime_moteur"] > 4000:
        pieces.append("Injecteurs / Systeme injection")
    if vehicle_data["age_vehicule"] > 10:
        pieces.append("Plaquettes de frein")
    if not pieces:
        pieces.append("Aucune piece critique identifiee")
    return pieces

def get_recommandation(etat: str, pieces: list) -> str:
    recommandations = {
        "aucune_panne": "Vehicule en bon etat. Continuer les entretiens reguliers.",
        "entretien_conseille": "Un entretien est conseille dans les prochains 2000 km.",
        "panne_probable": f"Risque de panne detecte. Verifier rapidement : {', '.join(pieces)}.",
        "panne_critique": f"URGENT : Panne critique probable. Arreter le vehicule et verifier : {', '.join(pieces)}."
    }
    return recommandations.get(etat, "Etat inconnu.")

def predict(vehicle_data: dict) -> dict:
    models = load_models()

    carburant_encoded = models["le_carburant"].transform(
        [vehicle_data["type_carburant"]]
    )[0]

    features = np.array([[
        vehicle_data["kilometrage"],
        vehicle_data["age_vehicule"],
        vehicle_data["regime_moteur"],
        vehicle_data["temperature_moteur"],
        vehicle_data["pression_huile"],
        vehicle_data["tension_batterie"],
        carburant_encoded,
        vehicle_data["nbre_entretiens"]
    ]])

    features_scaled = models["scaler"].transform(features)

    xgb_pred = models["xgboost"].predict(features_scaled)[0]
    xgb_proba = models["xgboost"].predict_proba(features_scaled)[0]
    etat = models["le_target"].inverse_transform([xgb_pred])[0]
    score_xgb = float(max(xgb_proba))

    rf_pred = models["randomforest"].predict(features_scaled)[0]
    score_rf = float(max(
        models["randomforest"].predict_proba(features_scaled)[0]
    ))

    iso_pred = models["isoforest"].predict(features_scaled)[0]
    anomalie = iso_pred == -1

    pieces = get_pieces_a_verifier(vehicle_data)
    recommandation = get_recommandation(etat, pieces)

    return {
        "matricule": vehicle_data["matricule"],
        "etat": etat,
        "score_xgboost": round(score_xgb * 100, 2),
        "score_random_forest": round(score_rf * 100, 2),
        "anomalie_detectee": anomalie,
        "recommandation": recommandation,
        "pieces_a_verifier": pieces
    }