import sys
sys.stdout.reconfigure(encoding='utf-8')

import os
import ollama
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings

# Chemins
KB_PATH = os.path.join(os.path.dirname(__file__), "../../ml/knowledge_base")
CHROMA_PATH = os.path.join(os.path.dirname(__file__), "../../ml/chroma_db")

def load_knowledge_base():
    """Charge et indexe les documents dans ChromaDB."""
    documents = []
    
    for filename in os.listdir(KB_PATH):
        if filename.endswith(".txt"):
            filepath = os.path.join(KB_PATH, filename)
            loader = TextLoader(filepath, encoding="utf-8")
            documents.extend(loader.load())
    
    # Découpe les documents en chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(documents)
    
    # Crée la base vectorielle
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )
    print("Knowledge base chargee avec succes !")
    return vectorstore

def get_vectorstore():
    """Charge la base vectorielle existante ou en crée une nouvelle."""
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    
    if os.path.exists(CHROMA_PATH):
        vectorstore = Chroma(
            persist_directory=CHROMA_PATH,
            embedding_function=embeddings
        )
    else:
        vectorstore = load_knowledge_base()
    
    return vectorstore

def chat_with_rag(question: str, vehicle_context: dict = None) -> str:
    """
    Répond à une question en utilisant RAG + Phi-3 via Ollama.
    """
    try:
        print(f"Question recue : {question}")
        
        print("Chargement vectorstore...")
        vectorstore = get_vectorstore()
        
        print("Recherche documents pertinents...")
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
        relevant_docs = retriever.invoke(question)
        context = "\n".join([doc.page_content for doc in relevant_docs])
        print(f"Contexte trouve : {len(context)} caracteres")

        vehicle_info = ""
        if vehicle_context:
            vehicle_info = f"""
Informations du vehicule analyse :
- Kilometrage : {vehicle_context.get('kilometrage', 'N/A')} km
- Age : {vehicle_context.get('age_vehicule', 'N/A')} ans
- Temperature moteur : {vehicle_context.get('temperature_moteur', 'N/A')} C
- Pression huile : {vehicle_context.get('pression_huile', 'N/A')} bar
- Tension batterie : {vehicle_context.get('tension_batterie', 'N/A')} V
- Etat detecte : {vehicle_context.get('etat', 'N/A')}
"""

        prompt = f"""Tu es AutoBot, l'assistant expert en mecanique automobile de PredictDrive.
Tu aides les utilisateurs a comprendre l'etat de leur vehicule Renault Clio 4
et tu leur proposes des solutions concretes basees sur la documentation technique.

Contexte technique disponible :
{context}

{vehicle_info}

Question de l'utilisateur : {question}

Reponds de facon claire, professionnelle et en francais.
Si l'utilisateur veut analyser son vehicule, dis-lui de remplir 
le formulaire dans la page Analyse.
Limite ta reponse a 3-4 phrases maximum."""

        print("Appel Ollama Phi-3...")
        response = ollama.chat(
            model="tinyllama",
            messages=[{"role": "user", "content": prompt}]
        )
        print("Reponse Ollama recue !")
        return response['message']['content']

    except Exception as e:
        print(f"ERREUR chat_with_rag : {e}")
        raise e

def get_quick_response(message: str) -> str:
    """
    Réponses rapides sans appel LLM pour les questions simples.
    """
    message_lower = message.lower()
    
    if any(word in message_lower for word in ["bonjour", "salut", "hello", "bonsoir"]):
        return "Bonjour ! Je suis AutoBot, votre assistant PredictDrive. Comment puis-je vous aider avec votre vehicule aujourd'hui ?"
    
    if any(word in message_lower for word in ["analyser", "analyse", "diagnostic", "tester"]):
        return "Pour analyser votre vehicule, rendez-vous sur la page Analyse dans le menu de gauche. Remplissez les informations de votre vehicule et obtenez une prediction instantanee !"
    
    if any(word in message_lower for word in ["merci", "thanks"]):
        return "De rien ! N'hesitez pas si vous avez d'autres questions sur votre vehicule."
    
    return None