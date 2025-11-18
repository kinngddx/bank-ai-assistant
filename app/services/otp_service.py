import random
import time
from app.database import read_json, write_json
from app.services.sms_service import send_sms

OTP_EXPIRY_SECONDS = 120   # 2 minutes

def generate_otp(user_id: int):
    otps = read_json("otps.json")

    otp = random.randint(100000, 999999)
    timestamp = int(time.time())

    otps[user_id] = {
        "otp": str(otp),
        "timestamp": timestamp,
        "verified": False
    }

    write_json("otps.json", otps)

    return otp


def send_otp_to_user(user_id: int, phone: str):
    otp = generate_otp(user_id)
    msg = f"Your OTP is {otp}. Do not share with anyone."

    send_sms(phone, msg)
    return {"status": "sent"}


def verify_otp(user_id: int, otp_entered: str):
    otps = read_json("otps.json")

    if user_id not in otps:
        return {"success": False, "msg": "OTP not generated"}

    saved = otps[user_id]

    # Check expiry
    if int(time.time()) - saved["timestamp"] > OTP_EXPIRY_SECONDS:
        return {"success": False, "msg": "OTP expired"}

    # Check match
    if saved["otp"] != otp_entered:
        return {"success": False, "msg": "Incorrect OTP"}

    saved["verified"] = True
    write_json("otps.json", otps)

    return {"success": True, "msg": "OTP verified"}
