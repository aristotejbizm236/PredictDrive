from fastapi import APIRouter, HTTPException
from app.models.vehicle import VehicleInput, PredictionOutput
from app.services.prediction_service import predict
from app.database.queries import save_prediction, get_all_predictions, get_prediction_by_matricule

router = APIRouter(prefix="/api", tags=["Predictions"])

@router.post("/predict", response_model=PredictionOutput)
def predict_breakdown(vehicle: VehicleInput):
    try:
        vehicle_dict = vehicle.dict()
        result = predict(vehicle_dict)
        save_prediction(vehicle_dict, result)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history")
def get_history():
    try:
        return get_all_predictions()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history/{matricule}")
def get_vehicle_history(matricule: str):
    try:
        return get_prediction_by_matricule(matricule)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))