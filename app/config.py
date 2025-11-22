import os
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key-2024")
JWT_ALGORITHM = "HS256"
OTP_EXPIRY_SECONDS = 120
FAST2SMS_API_KEY = os.getenv("FAST2SMS_API_KEY", "")