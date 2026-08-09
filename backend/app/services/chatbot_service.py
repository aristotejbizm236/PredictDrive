import sys
sys.stdout.reconfigure(encoding='utf-8')

import os
import re
import ollama
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings

KB_PATH = os.path.join(os.path.dirname(__file__), "../../ml/knowledge_base")
CHROMA_PATH = os.path.join(os.path.dirname(__file__), "../../ml/chroma_db")

def load_knowledge_base():
    documents = []
    for filename in os.listdir(KB_PATH):
        if filename.endswith(".txt"):
            filepath = os.path.join(KB_PATH, filename)
            loader = TextLoader(filepath, encoding="utf-8")
            documents.extend(loader.load())

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(documents)

    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )
    print("Knowledge base chargee avec succes !")
    return vectorstore

def get_vectorstore():
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    if os.path.exists(CHROMA_PATH):
        vectorstore = Chroma(
            persist_directory=CHROMA_PATH,
            embedding_function=embeddings
        )
    else:
        vectorstore = load_knowledge_base()
    return vectorstore

def clean_response(text: str) -> str:
    """Nettoie la réponse de TinyLLaMA."""
    # Supprime les balises
    for tag in ["[SYS]", "<<SYS>>", "<</SYS>>", "[INST]",
                "[/INST]", "<<USER>>", "<<ASSISTANT>>",
                "<s>", "</s>", "[/s]"]:
        text = text.replace(tag, "")

    # Supprime le markdown
    text = re.sub(r'\*\*.*?\*\*', lambda m: m.group(0).replace('**', ''), text)
    text = re.sub(r'#{1,6}\s.*?\n', '', text)
    text = re.sub(r'\*+', '', text)
    text = re.sub(r'_{1,2}.*?_{1,2}', '', text)
    text = re.sub(r'\n{3,}', '\n\n', text)

    # Supprime les phrases en anglais
    lines = text.split('\n')
    french_lines = []
    english_indicators = [
        "sure", "here's", "here is", "i'll", "i will",
        "let me", "of course", "certainly", "absolutely"
    ]
    for line in lines:
        line_lower = line.lower().strip()
        if not any(indicator in line_lower for indicator in english_indicators):
            french_lines.append(line)

    text = '\n'.join(french_lines)
    return text.strip()

def chat_with_rag(question: str, vehicle_context: dict = None) -> str:
    try:
        print(f"Question recue : {question}")

        print("Chargement vectorstore...")
        vectorstore = get_vectorstore()

        print("Recherche documents pertinents...")
        retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
        relevant_docs = retriever.invoke(question)
        context = "\n".join([doc.page_content for doc in relevant_docs])[:400]
        print(f"Contexte trouve : {len(context)} caracteres")

        vehicle_info = ""
        if vehicle_context:
            vehicle_info = f"""Vehicule : kilometrage {vehicle_context.get('kilometrage', 'N/A')} km, age {vehicle_context.get('age_vehicule', 'N/A')} ans, temperature {vehicle_context.get('temperature_moteur', 'N/A')}C, pression huile {vehicle_context.get('pression_huile', 'N/A')} bar, batterie {vehicle_context.get('tension_batterie', 'N/A')}V, etat {vehicle_context.get('etat', 'N/A')}."""

        print("Appel Ollama Phi3...")
        response = ollama.chat(
            model="phi3",
            messages=[
                {
                    "role": "system",
                    "content": "Tu es AutoBot, expert Renault. Reponds UNIQUEMENT en francais. Texte simple sans markdown. 2 phrases maximum. Direct et pratique."
                },
                {
                    "role": "user",
                    "content": f"Contexte technique : {context}\n\n{vehicle_info}\n\nQuestion : {question}\n\nReponse courte en francais :"
                }
            ],
            options={
                "temperature": 0.1,
                "num_predict": 120,
                "stop": ["Question :", "Contexte :", "\n\n\n"]
            }
        )
        print("Reponse Ollama recue !")

        raw = response['message']['content']
        cleaned = clean_response(raw)

        if not cleaned or len(cleaned) < 10:
            return "Verifiez votre vehicule aupres d un mecanicien Renault agree pour ce type de probleme."

        return cleaned

    except Exception as e:
        print(f"ERREUR chat_with_rag : {e}")
        raise e

def get_quick_response(message: str) -> str:
    message_lower = message.lower()

    if any(word in message_lower for word in
           ["bonjour", "salut", "hello", "bonsoir"]):
        return "Bonjour ! Je suis AutoBot, votre expert Renault de PredictDrive. Comment puis-je vous aider ?"

    if any(word in message_lower for word in
           ["analyser", "analyse", "diagnostic", "tester"]):
        return "Pour analyser votre vehicule, rendez-vous sur la page Analyse dans le menu de gauche et remplissez le formulaire !"

    if any(word in message_lower for word in ["merci", "thanks"]):
        return "De rien ! N hesitez pas si vous avez d autres questions sur votre Renault."

    return None