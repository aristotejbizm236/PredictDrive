import sys
sys.stdout.reconfigure(encoding='utf-8')
import streamlit as st
import requests
from PIL import Image
import os

st.set_page_config(page_title="Analyse", page_icon="🔍", layout="wide")

st.markdown("""
<style>
    .stApp { background: #0a0a0a; }
    section[data-testid="stSidebar"] {
        background: #0d0d0d;
        border-right: 1px solid rgba(0,255,200,0.2);
    }
    .page-title {
        font-size: 3.5em;
        font-weight: 900;
        background: linear-gradient(90deg, #00ffc8, #00a896, #007cf0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .page-subtitle {
        color: #8892a4;
        font-size: 1em;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    .section-title {
        color: #00ffc8;
        font-size: 0.85em;
        text-transform: uppercase;
        letter-spacing: 3px;
        margin-bottom: 1em;
        border-bottom: 1px solid rgba(0,255,200,0.2);
        padding-bottom: 0.5em;
    }
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(0,255,200,0.3) !important;
        border-radius: 12px !important;
        color: white !important;
        padding: 0.8em !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #00ffc8 !important;
        box-shadow: 0 0 15px rgba(0,255,200,0.2) !important;
    }
    .stNumberInput > div > div > input {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(0,255,200,0.3) !important;
        border-radius: 12px !important;
        color: white !important;
    }
    .stSelectbox > div > div {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(0,255,200,0.3) !important;
        border-radius: 12px !important;
        color: white !important;
    }
    .stTextInput label, .stNumberInput label, .stSelectbox label {
        color: #8892a4 !important;
        font-size: 0.85em !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }
    .stFormSubmitButton > button {
        background: linear-gradient(135deg, #00ffc8, #00a896) !important;
        color: #0a0a0a !important;
        border: none !important;
        border-radius: 15px !important;
        font-weight: 900 !important;
        font-size: 1.1em !important;
        padding: 1em 3em !important;
        width: 100% !important;
        box-shadow: 0 8px 25px rgba(0,255,200,0.4) !important;
        letter-spacing: 2px !important;
        text-transform: uppercase !important;
    }
    .stFormSubmitButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 35px rgba(0,255,200,0.6) !important;
    }
    .etat-badge {
        display: inline-block;
        padding: 0.5em 1.5em;
        border-radius: 50px;
        font-weight: 900;
        font-size: 1em;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    .etat-sain {
        background: rgba(0,255,136,0.15);
        border: 2px solid #00ff88;
        color: #00ff88;
    }
    .etat-conseille {
        background: rgba(255,255,0,0.15);
        border: 2px solid #ffff00;
        color: #ffff00;
    }
    .etat-probable {
        background: rgba(255,165,0,0.15);
        border: 2px solid #ffa500;
        color: #ffa500;
    }
    .etat-critique {
        background: rgba(255,68,68,0.15);
        border: 2px solid #ff4444;
        color: #ff4444;
        animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(255,68,68,0.4); }
        70% { box-shadow: 0 0 0 10px rgba(255,68,68,0); }
        100% { box-shadow: 0 0 0 0 rgba(255,68,68,0); }
    }
    .metric-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(0,255,200,0.15);
        border-radius: 15px;
        padding: 1.5em;
        text-align: center;
    }
    .metric-value {
        font-size: 2em;
        font-weight: 900;
        color: #00ffc8;
    }
    .metric-label {
        color: #8892a4;
        font-size: 0.8em;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 0.3em;
    }
    .autobot-card {
        background: rgba(0,255,200,0.05);
        border: 1px solid rgba(0,255,200,0.2);
        border-radius: 20px;
        padding: 2em;
        margin-top: 1.5em;
    }
    .stButton > button {
        background: linear-gradient(135deg, #00ffc8, #00a896) !important;
        color: #0a0a0a !important;
        border: none !important;
        border-radius: 50px !important;
        font-weight: 900 !important;
        width: 100% !important;
        box-shadow: 0 4px 15px rgba(0,255,200,0.3) !important;
    }
    hr { border-color: rgba(0,255,200,0.15) !important; }
</style>
""", unsafe_allow_html=True)

# Logo
logo_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'logo.png')
logo = Image.open(logo_path)

# Sidebar
st.sidebar.image(logo, width=80)
st.sidebar.markdown("""
<p style="color:#00ffc8;font-weight:900;
font-size:1.2em;letter-spacing:2px;
text-align:center;margin-top:0.5em;">
PredictDrive</p>
""", unsafe_allow_html=True)
st.sidebar.markdown("---")

# Header
col_title, col_info = st.columns([2, 1])
with col_title:
    st.markdown('<p class="page-title">🔍 Analyse</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Diagnostic IA en temps réel</p>', unsafe_allow_html=True)
with col_info:
    st.markdown("""
    <div style="background:rgba(0,255,200,0.05);border:1px solid rgba(0,255,200,0.2);
    border-radius:15px;padding:1em;margin-top:1em;">
        <p style="color:#00ffc8;margin:0;font-size:0.85em;letter-spacing:1px;">
        ⚡ MODELES ACTIFS
        </p>
        <p style="color:#cccccc;margin:0.3em 0 0 0;font-size:0.9em;">
        XGBoost • Random Forest • Isolation Forest
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Formulaire
st.markdown("""
<div style="background:rgba(255,255,255,0.03);
border:1px solid rgba(0,255,200,0.15);
border-radius:25px;padding:2.5em;
box-shadow:0 20px 60px rgba(0,0,0,0.5);">
""", unsafe_allow_html=True)

with st.form("vehicle_form"):
    st.markdown('<p class="section-title">📋 Informations du véhicule</p>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        matricule = st.text_input("Matricule", placeholder="AB-123-CD")
        modele_renault = st.selectbox("Modèle Renault", [
    "Renault Austral",
    "Renault Espace",
    "Renault R4",
    "Renault Scenic E-Tech",
    "Renault Captur",
    "Renault Clio",
    "Renault Rafale"
])
        kilometrage = st.number_input("Kilométrage (km)", min_value=0, max_value=500000, value=50000, step=1000)
        age_vehicule = st.number_input("Age du véhicule (ans)", min_value=1, max_value=50, value=5)

    with col2:
        regime_moteur = st.number_input("Régime moteur (RPM)", min_value=500, max_value=8000, value=2000)
        temperature_moteur = st.number_input("Température moteur (°C)", min_value=40, max_value=150, value=90)
        pression_huile = st.number_input("Pression huile (bar)", min_value=0.0, max_value=6.0, value=2.5, step=0.1)

    with col3:
        tension_batterie = st.number_input("Tension batterie (V)", min_value=9.0, max_value=16.0, value=12.6, step=0.1)
        type_carburant = st.selectbox("Type de carburant", ["essence", "diesel"])
        nbre_entretiens = st.number_input("Nombre d'entretiens", min_value=0, max_value=50, value=5)

    st.markdown("<br>", unsafe_allow_html=True)
    submitted = st.form_submit_button("⚡ LANCER L'ANALYSE IA", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Résultats
if submitted:
    if not matricule:
        st.error("Veuillez entrer le matricule du véhicule !")
    else:
        with st.spinner("Analyse IA en cours..."):
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/api/predict",
                    json={
                        "matricule": matricule,
                        "kilometrage": int(kilometrage),
                        "age_vehicule": int(age_vehicule),
                        "regime_moteur": int(regime_moteur),
                        "temperature_moteur": int(temperature_moteur),
                        "pression_huile": float(pression_huile),
                        "tension_batterie": float(tension_batterie),
                        "type_carburant": type_carburant,
                        "nbre_entretiens": int(nbre_entretiens)
                    }
                )

                if response.status_code == 200:
                    result = response.json()

                    st.markdown("---")
                    st.markdown("""
                    <div style="background:rgba(255,255,255,0.03);
                    border:1px solid rgba(0,255,200,0.15);
                    border-radius:25px;padding:2.5em;
                    box-shadow:0 20px 60px rgba(0,0,0,0.5);">
                    """, unsafe_allow_html=True)

                    st.markdown("""
                    <p style="color:white;font-size:1.5em;
                    font-weight:800;margin-bottom:1.5em;">
                    📊 Résultats de l'analyse
                    </p>""", unsafe_allow_html=True)

                    # Badge état
                    etat_classes = {
                        "aucune_panne": "etat-sain",
                        "entretien_conseille": "etat-conseille",
                        "panne_probable": "etat-probable",
                        "panne_critique": "etat-critique"
                    }
                    etat_emojis = {
                        "aucune_panne": "✅",
                        "entretien_conseille": "🔧",
                        "panne_probable": "⚠️",
                        "panne_critique": "🚨"
                    }
                    etat_class = etat_classes.get(result["etat"], "etat-sain")
                    etat_emoji = etat_emojis.get(result["etat"], "")

                    st.markdown(f"""
                    <div style="text-align:center;margin:1.5em 0;">
                        <p style="color:#8892a4;font-size:0.8em;
                        text-transform:uppercase;letter-spacing:2px;">
                        Modèle analysé : {modele_renault}
                        </p>
                        <span class="etat-badge {etat_class}">
                            {etat_emoji} {result['etat'].replace('_',' ').upper()}
                        </span>
                    </div>
                    """, unsafe_allow_html=True)

                    # Métriques
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-value">{result['score_xgboost']}%</div>
                            <div class="metric-label">Score XGBoost</div>
                        </div>""", unsafe_allow_html=True)
                    with col2:
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-value">{result['score_random_forest']}%</div>
                            <div class="metric-label">Score Random Forest</div>
                        </div>""", unsafe_allow_html=True)
                    with col3:
                        anomalie_color = "#ff4444" if result["anomalie_detectee"] else "#00ff88"
                        anomalie_text = "OUI" if result["anomalie_detectee"] else "NON"
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-value" style="color:{anomalie_color};">
                                {anomalie_text}
                            </div>
                            <div class="metric-label">Anomalie détectée</div>
                        </div>""", unsafe_allow_html=True)
                    with col4:
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-value">{kilometrage:,}</div>
                            <div class="metric-label">Kilomètres</div>
                        </div>""", unsafe_allow_html=True)

                    st.markdown("<br>", unsafe_allow_html=True)

                    # Recommandation + Pièces
                    col1, col2 = st.columns([3, 2])
                    with col1:
                        st.markdown("""
                        <p style="color:#00ffc8;font-size:0.85em;
                        text-transform:uppercase;letter-spacing:2px;">
                        💡 Recommandation
                        </p>""", unsafe_allow_html=True)
                        st.markdown(f"""
                        <div style="background:rgba(0,255,200,0.05);
                        border:1px solid rgba(0,255,200,0.2);
                        border-radius:15px;padding:1.5em;">
                            <p style="color:#cccccc;line-height:1.8;margin:0;">
                                {result['recommandation']}
                            </p>
                        </div>""", unsafe_allow_html=True)

                    with col2:
                        st.markdown("""
                        <p style="color:#ff4444;font-size:0.85em;
                        text-transform:uppercase;letter-spacing:2px;">
                        🔧 Pièces à vérifier
                        </p>""", unsafe_allow_html=True)
                        for piece in result["pieces_a_verifier"]:
                            st.markdown(f"""
                            <div style="background:rgba(255,68,68,0.08);
                            border:1px solid rgba(255,68,68,0.3);
                            border-radius:12px;padding:0.8em 1.2em;
                            margin:0.4em 0;color:#ff8888;font-size:0.9em;">
                            ⚠️ {piece}</div>
                            """, unsafe_allow_html=True)

                    st.markdown('</div>', unsafe_allow_html=True)

                    # AutoBot
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("🤖 Demander l'avis d'AutoBot", use_container_width=True):
                        with st.spinner("AutoBot analyse les résultats..."):
                            try:
                                chat_response = requests.post(
                                    "http://127.0.0.1:8000/api/chat",
                                    json={
                                        "message": f"Analyse ce vehicule Renault {modele_renault} : etat {result['etat']}, kilometrage {kilometrage} km, temperature {temperature_moteur}C, pression huile {pression_huile} bar, tension batterie {tension_batterie}V. Quelles sont les causes et solutions ?",
                                        "vehicle_context": result
                                    },
                                    timeout=120
                                )
                                if chat_response.status_code == 200:
                                    st.markdown(f"""
                                    <div class="autobot-card">
                                        <p style="color:#00ffc8;font-weight:bold;
                                        font-size:0.9em;letter-spacing:2px;
                                        text-transform:uppercase;">
                                        🤖 AutoBot — Powered by TinyLLaMA & RAG
                                        </p>
                                        <p style="color:#cccccc;line-height:1.8;">
                                        {chat_response.json()['response']}
                                        </p>
                                    </div>
                                    """, unsafe_allow_html=True)
                            except:
                                st.info("AutoBot indisponible pour le moment.")

                else:
                    st.error(f"Erreur API : {response.status_code}")

            except Exception as e:
                st.error(f"Erreur de connexion à l'API : {e}")