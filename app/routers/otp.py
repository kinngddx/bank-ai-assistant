from fastapi import APIRouter, HTTPException
from ..services.otp_service import generate_otp, verify_otp, send_otp_to_user
from ..db.database import load_db
from ..utils.logger import log_info

router = APIRouter()

@router.post("/generate")
def request_otp(user_id: int):
    db = load_db()
    user = next((u for u in db["users"] if u["id"] == user_id), None)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    otp = generate_otp(user_id)
    log_info(f"OTP generated", user_id)
    
    return {
        "message": "OTP generated successfully",
        "otp": otp  # For demo only! Remove in production
    }

@router.post("/verify")
def verify_otp_endpoint(user_id: int, otp: str):
    result = verify_otp(user_id, otp)
    
    if not result["success"]:
        raise HTTPException(status_code=401, detail=result["msg"])
    
    return {"message": "OTP verified successfully"}

@router.post("/send")
def send_otp(user_id: int):
    """Send OTP via SMS"""
    db = load_db()
    user = next((u for u in db["users"] if u["id"] == user_id), None)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    result = send_otp_to_user(user_id, user["phone"])
    return result