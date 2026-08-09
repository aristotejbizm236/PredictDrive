import sys
sys.stdout.reconfigure(encoding='utf-8')
import streamlit as st
import requests
import pandas as pd
import json
from PIL import Image
import os

st.set_page_config(page_title="Historique", page_icon="📋", layout="wide")

st.markdown("""
<style>
    .stApp { background: #0a0a0a; }
    section[data-testid="stSidebar"] {
        background: #0d0d0d;
        border-right: 1px solid rgba(0,255,200,0.2);
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
    .stSelectbox > div > div {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(0,255,200,0.3) !important;
        border-radius: 12px !important;
        color: white !important;
    }
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(0,255,200,0.3) !important;
        border-radius: 50px !important;
        color: white !important;
        padding: 0.8em 1.5em !important;
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
<p style="color:#00ffc8;font-weight:900;font-size:1.2em;
letter-spacing:2px;text-align:center;margin-top:0.5em;">
PredictDrive</p>
""", unsafe_allow_html=True)
st.sidebar.markdown("---")

# Header
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("""
    <p style="font-size:3.5em;font-weight:900;
    background:linear-gradient(90deg,#00ffc8,#00a896,#007cf0);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
    margin-bottom:0;">📋 Historique</p>
    <p style="color:#8892a4;font-size:1em;letter-spacing:2px;
    text-transform:uppercase;">Suivi complet des analyses véhicules</p>
    """, unsafe_allow_html=True)
with col2:
    if st.button("🔄 Actualiser", use_container_width=True):
        st.rerun()

st.markdown("---")

# Recherche
col1, col2, col3 = st.columns([3, 1, 1])
with col1:
    matricule_search = st.text_input(
        "search",
        placeholder="🔍 Rechercher par matricule...",
        label_visibility="collapsed"
    )
with col2:
    search_btn = st.button("Rechercher", use_container_width=True)
with col3:
    show_all = st.button("Tout afficher", use_container_width=True)

st.markdown("---")

try:
    if search_btn and matricule_search:
        response = requests.get(f"http://127.0.0.1:8000/api/history/{matricule_search}")
    else:
        response = requests.get("http://127.0.0.1:8000/api/history")

    data = response.json()

    if not isinstance(data, list) or len(data) == 0:
        st.info("Aucune analyse trouvee. Analysez un vehicule pour voir l'historique !")
        st.stop()

    df = pd.DataFrame.from_records(data)

    col1, col2 = st.columns([2, 4])
    with col1:
        etats = ["Tous"] + list(df["etat"].unique())
        filtre = st.selectbox("Filtrer par état", etats)

    if filtre != "Tous":
        df = df[df["etat"] == filtre]

    st.markdown(f"**{len(df)} analyse(s) trouvee(s)**")
    st.markdown("<br>", unsafe_allow_html=True)

    # Affichage avec composants natifs
    for _, row in df.iterrows():
        etat_config = {
            "panne_critique":      ("🚨", "red"),
            "panne_probable":      ("⚠️", "orange"),
            "entretien_conseille": ("🔧", "yellow"),
            "aucune_panne":        ("✅", "green")
        }
        emoji, couleur = etat_config.get(row["etat"], ("✅", "green"))

        with st.container():
            st.markdown(f"""
            <div style="border-left:5px solid {'#ff4444' if couleur=='red' else '#ffa500' if couleur=='orange' else '#ffff00' if couleur=='yellow' else '#00ff88'};
            background:rgba(255,255,255,0.03);border-radius:0 20px 20px 0;
            padding:0.5em 1em;margin-bottom:0.5em;">
            <span style="color:white;font-size:1.1em;font-weight:900;">
            🚗 {row['matricule']}</span>
            <span style="color:#555;font-size:0.8em;float:right;">
            {row.get('created_at','N/A')}</span>
            </div>
            """, unsafe_allow_html=True)

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("État", f"{emoji} {row['etat'].replace('_',' ').upper()}")
            with col2:
                st.metric("XGBoost", f"{row.get('score_xgboost','N/A')}%")
            with col3:
                st.metric("Random Forest", f"{row.get('score_random_forest','N/A')}%")
            with col4:
                anomalie = "🔴 Oui" if row.get('anomalie_detectee') else "🟢 Non"
                st.metric("Anomalie", anomalie)

            # Pièces
            pieces = row.get("pieces_a_verifier", "[]")
            if isinstance(pieces, str):
                try:
                    pieces = json.loads(pieces)
                except:
                    pieces = [pieces]

            if pieces:
                st.markdown("**🔧 Pièces à vérifier :**")
                cols = st.columns(len(pieces) if len(pieces) <= 4 else 4)
                for i, piece in enumerate(pieces):
                    with cols[i % 4]:
                        st.error(f"⚠️ {piece}")

            # Recommandation
            st.info(f"💡 {row.get('recommandation', 'N/A')}")
            st.markdown("---")

    # Export
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Exporter en CSV",
        data=csv,
        file_name="historique_predictdrive.csv",
        mime="text/csv",
        use_container_width=True
    )

except requests.exceptions.ConnectionError:
    st.error("Impossible de se connecter à l'API !")
except Exception as e:
    st.error(f"Erreur : {e}")