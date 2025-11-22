import os
import requests
from ..config import FAST2SMS_API_KEY

def send_sms(phone: str, message: str):
    if not FAST2SMS_API_KEY:
        return {"status": "skipped", "reason": "No API key"}
    
    url = "https://www.fast2sms.com/dev/bulkV2"
    headers = {
        "authorization": FAST2SMS_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "route": "v3",
        "sender_id": "TXTIND",
        "message": message,
        "language": "english",
        "numbers": phone
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        return response.json()
    except Exception as e:
        return {"error": str(e)}