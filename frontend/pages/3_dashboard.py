import sys
sys.stdout.reconfigure(encoding='utf-8')
import streamlit as st
import requests
import pandas as pd
from PIL import Image
import os

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

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
    .stat-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(0,255,200,0.15);
        border-radius: 20px;
        padding: 1.8em;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        transition: all 0.3s;
    }
    .stat-card:hover {
        border-color: rgba(0,255,200,0.4);
        box-shadow: 0 12px 35px rgba(0,255,200,0.1);
    }
    .stat-number {
        font-size: 3em;
        font-weight: 900;
        color: #00ffc8;
        line-height: 1;
    }
    .stat-label {
        color: #8892a4;
        font-size: 0.8em;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-top: 0.5em;
    }
    .stat-icon { font-size: 1.5em; margin-bottom: 0.3em; }
    .chart-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(0,255,200,0.15);
        border-radius: 20px;
        padding: 1.5em;
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }
    .chart-title {
        color: #00ffc8;
        font-size: 0.85em;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 1em;
        border-bottom: 1px solid rgba(0,255,200,0.15);
        padding-bottom: 0.5em;
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
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown('<p class="page-title">📊 Dashboard</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Analytics & Statistiques en temps réel</p>', unsafe_allow_html=True)
with col2:
    if st.button("🔄 Actualiser", use_container_width=True):
        st.rerun()

st.markdown("---")

try:
    response = requests.get("http://127.0.0.1:8000/api/history")
    data = response.json()

    if not isinstance(data, list) or len(data) == 0:
        st.markdown("""
        <div style="text-align:center;padding:4em;
        background:rgba(255,255,255,0.02);
        border:1px solid rgba(0,255,200,0.1);
        border-radius:25px;">
            <div style="font-size:4em;">🚗</div>
            <p style="color:#8892a4;font-size:1.2em;margin-top:1em;">
                Aucune analyse effectuee pour le moment.
            </p>
            <p style="color:#555;">
                Analysez un vehicule pour voir les statistiques !
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    df = pd.DataFrame.from_records(data)

    # Stats
    total = len(df)
    critiques = len(df[df["etat"] == "panne_critique"])
    probables = len(df[df["etat"] == "panne_probable"])
    entretiens = len(df[df["etat"] == "entretien_conseille"])
    sains = len(df[df["etat"] == "aucune_panne"])
    anomalies = int(df["anomalie_detectee"].sum()) if "anomalie_detectee" in df.columns else 0

    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-icon">📋</div>
            <div class="stat-number">{total}</div>
            <div class="stat-label">Total</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-icon">🚨</div>
            <div class="stat-number" style="color:#ff4444;">{critiques}</div>
            <div class="stat-label">Critiques</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-icon">⚠️</div>
            <div class="stat-number" style="color:#ffa500;">{probables}</div>
            <div class="stat-label">Probables</div>
        </div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-icon">🔧</div>
            <div class="stat-number" style="color:#ffff00;">{entretiens}</div>
            <div class="stat-label">Entretiens</div>
        </div>""", unsafe_allow_html=True)
    with col5:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-icon">✅</div>
            <div class="stat-number" style="color:#00ff88;">{sains}</div>
            <div class="stat-label">Sains</div>
        </div>""", unsafe_allow_html=True)
    with col6:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-icon">🔴</div>
            <div class="stat-number" style="color:#ff6b6b;">{anomalies}</div>
            <div class="stat-label">Anomalies</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Graphiques
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<p class="chart-title">📈 Répartition des états</p>', unsafe_allow_html=True)
        etat_counts = df["etat"].value_counts().reset_index()
        etat_counts.columns = ["etat", "count"]
        st.bar_chart(etat_counts.set_index("etat"), color="#00ffc8")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<p class="chart-title">📊 Score XGBoost moyen par état</p>', unsafe_allow_html=True)
        if "score_xgboost" in df.columns:
            avg_scores = df.groupby("etat")["score_xgboost"].mean().reset_index()
            avg_scores.columns = ["etat", "score"]
            st.bar_chart(avg_scores.set_index("etat"), color="#007cf0")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Tableau
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<p class="chart-title">🕐 Dernières analyses</p>', unsafe_allow_html=True)
    colonnes = [c for c in ["matricule", "etat", "score_xgboost",
                "score_random_forest", "anomalie_detectee",
                "created_at"] if c in df.columns]
    st.dataframe(df[colonnes].head(10), use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Exporter en CSV",
        data=csv,
        file_name="predictdrive_analytics.csv",
        mime="text/csv",
        use_container_width=True
    )

except requests.exceptions.ConnectionError:
    st.error("Impossible de se connecter à l'API !")
except Exception as e:
    st.error(f"Erreur : {e}")