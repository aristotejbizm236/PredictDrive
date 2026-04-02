# Ce fichier gère la connexion à SQLite
# SQLite = une base de données stockée dans un simple fichier .db
# Pas besoin d'installer un serveur comme PostgreSQL

import sqlite3
import os

DB_PATH = "backend/data/predictdrive.db"

def get_connection():
    """
    Ouvre une connexion à la base de données.
    Crée le fichier .db s'il n'existe pas encore.
    """
    os.makedirs("backend/data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Retourne des dicts au lieu de tuples
    return conn

def init_database():
    """
    Crée les tables si elles n'existent pas.
    Appelée une seule fois au démarrage de l'API.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Table des véhicules analysés
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id                  INTEGER PRIMARY KEY AUTOINCREMENT,
            matricule           TEXT NOT NULL,
            kilometrage         INTEGER,
            age_vehicule        INTEGER,
            regime_moteur       INTEGER,
            temperature_moteur  INTEGER,
            pression_huile      REAL,
            tension_batterie    REAL,
            type_carburant      TEXT,
            nbre_entretiens     INTEGER,
            etat                TEXT,
            score_xgboost       REAL,
            anomalie_detectee   INTEGER,
            recommandation      TEXT,
            pieces_a_verifier   TEXT,
            created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()
    print("Base de donnees initialisee avec succes !")