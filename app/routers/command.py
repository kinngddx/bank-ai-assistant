from fastapi import APIRouter
from ..services.nlp_service import predict_intent
from ..utils.logger import log_info

router = APIRouter()

@router.post("/")
def process_command(text: str, user_id: int):
    log_info(f"Voice command: '{text}'", user_id)
    
    result = predict_intent(text)
    
    log_info(f"Intent detected: {result['intent']}", user_id)
    
    return {
        "intent": result["intent"],
        "entities": result.get("entities", {}),
        "message": f"Intent: {result['intent']}"
    }