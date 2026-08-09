import sys
sys.stdout.reconfigure(encoding='utf-8')

import os
import pdfplumber
import shutil

PDF_FOLDER = "backend/ml/knowledge_base/pdfs"
KB_FOLDER = "backend/ml/knowledge_base"
CHROMA_PATH = "backend/ml/chroma_db"

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extrait le texte d'un PDF page par page."""
    texte = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            print(f"  → {len(pdf.pages)} pages detectees")
            for i, page in enumerate(pdf.pages):
                content = page.extract_text()
                if content:
                    texte += f"\n--- Page {i+1} ---\n"
                    texte += content + "\n"
    except Exception as e:
        print(f"  ERREUR lecture PDF : {e}")
    return texte

def ingest_all_pdfs():
    """Convertit tous les PDFs en TXT et recrée la knowledge base."""
    
    os.makedirs(PDF_FOLDER, exist_ok=True)
    
    pdf_files = [f for f in os.listdir(PDF_FOLDER) if f.endswith('.pdf')]
    
    if not pdf_files:
        print("Aucun PDF trouve dans le dossier pdfs/")
        print(f"Place tes PDFs dans : {PDF_FOLDER}")
        return
    
    print(f"\n{len(pdf_files)} PDF(s) detecte(s) :")
    print("=" * 50)
    
    total_chars = 0
    converted = 0
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(PDF_FOLDER, pdf_file)
        txt_filename = pdf_file.replace('.pdf', '.txt')
        txt_path = os.path.join(KB_FOLDER, txt_filename)
        
        print(f"\nConversion : {pdf_file}")
        texte = extract_text_from_pdf(pdf_path)
        
        if texte.strip():
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(texte)
            total_chars += len(texte)
            converted += 1
            print(f"  Sauvegarde : {txt_filename}")
            print(f"  Taille : {len(texte)} caracteres")
        else:
            print(f"  ATTENTION : Aucun texte extrait de {pdf_file}")
            print(f"  Le PDF est peut-etre scanné (image)")
    
    print("\n" + "=" * 50)
    print(f"Conversion terminee !")
    print(f"  PDFs convertis : {converted}/{len(pdf_files)}")
    print(f"  Total caracteres : {total_chars}")
    
    # Recrée automatiquement ChromaDB
    if converted > 0:
        print("\nRecreation de la knowledge base ChromaDB...")
        if os.path.exists(CHROMA_PATH):
            shutil.rmtree(CHROMA_PATH)
            print("Ancienne ChromaDB supprimee")
        
        # Import et recréation
        sys.path.insert(0, os.path.abspath('.'))
        from backend.app.services.chatbot_service import load_knowledge_base
        load_knowledge_base()
        print("Knowledge base recreee avec succes !")

if __name__ == "__main__":
    ingest_all_pdfs()