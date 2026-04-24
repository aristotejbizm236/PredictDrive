import sys
sys.stdout.reconfigure(encoding='utf-8')
import streamlit as st
import requests
import pandas as pd
import json

st.set_page_config(page_title="Historique", page_icon="📋", layout="wide")

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
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(0,255,200,0.3) !important;
        border-radius: 50px !important;
        color: white !important;
        padding: 0.8em 1.5em !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #00ffc8 !important;
        box-shadow: 0 0 20px rgba(0,255,200,0.2) !important;
    }
    .stSelectbox > div > div {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(0,255,200,0.3) !important;
        border-radius: 12px !important;
        color: white !important;
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
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(0,255,200,0.5) !important;
    }
    .vehicle-card {
        background: rgba(255,255,255,0.03);
        border-radius: 20px;
        padding: 1.8em;
        margin: 1em 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }
    .card-critique { border: 1px solid rgba(255,68,68,0.4); border-left: 5px solid #ff4444; }
    .card-probable { border: 1px solid rgba(255,165,0,0.4); border-left: 5px solid #ffa500; }
    .card-conseille { border: 1px solid rgba(255,255,0,0.4); border-left: 5px solid #ffff00; }
    .card-sain { border: 1px solid rgba(0,255,136,0.4); border-left: 5px solid #00ff88; }
    hr { border-color: rgba(0,255,200,0.15) !important; }
</style>
""", unsafe_allow_html=True)

# Header
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown('<p class="page-title">📋 Historique</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Suivi complet des analyses véhicules</p>', unsafe_allow_html=True)
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

    for _, row in df.iterrows():
        etat_config = {
            "panne_critique":      ("card-critique", "#ff4444", "🚨"),
            "panne_probable":      ("card-probable",  "#ffa500", "⚠️"),
            "entretien_conseille": ("card-conseille", "#ffff00", "🔧"),
            "aucune_panne":        ("card-sain",      "#00ff88", "✅")
        }
        card_class, color, emoji = etat_config.get(
            row["etat"], ("card-sain", "#00ff88", "✅")
        )

        pieces = row.get("pieces_a_verifier", "[]")
        if isinstance(pieces, str):
            try:
                pieces = json.loads(pieces)
            except:
                pieces = [pieces]

        pieces_html = "".join([
            f'<span style="display:inline-block;background:rgba(255,68,68,0.1);'
            f'border:1px solid rgba(255,68,68,0.3);border-radius:50px;'
            f'padding:0.3em 0.8em;margin:0.2em;color:#ff8888;font-size:0.8em;">⚠️ {p}</span>'
            for p in pieces
        ])

        anomalie_color = "#ff4444" if row.get("anomalie_detectee") else "#00ff88"
        anomalie_text = "Détectée" if row.get("anomalie_detectee") else "Aucune"
        score_xgb = row.get('score_xgboost', 'N/A')
        score_rf = row.get('score_random_forest', 'N/A')

        with st.container():
            st.markdown(f"""
            <div class="vehicle-card {card_class}">
                <div style="display:flex;justify-content:space-between;
                align-items:center;margin-bottom:1em;">
                    <span style="color:white;font-size:1.3em;
                    font-weight:900;letter-spacing:2px;">
                        🚗 {row['matricule']}
                    </span>
                    <span style="color:#555;font-size:0.85em;">
                        {row.get('created_at','N/A')}
                    </span>
                </div>
                <div style="margin-bottom:1em;">
                    <span style="background:rgba(255,255,255,0.05);
                    border:1px solid {color}55;border-radius:50px;
                    padding:0.3em 1em;color:{color};
                    font-weight:bold;font-size:0.9em;letter-spacing:1px;">
                        {emoji} {row['etat'].replace('_',' ').upper()}
                    </span>
                </div>
                <div style="display:grid;grid-template-columns:repeat(3,1fr);
                gap:1em;margin:1em 0;">
                    <div style="background:rgba(255,255,255,0.03);
                    border-radius:10px;padding:0.8em;text-align:center;">
                        <div style="color:#00ffc8;font-size:1.2em;
                        font-weight:bold;">{score_xgb}%</div>
                        <div style="color:#8892a4;font-size:0.75em;
                        text-transform:uppercase;letter-spacing:1px;">XGBoost</div>
                    </div>
                    <div style="background:rgba(255,255,255,0.03);
                    border-radius:10px;padding:0.8em;text-align:center;">
                        <div style="color:#007cf0;font-size:1.2em;
                        font-weight:bold;">{score_rf}%</div>
                        <div style="color:#8892a4;font-size:0.75em;
                        text-transform:uppercase;letter-spacing:1px;">Random Forest</div>
                    </div>
                    <div style="background:rgba(255,255,255,0.03);
                    border-radius:10px;padding:0.8em;text-align:center;">
                        <div style="color:{anomalie_color};font-size:1.2em;
                        font-weight:bold;">{anomalie_text}</div>
                        <div style="color:#8892a4;font-size:0.75em;
                        text-transform:uppercase;letter-spacing:1px;">Anomalie</div>
                    </div>
                </div>
                <div style="margin-top:1em;">
                    <p style="color:#8892a4;font-size:0.8em;
                    text-transform:uppercase;letter-spacing:1px;
                    margin-bottom:0.5em;">🔧 Pièces à vérifier</p>
                    {pieces_html}
                </div>
                <div style="background:rgba(0,255,200,0.05);
                border:1px solid rgba(0,255,200,0.15);
                border-radius:12px;padding:1em;margin-top:1em;
                color:#cccccc;font-size:0.9em;line-height:1.6;">
                    💡 {row.get('recommandation','N/A')}
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
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