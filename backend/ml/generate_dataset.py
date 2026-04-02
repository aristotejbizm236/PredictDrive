import sys
sys.stdout.reconfigure(encoding='utf-8')  
import pandas as pd
import numpy as np
import os

# Pour avoir les mêmes données à chaque génération
np.random.seed(42)

N = 1000  # Nombre de véhicules simulés

def generate_dataset():
    print("⏳ Génération du dataset en cours...")

    # --- CARACTÉRISTIQUES DU VÉHICULE ---
    data = {
        "kilometrage": np.random.randint(5000, 300000, N),
        "age_vehicule": np.random.randint(1, 20, N),
        "regime_moteur": np.random.randint(700, 5000, N),
        "temperature_moteur": np.random.randint(60, 130, N),
        "pression_huile": np.round(np.random.uniform(0.5, 4.5, N), 1),
        "tension_batterie": np.round(np.random.uniform(11.0, 14.8, N), 1),
        "type_carburant": np.random.choice(["essence", "diesel"], N),
        "nbre_entretiens": np.random.randint(0, 20, N),
    }

    df = pd.DataFrame(data)

    # --- RÈGLES MÉTIER : simulation réaliste des pannes ---
    conditions = []

    for _, row in df.iterrows():
        score = 0

        # Kilométrage élevé = risque
        if row["kilometrage"] > 150000:
            score += 2
        if row["kilometrage"] > 250000:
            score += 2

        # Vieux véhicule = risque
        if row["age_vehicule"] > 10:
            score += 1
        if row["age_vehicule"] > 15:
            score += 2

        # Température moteur anormale
        if row["temperature_moteur"] > 105:
            score += 3

        # Pression huile faible
        if row["pression_huile"] < 1.5:
            score += 3

        # Tension batterie faible
        if row["tension_batterie"] < 12.0:
            score += 2

        # Peu d'entretiens = risque
        if row["nbre_entretiens"] < 3:
            score += 2

        # Régime moteur anormal
        if row["regime_moteur"] > 4000 or row["regime_moteur"] < 750:
            score += 1

        # --- CLASSIFICATION FINALE ---
        if score <= 2:
            conditions.append("aucune_panne")
        elif score <= 4:
            conditions.append("entretien_conseille")
        elif score <= 6:
            conditions.append("panne_probable")
        else:
            conditions.append("panne_critique")

    df["etat"] = conditions

    # --- SAUVEGARDE ---
    os.makedirs("backend/data", exist_ok=True)
    df.to_csv("backend/data/vehicles_train.csv", index=False)

    print(f"✅ Dataset généré : {N} véhicules")
    print(f"\n📊 Répartition des états :")
    print(df["etat"].value_counts())
    print(f"\n📁 Fichier sauvegardé : backend/data/vehicles_train.csv")

if __name__ == "__main__":
    generate_dataset()