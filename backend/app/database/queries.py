# Ce fichier contient toutes les interactions
# avec la base de données SQLite

import json
from app.database.connection import get_connection

def save_prediction(vehicle_data: dict, prediction: dict):
    """
    Sauvegarde une prédiction dans la base de données.
    Appelée après chaque analyse de véhicule.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO predictions (
            matricule, kilometrage, age_vehicule,
            regime_moteur, temperature_moteur,
            pression_huile, tension_batterie,
            type_carburant, nbre_entretiens,
            etat, score_xgboost, anomalie_detectee,
            recommandation, pieces_a_verifier
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        vehicle_data["matricule"],
        vehicle_data["kilometrage"],
        vehicle_data["age_vehicule"],
        vehicle_data["regime_moteur"],
        vehicle_data["temperature_moteur"],
        vehicle_data["pression_huile"],
        vehicle_data["tension_batterie"],
        vehicle_data["type_carburant"],
        vehicle_data["nbre_entretiens"],
        prediction["etat"],
        prediction["score_xgboost"],
        int(prediction["anomalie_detectee"]),
        prediction["recommandation"],
        json.dumps(prediction["pieces_a_verifier"])
    ))

    conn.commit()
    conn.close()

def get_all_predictions():
    """
    Récupère tout l'historique des prédictions.
    Utilisé par Streamlit pour afficher l'historique.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM predictions
        ORDER BY created_at DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_prediction_by_matricule(matricule: str):
    """
    Récupère l'historique d'un véhicule spécifique.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM predictions
        WHERE matricule = ?
        ORDER BY created_at DESC
    """, (matricule,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]