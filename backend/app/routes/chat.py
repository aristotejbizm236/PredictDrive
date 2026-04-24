from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.chatbot_service import chat_with_rag, get_quick_response

router = APIRouter(prefix="/api", tags=["Chatbot"])

class ChatInput(BaseModel):
    message: str
    vehicle_context: dict = None

class ChatOutput(BaseModel):
    response: str

@router.post("/chat", response_model=ChatOutput)
def chat(input: ChatInput):
    try:
        # Vérifie d'abord les réponses rapides
        quick = get_quick_response(input.message)
        if quick:
            return {"response": quick}
        
        # Sinon utilise RAG + Phi-3
        response = chat_with_rag(input.message, input.vehicle_context)
        return {"response": response}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))