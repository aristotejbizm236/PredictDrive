import sys
sys.stdout.reconfigure(encoding='utf-8')
import streamlit as st
from PIL import Image
import os

st.set_page_config(
    page_title="PredictDrive",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
        border-radius: 15px !important;
        font-weight: 900 !important;
        width: 100% !important;
        padding: 0.8em !important;
        box-shadow: 0 4px 15px rgba(0,255,200,0.3) !important;
        letter-spacing: 1px !important;
        font-size: 1em !important;
    }
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 25px rgba(0,255,200,0.5) !important;
    }
    .stat-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(0,255,200,0.15);
        border-radius: 20px;
        padding: 1.8em;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }
    .stat-number {
        font-size: 2.5em;
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
    .feature-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(0,255,200,0.15);
        border-radius: 20px;
        padding: 2em;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }
    .feature-icon { font-size: 3em; margin-bottom: 0.3em; }
    .feature-title {
        color: #00ffc8;
        font-size: 1.2em;
        font-weight: bold;
        margin: 0.5em 0;
    }
    .feature-desc { color: #8892a4; font-size: 0.9em; line-height: 1.6; }
    hr { border-color: rgba(0,255,200,0.15) !important; }
</style>
""", unsafe_allow_html=True)

# Logo
logo_path = os.path.join(os.path.dirname(__file__), 'assets', 'logo.png')
logo = Image.open(logo_path)

# Sidebar
st.sidebar.markdown("""
<div style="display:flex;flex-direction:column;
align-items:center;justify-content:center;
text-align:center;width:100%;padding-top:1em;">
    <img src="data:image/png;base64,{}" 
    style="width:80px;margin:0 auto;display:block;">
    <p style="color:#00ffc8;font-weight:900;
    font-size:1.2em;letter-spacing:2px;
    text-align:center;margin-top:0.5em;">
    PredictDrive</p>
</div>
""".format(__import__('base64').b64encode(
    open(logo_path, 'rb').read()).decode()),
unsafe_allow_html=True)
st.sidebar.markdown("---")

# Header — Logo centré au dessus du nom
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div style="display:flex;flex-direction:column;
    align-items:center;justify-content:center;
    text-align:center;width:100%;">
        <img src="data:image/png;base64,{}" 
        style="width:100px;margin:0 auto;display:block;">
    </div>
    """.format(__import__('base64').b64encode(
        open(logo_path, 'rb').read()).decode()),
    unsafe_allow_html=True)
    
    st.markdown("""
    <p style="font-size:2.5em;font-weight:900;
    background:linear-gradient(90deg,#00ffc8,#00a896,#007cf0);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
    text-align:center;margin:0;letter-spacing:3px;line-height:1;">
    PredictDrive</p>
    <p style="color:#8892a4;text-align:center;
    letter-spacing:3px;text-transform:uppercase;
    font-size:0.9em;margin-top:0.3em;">
    Intelligence Artificielle • Maintenance Prédictive • Automobile
    </p>
    """, unsafe_allow_html=True)

st.markdown("---")
# Stats
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">84%</div>
        <div class="stat-label">Précision IA</div>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">3</div>
        <div class="stat-label">Modèles IA</div>
    </div>""", unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">8</div>
        <div class="stat-label">Paramètres</div>
    </div>""", unsafe_allow_html=True)
with col4:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">4</div>
        <div class="stat-label">Niveaux risque</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Features avec boutons
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🔍</div>
        <div class="feature-title">Analyse Intelligente</div>
        <div class="feature-desc">Saisissez les paramètres de votre véhicule et obtenez une prédiction instantanée.</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔍 Lancer une Analyse", key="btn_analyse", use_container_width=True):
        st.switch_page("pages/1_analyse.py")

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🤖</div>
        <div class="feature-title">Assistant AutoBot</div>
        <div class="feature-desc">Chatbot RAG propulsé par Phi-3 pour guider votre diagnostic Renault.</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🤖 Parler à AutoBot", key="btn_chat", use_container_width=True):
        st.switch_page("pages/2_chatbot.py")

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📊</div>
        <div class="feature-title">Dashboard Analytics</div>
        <div class="feature-desc">Visualisez les statistiques et tendances de votre flotte.</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📊 Voir le Dashboard", key="btn_dashboard", use_container_width=True):
        st.switch_page("pages/3_dashboard.py")

with col4:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📋</div>
        <div class="feature-title">Historique</div>
        <div class="feature-desc">Consultez l'historique complet de toutes les analyses effectuées.</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📋 Voir l'Historique", key="btn_historique", use_container_width=True):
        st.switch_page("pages/4_historique.py")

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
<p style='text-align:center;color:#555;font-size:0.85em;'>
PredictDrive v1.0 • XGBoost • Random Forest • Isolation Forest • TinyLLaMA • RAG
</p>""", unsafe_allow_html=True)