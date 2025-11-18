from fastapi import APIRouter, HTTPException
from ..db.database import load_db, save_db

router = APIRouter()

@router.get("/balance")
def get_balance(user_id: int):
    db = load_db()
    user = next((u for u in db["users"] if u["id"] == user_id), None)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"balance": user["balance"]}


@router.post("/transfer")
def transfer_money(user_id: int, amount: int):
    db = load_db()

    user = next((u for u in db["users"] if u["id"] == user_id), None)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user["balance"] < amount:
        raise HTTPException(status_code=400, detail="Insufficient balance😞")

    user["balance"] -= amount

    save_db(db)

    return {"message": f"Transfer successful😄. New balance = {user['balance']}"}
