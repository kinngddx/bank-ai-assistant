from fastapi import APIRouter, HTTPException
from ..db.database import load_db

router = APIRouter()

@router.post("/login")
def login(username: str, password: str):
    db = load_db()

    # find user
    user = next((u for u in db["users"] if u["username"] == username and u["password"] == password), None)

    if not user:    #yaha pr user nhi mila to
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {
        "message": "Login successful",
        "user_id": user["id"],
        "token": "mock_token_123"
    }
