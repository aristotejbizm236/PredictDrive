import sys
sys.stdout.reconfigure(encoding='utf-8')

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.predict import router
from app.routes.chat import router as chat_router
from app.database.connection import init_database

app = FastAPI(
    title="PredictDrive API",
    description="API de prediction de pannes automobiles par IA",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    init_database()
    print("PredictDrive API demarree !")

app.include_router(router)
app.include_router(chat_router)

@app.get("/")
def root():
    return {"message": "PredictDrive API", "status": "online"}