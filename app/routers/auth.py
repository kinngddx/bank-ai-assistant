from fastapi import APIRouter, HTTPException
from ..db.database import load_db
from ..utils.logger import log_info, log_warning

router = APIRouter()

@router.post("/login")
def login(username: str, password: str):
    db = load_db()
    user = next((u for u in db["users"] if u["username"] == username and u["password"] == password), None)

    if not user:
        log_warning(f"Failed login attempt for username: {username}")
        raise HTTPException(status_code=401, detail="Invalid username or password")

    log_info(f"User {user['name']} logged in", user["id"])
    
    return {
        "message": "Login successful",
        "user_id": user["id"],
        "name": user["name"],
        "token": f"token_{user['id']}_2024"
    }