import sys
sys.stdout.reconfigure(encoding='utf-8')
import streamlit as st
import requests
from PIL import Image
import os

st.set_page_config(page_title="AutoBot", page_icon="🤖", layout="wide")

st.markdown("""
<style>
    .stApp { background: #0a0a0a; }
    section[data-testid="stSidebar"] {
        background: #0d0d0d;
        border-right: 1px solid rgba(0,255,200,0.2);
    }
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(0,255,200,0.3) !important;
        border-radius: 50px !important;
        color: white !important;
        padding: 0.8em 1.5em !important;
        font-size: 1em !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #00ffc8 !important;
        box-shadow: 0 0 20px rgba(0,255,200,0.2) !important;
    }
    .stButton > button {
        background: linear-gradient(135deg, #00ffc8, #00a896) !important;
        color: #0a0a0a !important;
        border: none !important;
        border-radius: 50px !important;
        font-weight: 900 !important;
        padding: 0.7em 2em !important;
        width: 100% !important;
        box-shadow: 0 4px 15px rgba(0,255,200,0.3) !important;
        letter-spacing: 1px !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(0,255,200,0.5) !important;
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
    st.markdown("""
    <p style="font-size:3.5em;font-weight:900;
    background:linear-gradient(90deg,#00ffc8,#00a896,#007cf0);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
    margin-bottom:0;">🤖 AutoBot</p>
    """, unsafe_allow_html=True)
    st.markdown("""
    <p style="color:#8892a4;font-size:1em;letter-spacing:2px;
    text-transform:uppercase;">
    Assistant IA • TinyLLaMA & RAG • Renault Expert
    </p>""", unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div style="margin-top:2em;">
        <span style="display:inline-flex;align-items:center;gap:0.5em;
        background:rgba(0,255,200,0.08);
        border:1px solid rgba(0,255,200,0.3);
        border-radius:50px;padding:0.4em 1.2em;
        color:#00ffc8;font-size:0.85em;letter-spacing:1px;">
            <span style="width:8px;height:8px;background:#00ffc8;
            border-radius:50%;display:inline-block;"></span>
            EN LIGNE
        </span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Initialise historique
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "bot",
            "content": "Bonjour ! Je suis AutoBot, votre expert en mecanique Renault. Je suis propulse par TinyLLaMA et une base de connaissances technique complete sur toute la gamme Renault. Comment puis-je vous aider aujourd'hui ?"
        }
    ]

# Zone de chat
# Zone de chat
st.markdown("""
<p style="color:#00ffc8;font-size:0.85em;
text-transform:uppercase;letter-spacing:2px;">
💬 Conversation
</p>""", unsafe_allow_html=True)

for msg in st.session_state.messages:
    if msg["role"] == "user":
        col1, col2 = st.columns([1, 4])
        with col2:
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#00ffc8,#00a896);
            color:#0a0a0a;border-radius:20px 20px 5px 20px;
            padding:1em 1.5em;margin:0.5em 0;
            font-weight:600;box-shadow:0 4px 15px rgba(0,255,200,0.3);">
            👤 {msg['content']}
            </div>""", unsafe_allow_html=True)
    else:
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.05);
            border:1px solid rgba(0,255,200,0.15);
            color:#cccccc;border-radius:5px 20px 20px 20px;
            padding:1em 1.5em;margin:0.5em 0;line-height:1.8;
            box-shadow:0 4px 15px rgba(0,0,0,0.2);">
            🤖 {msg['content']}
            </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Input
col1, col2 = st.columns([5, 1])
with col1:
    user_input = st.text_input(
        "message",
        placeholder="Posez votre question sur votre Renault...",
        label_visibility="collapsed",
        key="chat_input"
    )
with col2:
    send = st.button("Envoyer ⚡", use_container_width=True)

# Questions rapides
st.markdown("""
<p style="color:#8892a4;font-size:0.8em;text-transform:uppercase;
letter-spacing:2px;margin:1em 0 0.8em 0;">
💬 Questions rapides</p>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("🔍 Analyser mon véhicule", use_container_width=True):
        user_input = "Comment analyser mon vehicule sur PredictDrive ?"
        send = True
with col2:
    if st.button("🌡️ Moteur qui chauffe", use_container_width=True):
        user_input = "Mon moteur chauffe beaucoup, que faire ?"
        send = True
with col3:
    if st.button("🛢️ Pression huile faible", use_container_width=True):
        user_input = "Ma pression huile est faible, est-ce dangereux ?"
        send = True
with col4:
    if st.button("🔋 Batterie faible", use_container_width=True):
        user_input = "Ma batterie est faible, que faire ?"
        send = True

col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("⚙️ Pannes Clio 4", use_container_width=True):
        user_input = "Quelles sont les pannes frequentes de la Renault Clio 4 ?"
        send = True
with col2:
    if st.button("🚗 Entretien Megane", use_container_width=True):
        user_input = "Quels sont les intervalles d'entretien de la Renault Megane 4 ?"
        send = True
with col3:
    if st.button("⚡ Pannes Zoe", use_container_width=True):
        user_input = "Quelles sont les pannes frequentes de la Renault Zoe ?"
        send = True
with col4:
    if st.button("🔧 Code P0300", use_container_width=True):
        user_input = "J'ai le code defaut P0300 sur ma Renault, que faire ?"
        send = True

# Traitement
if send and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("AutoBot réfléchit..."):
        try:
            response = requests.post(
                "http://127.0.0.1:8000/api/chat",
                json={"message": user_input},
                timeout=120
            )
            if response.status_code == 200:
                bot_response = response.json()["response"]
            else:
                bot_response = "Desolee, je rencontre un probleme technique."
        except requests.exceptions.Timeout:
            bot_response = "Le modele prend trop de temps. Reessayez."
        except Exception:
            bot_response = "Je ne peux pas me connecter au serveur."
    st.session_state.messages.append({"role": "bot", "content": bot_response})
    st.rerun()