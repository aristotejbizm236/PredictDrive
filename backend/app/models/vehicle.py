from pydantic import BaseModel, Field
from typing import Literal, List

class VehicleInput(BaseModel):
    matricule: str = Field(..., example="AB-123-CD")
    kilometrage: int = Field(..., ge=0, le=500000, example=95000)
    age_vehicule: int = Field(..., ge=1, le=50, example=7)
    regime_moteur: int = Field(..., ge=500, le=8000, example=3200)
    temperature_moteur: int = Field(..., ge=40, le=150, example=95)
    pression_huile: float = Field(..., ge=0.0, le=6.0, example=2.5)
    tension_batterie: float = Field(..., ge=9.0, le=16.0, example=12.6)
    type_carburant: Literal["essence", "diesel"] = Field(..., example="diesel")
    nbre_entretiens: int = Field(..., ge=0, le=50, example=5)

class PredictionOutput(BaseModel):
    matricule: str
    etat: str
    score_xgboost: float
    score_random_forest: float
    anomalie_detectee: bool
    recommandation: str
    pieces_a_verifier: List[str]