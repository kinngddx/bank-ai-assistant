from fastapi import APIRouter
from ..services.nlp_service import predict_intent

router = APIRouter()

@router.post("/")
def process_command(text: str, user_id: int):
    # send text to NLP model
    result = predict_intent(text)

    return {
        "intent": result["intent"],
        "entities": result.get("entities", {}),
        "message": "Intent detected successfully"
    }
