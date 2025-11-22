import random
import time
from ..db.database import load_otps, save_otps
from ..config import OTP_EXPIRY_SECONDS

def generate_otp(user_id: int):
    otps = load_otps()
    otp = str(random.randint(100000, 999999))
    
    otps[str(user_id)] = {
        "otp": otp,
        "timestamp": int(time.time()),
        "verified": False
    }
    save_otps(otps)
    
    return otp

def verify_otp(user_id: int, otp_entered: str):
    otps = load_otps()
    
    if str(user_id) not in otps:
        return {"success": False, "msg": "OTP not generated"}

    saved = otps[str(user_id)]

    if int(time.time()) - saved["timestamp"] > OTP_EXPIRY_SECONDS:
        return {"success": False, "msg": "OTP expired"}

    if saved["otp"] != otp_entered:
        return {"success": False, "msg": "Incorrect OTP"}

    saved["verified"] = True
    save_otps(otps)
    
    return {"success": True, "msg": "OTP verified"}

def send_otp_to_user(user_id: int, phone: str):
    otp = generate_otp(user_id)
    # SMS sending disabled for demo
    return {"status": "sent", "otp": otp}