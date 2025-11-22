import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "mock_db.json")
OTP_PATH = os.path.join(os.path.dirname(__file__), "otps.json")

def load_db():
    if not os.path.exists(DB_PATH):
        init_db()
    with open(DB_PATH, "r") as f:
        return json.load(f)

def save_db(data):
    with open(DB_PATH, "w") as f:
        json.dump(data, f, indent=4)

def load_otps():
    if not os.path.exists(OTP_PATH):
        with open(OTP_PATH, "w") as f:
            json.dump({}, f)
    with open(OTP_PATH, "r") as f:
        return json.load(f)

def save_otps(data):
    with open(OTP_PATH, "w") as f:
        json.dump(data, f, indent=4)

def init_db():
    initial_data = {
        "users": [
            {
                "id": 1,
                "username": "Umang",
                "password": "1234",
                "name": "Umang chandra",
                "phone": "9876543210",
                "balance": 5000000.0
            },
            {
                "id": 2,
                "username": "Ujjwal",
                "password": "123456",
                "name": "Ujjwal bhai",
                "phone": "9876543211",
                "balance": 30000000.0
            }
        ],
        "transactions": [],
        "pending_transfers": []
    }
    save_db(initial_data)