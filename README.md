# 🚗 PredictDrive — Système Intelligent de Maintenance Prédictive Automobile

![PredictDrive](https://img.shields.io/badge/PredictDrive-v1.0-00ffc8?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green?style=for-the-badge&logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-1.55-red?style=for-the-badge&logo=streamlit)
![XGBoost](https://img.shields.io/badge/XGBoost-3.2-orange?style=for-the-badge)
![RAG](https://img.shields.io/badge/RAG-TinyLLaMA-purple?style=for-the-badge)

---

## 📋 Table des matières

- [Description du projet](#description-du-projet)
- [Problématique](#problématique)
- [Architecture du système](#architecture-du-système)
- [Technologies utilisées](#technologies-utilisées)
- [Fonctionnalités](#fonctionnalités)
- [Structure du projet](#structure-du-projet)
- [Installation et démarrage](#installation-et-démarrage)
- [Utilisation](#utilisation)
- [Les modèles IA](#les-modèles-ia)
- [Le système RAG](#le-système-rag)
- [API REST](#api-rest)
- [Résultats et performances](#résultats-et-performances)
- [Perspectives d'évolution](#perspectives-dévolution)

---

## 📌 Description du projet

**PredictDrive** est une application d'intelligence artificielle dédiée à la **maintenance prédictive automobile**, développée dans le cadre d'un projet étudiant en informatique. Elle permet à un utilisateur — mécanicien, technicien ou particulier — de saisir les paramètres techniques d'un véhicule Renault et d'obtenir en temps réel une **analyse complète de son état de santé mécanique**.

Le projet couvre l'intégralité du cycle de vie d'un système Data Science : de la génération des données à la mise en production, en passant par l'entraînement des modèles, la conception d'une API REST et le développement d'une interface utilisateur moderne.

PredictDrive se distingue par la combinaison de deux approches complémentaires :
- Des **modèles de Machine Learning supervisés et non supervisés** pour la détection et la classification des pannes
- Un **système RAG (Retrieval-Augmented Generation)** propulsé par un LLM local (TinyLLaMA via Ollama) pour générer des explications et recommandations en langage naturel, enrichi par des documents techniques officiels Renault

---

## 🎯 Problématique

Les pannes automobiles surviennent souvent de manière imprévisible, entraînant des coûts de réparation élevés et des immobilisations non planifiées des véhicules. La maintenance curative — attendre la panne pour intervenir — est coûteuse et inefficace.

**PredictDrive répond à cette problématique en proposant :**
- Une détection précoce des risques de panne avant qu'ils ne surviennent
- Une identification précise des pièces susceptibles d'être défaillantes
- Des recommandations concrètes en langage naturel, basées sur des documents techniques officiels
- Un historique complet permettant le suivi de l'évolution de l'état d'un véhicule dans le temps

---

## 🏗️ Architecture du système

```
┌─────────────────────────────────────────────────────────────────┐
│                     UTILISATEUR                                  │
│           (Mécanicien / Technicien / Particulier)               │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│              COUCHE PRÉSENTATION (Streamlit)                     │
│   Page Accueil │ Analyse │ AutoBot │ Dashboard │ Historique      │
└─────────────────────────┬───────────────────────────────────────┘
                          │ HTTP/JSON
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                COUCHE API REST (FastAPI)                         │
│   POST /api/predict │ POST /api/chat │ GET /api/history          │
└──────────┬──────────────────────────┬──────────────────────────┘
           │                          │
           ▼                          ▼
┌──────────────────┐      ┌───────────────────────────────────────┐
│   MOTEUR IA ML   │      │         MOTEUR RAG                    │
│                  │      │                                       │
│ XGBoost          │      │  ChromaDB (Base Vectorielle)          │
│ Random Forest    │      │  nomic-embed-text (Embeddings)        │
│ Isolation Forest │      │  TinyLLaMA via Ollama (LLM)           │
└──────────┬───────┘      │  Documents techniques Renault (PDFs)  │
           │              └───────────────────────────────────────┘
           ▼
┌─────────────────────────────────────────────────────────────────┐
│                  COUCHE DONNÉES                                  │
│   SQLite (Historique) │ CSV (Dataset) │ PKL (Modèles sauvegardés)│
└─────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Technologies utilisées

### Intelligence Artificielle & Machine Learning
| Technologie | Version | Rôle |
|-------------|---------|------|
| XGBoost | 3.2.0 | Classification supervisée des pannes |
| Scikit-learn | 1.4.2 | Random Forest + Isolation Forest |
| Pandas | 2.3.3 | Traitement et preprocessing des données |
| NumPy | 1.26.4 | Calculs mathématiques |
| Joblib | 1.4.0 | Sérialisation des modèles |

### RAG & LLM
| Technologie | Version | Rôle |
|-------------|---------|------|
| Ollama | Latest | Exécution du LLM en local |
| TinyLLaMA | Latest | Modèle de langage local |
| LangChain | Latest | Orchestration du pipeline RAG |
| ChromaDB | Latest | Base de données vectorielle |
| nomic-embed-text | Latest | Génération des embeddings |
| pdfplumber | Latest | Extraction de texte des PDFs |

### Backend & API
| Technologie | Version | Rôle |
|-------------|---------|------|
| FastAPI | 0.111.0 | API REST |
| Uvicorn | 0.29.0 | Serveur ASGI |
| SQLite | Built-in | Base de données |
| SQLAlchemy | 2.0.30 | ORM |
| Pydantic | 2.7.1 | Validation des données |

### Frontend
| Technologie | Version | Rôle |
|-------------|---------|------|
| Streamlit | 1.55.0 | Interface web interactive |
| Pillow | Latest | Gestion des images |

---

## ✨ Fonctionnalités

### 🔍 Analyse intelligente des véhicules
- Saisie des paramètres techniques du véhicule (kilométrage, âge, température moteur, pression huile, tension batterie, régime moteur, type de carburant, nombre d'entretiens)
- Sélection du modèle Renault parmi les 7 modèles supportés
- Prédiction instantanée de l'état du véhicule en 4 niveaux de criticité
- Score de confiance pour chaque modèle IA
- Détection automatique des anomalies
- Identification des pièces à risque
- Recommandations personnalisées

### 🤖 Assistant AutoBot (RAG)
- Chatbot conversationnel propulsé par TinyLLaMA via Ollama
- Base de connaissances enrichie par des documents techniques officiels Renault (7 modèles)
- Réponses contextuelles basées sur les documents indexés dans ChromaDB
- Questions rapides prédéfinies pour les cas les plus courants
- Fonctionnement 100% local, sans connexion internet requise

### 📊 Dashboard Analytics
- Statistiques globales en temps réel (total analyses, pannes critiques, véhicules sains...)
- Graphiques de répartition des états
- Score XGBoost moyen par état
- Tableau des dernières analyses
- Export CSV des données

### 📋 Historique des analyses
- Consultation de toutes les analyses effectuées
- Recherche par matricule
- Filtrage par état
- Cartes détaillées avec scores, pièces à vérifier et recommandations
- Export CSV

### 📥 Ingestion automatique de PDFs
- Système d'ingestion automatique des documents techniques Renault
- Conversion PDF → TXT → Embeddings ChromaDB
- Mise à jour automatique de la base de connaissances RAG

---

## 📁 Structure du projet

```
PredictDrive/
│
├── backend/
│   ├── main.py                          # Point d'entrée FastAPI
│   ├── requirements.txt                 # Dépendances Python
│   │
│   ├── app/
│   │   ├── models/
│   │   │   └── vehicle.py               # Schémas Pydantic
│   │   ├── routes/
│   │   │   ├── predict.py               # Endpoints prédiction
│   │   │   └── chat.py                  # Endpoints chatbot
│   │   ├── services/
│   │   │   ├── prediction_service.py    # Logique ML
│   │   │   └── chatbot_service.py       # Logique RAG
│   │   └── database/
│   │       ├── connection.py            # Connexion SQLite
│   │       └── queries.py               # Requêtes SQL
│   │
│   ├── ml/
│   │   ├── generate_dataset.py          # Génération du dataset
│   │   ├── train.py                     # Entraînement des modèles
│   │   ├── ingest_pdfs.py               # Ingestion des PDFs
│   │   └── knowledge_base/
│   │       ├── pdfs/                    # PDFs techniques Renault
│   │       ├── pannes_auto.txt          # Base de connaissances pannes
│   │       └── entretiens.txt           # Base de connaissances entretiens
│   │
│   ├── saved_models/                    # Modèles ML sauvegardés (.pkl)
│   └── data/                            # Dataset CSV + BDD SQLite
│
├── frontend/
│   ├── app.py                           # Page d'accueil
│   ├── assets/
│   │   └── logo.png                     # Logo PredictDrive
│   └── pages/
│       ├── 1_analyse.py                 # Page analyse véhicule
│       ├── 2_chatbot.py                 # Page AutoBot
│       ├── 3_dashboard.py               # Page dashboard
│       └── 4_historique.py             # Page historique
│
├── venv/                                # Environnement virtuel Python
├── .env                                 # Variables d'environnement
└── README.md                            # Documentation
```

---

## 🚀 Installation et démarrage

### Prérequis
- Python 3.9+
- Git
- Ollama (pour le chatbot RAG)

### 1. Cloner le projet
```bash
git clone https://github.com/votre-username/PredictDrive.git
cd PredictDrive
```

### 2. Créer et activer l'environnement virtuel
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python -m venv venv
source venv/bin/activate
```

### 3. Installer les dépendances
```bash
pip install -r backend/requirements.txt
```

### 4. Installer et configurer Ollama
```bash
# Télécharger Ollama sur https://ollama.com/download
# Puis télécharger les modèles nécessaires :
ollama pull tinyllama
ollama pull nomic-embed-text
```

### 5. Générer le dataset et entraîner les modèles
```bash
python backend/ml/generate_dataset.py
python backend/ml/train.py
```

### 6. Ingérer les documents techniques (optionnel)
```bash
# Placer les PDFs dans backend/ml/knowledge_base/pdfs/
python backend/ml/ingest_pdfs.py
```

### 7. Démarrer l'application

**Terminal 1 — API FastAPI :**
```bash
cd backend
uvicorn main:app --reload
```

**Terminal 2 — Interface Streamlit :**
```bash
python -m streamlit run frontend/app.py
```

### 8. Accéder à l'application
```
Interface web  : http://localhost:8501
API docs       : http://127.0.0.1:8000/docs
```

---

## 📖 Utilisation

### Analyser un véhicule
1. Accéder à la page **Analyse** via le menu latéral
2. Sélectionner le **modèle Renault** dans la liste
3. Saisir le **matricule** du véhicule
4. Renseigner les **paramètres techniques** (kilométrage, température, pression huile...)
5. Cliquer sur **"LANCER L'ANALYSE IA"**
6. Consulter les résultats : état, scores, pièces à vérifier, recommandations

### Utiliser AutoBot
1. Accéder à la page **AutoBot** via le menu latéral
2. Taper votre question dans le champ de saisie
3. Utiliser les **questions rapides** pour les cas courants
4. Recevoir une réponse basée sur les documents techniques Renault

### Ajouter des documents techniques
1. Placer les PDFs dans `backend/ml/knowledge_base/pdfs/`
2. Lancer `python backend/ml/ingest_pdfs.py`
3. La base de connaissances est automatiquement mise à jour

---

## 🧠 Les modèles IA

### Modèle 1 — XGBoost (Classification supervisée)
XGBoost est le modèle principal de PredictDrive. Il classifie l'état du véhicule parmi 4 catégories en se basant sur les paramètres saisis.

| Catégorie | Description |
|-----------|-------------|
| `aucune_panne` | Véhicule en bon état |
| `entretien_conseille` | Entretien recommandé sous 2000 km |
| `panne_probable` | Risque de panne détecté |
| `panne_critique` | Panne imminente, intervention urgente |

**Performances :** 84% de précision sur le jeu de test

### Modèle 2 — Random Forest (Confirmation)
Random Forest sert de modèle de confirmation. Il vote indépendamment de XGBoost et fournit un second score de confiance permettant de valider ou nuancer la prédiction principale.

**Performances :** 81.5% de précision

### Modèle 3 — Isolation Forest (Détection d'anomalies)
Isolation Forest est le seul modèle **non supervisé** du projet. Il apprend le comportement normal d'un véhicule et détecte automatiquement toute déviation significative, même pour des types de pannes non encore référencés.

**Output :** Normal (1) ou Anomalie (-1) avec score de confiance

### Features utilisées
| Feature | Description | Seuil critique |
|---------|-------------|----------------|
| `kilometrage` | Kilométrage total | > 150 000 km |
| `age_vehicule` | Âge en années | > 10 ans |
| `regime_moteur` | Régime en RPM | > 4000 RPM |
| `temperature_moteur` | Température en °C | > 105°C |
| `pression_huile` | Pression en bar | < 1.5 bar |
| `tension_batterie` | Tension en Volts | < 12V |
| `type_carburant` | Essence ou Diesel | — |
| `nbre_entretiens` | Nombre de révisions | < 3 |

---

## 🔍 Le système RAG

### Fonctionnement
Le système RAG (Retrieval-Augmented Generation) de PredictDrive combine la puissance de la recherche sémantique et d'un LLM local pour générer des réponses contextuelles et précises.

```
Question utilisateur
        ↓
Génération de l'embedding (nomic-embed-text)
        ↓
Recherche sémantique dans ChromaDB
        ↓
Extraction des passages les plus pertinents
        ↓
Construction du prompt enrichi
        ↓
Génération de la réponse (TinyLLaMA)
        ↓
Réponse en français à l'utilisateur
```

### Documents supportés
| Modèle | Fichier PDF |
|--------|-------------|
| Renault Austral | ct_ebrochure_renault_austral_fr_mars_2026.pdf |
| Renault Espace | ct_ebro_renault_espace_fr_mars_2026.pdf |
| Renault R4 | ct_renault_r4_fr_fevrier_2025.pdf |
| Renault Scenic E-Tech | ct_renault_scenic_etech_hcb_fr_mai_2025.pdf |
| Renault Captur | renault_captur_hjb_fr_avril_2026.pdf |
| Renault Clio | renault_clio_bja_fr_juillet_2025.pdf |
| Renault Rafale | renault_rafale_fr_mars_2026.pdf |

---

## 🔌 API REST

### Endpoints disponibles

#### POST /api/predict
Prédit l'état d'un véhicule à partir de ses paramètres techniques.

**Request body :**
```json
{
  "matricule": "AB-123-CD",
  "kilometrage": 95000,
  "age_vehicule": 7,
  "regime_moteur": 3200,
  "temperature_moteur": 102,
  "pression_huile": 1.8,
  "tension_batterie": 12.6,
  "type_carburant": "diesel",
  "nbre_entretiens": 5
}
```

**Response :**
```json
{
  "matricule": "AB-123-CD",
  "etat": "panne_probable",
  "score_xgboost": 78.5,
  "score_random_forest": 72.3,
  "anomalie_detectee": true,
  "recommandation": "Risque de panne detecte. Verifier rapidement : Systeme de refroidissement.",
  "pieces_a_verifier": ["Systeme de refroidissement", "Circuit huile"]
}
```

#### POST /api/chat
Envoie un message au chatbot AutoBot.

**Request body :**
```json
{
  "message": "Mon moteur chauffe beaucoup, que faire ?",
  "vehicle_context": null
}
```

#### GET /api/history
Retourne l'historique complet de toutes les analyses.

#### GET /api/history/{matricule}
Retourne l'historique des analyses pour un véhicule spécifique.

---

## 📈 Résultats et performances

### Modèles ML
| Modèle | Accuracy | Précision | Recall | F1-Score |
|--------|----------|-----------|--------|----------|
| XGBoost | **84%** | 83% | 84% | 83% |
| Random Forest | **81.5%** | 80% | 81% | 80% |
| Isolation Forest | N/A | Détection anomalies | N/A | N/A |

### Dataset
- **1000 véhicules simulés** avec des règles métier réalistes
- **4 classes** de sortie équilibrées
- **8 features** d'entrée
- Split **80/20** entraînement/test

---

## 🔮 Perspectives d'évolution

### Court terme
- Amélioration de la qualité des réponses RAG avec un modèle LLM plus puissant (Mistral 7B)
- Ajout de nouveaux modèles Renault dans la base de connaissances
- Intégration de codes défauts OBD-II réels

### Moyen terme
- Connexion à un boîtier OBD-II pour la collecte de données en temps réel
- Déploiement cloud (Streamlit Cloud, Railway ou Render)
- Application mobile pour les mécaniciens sur le terrain
- Système d'alertes automatiques par email/SMS

### Long terme
- Extension à d'autres marques automobiles
- Intégration de données IoT et capteurs temps réel
- Modèles LSTM pour l'analyse de séries temporelles
- Tableau de bord flotte pour les professionnels de l'automobile

---

## 👤 Auteur

**Jack** — Étudiant en informatique  
Projet réalisé dans le cadre d'un projet académique en Data Science et Intelligence Artificielle.

---

## 📄 Licence

Ce projet est réalisé dans un cadre académique. Tous droits réservés.

---

*PredictDrive v1.0 — XGBoost • Random Forest • Isolation Forest • TinyLLaMA • RAG • FastAPI • Streamlit*
