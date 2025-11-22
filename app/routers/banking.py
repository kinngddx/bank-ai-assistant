from fastapi import APIRouter, HTTPException
from ..db.database import load_db, save_db
from ..services.otp_service import generate_otp
from ..utils.logger import log_info, log_warning, log_error, log_security
router = APIRouter()

@router.get("/balance")
def get_balance(user_id: int):
    db = load_db()
    user = next((u for u in db["users"] if u["id"] == user_id), None)

    if not user:
        log_error("User not found", user_id)
        raise HTTPException(status_code=404, detail="User not found")

    log_info(f"Balance checked: ${user['balance']}", user_id)
    return {"balance": user["balance"], "name": user["name"]}


@router.post("/transfer/initiate")
def initiate_transfer(user_id: int, recipient_id: int, amount: float):
    """Step 1: Validate transfer and request OTP"""
    db = load_db()
    
    sender = next((u for u in db["users"] if u["id"] == user_id), None)
    recipient = next((u for u in db["users"] if u["id"] == recipient_id), None)

    if not sender:
        raise HTTPException(status_code=404, detail="Sender not found")
    if not recipient:
        raise HTTPException(status_code=404, detail="Recipient not found")
    if sender["balance"] < amount:
        log_warning(f"Insufficient balance for transfer: ${amount}", user_id)
        raise HTTPException(status_code=400, detail="Insufficient balance")
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")

    # Store pending transfer
    transfer_id = len(db.get("pending_transfers", [])) + 1
    if "pending_transfers" not in db:
        db["pending_transfers"] = []
    
    db["pending_transfers"].append({
        "transfer_id": transfer_id,
        "sender_id": user_id,
        "recipient_id": recipient_id,
        "amount": amount,
        "status": "pending_otp"
    })
    save_db(db)

    # Generate OTP
    otp = generate_otp(user_id)
    
    log_security(f"Transfer initiated: ${amount} to user {recipient_id}", user_id)
    
    return {
        "action": "REQUIRE_OTP",
        "message": f"OTP sent to your phone. Please verify to transfer ${amount} to {recipient['name']}",
        "transfer_id": transfer_id,
        "otp_for_demo": otp  # Remove in production!
    }


@router.post("/transfer/complete")
def complete_transfer(user_id: int, transfer_id: int, otp: str):
    """Step 2: Verify OTP and complete transfer"""
    from ..services.otp_service import verify_otp
    
    # Verify OTP first
    otp_result = verify_otp(user_id, otp)
    if not otp_result["success"]:
        log_security(f"Failed OTP verification: {otp_result['msg']}", user_id)
        raise HTTPException(status_code=401, detail=otp_result["msg"])

    db = load_db()
    
    # Find pending transfer
    transfer = next((t for t in db.get("pending_transfers", []) if t["transfer_id"] == transfer_id), None)
    if not transfer:
        raise HTTPException(status_code=404, detail="Transfer not found")
    if transfer["sender_id"] != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    if transfer["status"] != "pending_otp":
        raise HTTPException(status_code=400, detail="Transfer already processed")

    # Execute transfer
    sender = next(u for u in db["users"] if u["id"] == transfer["sender_id"])
    recipient = next(u for u in db["users"] if u["id"] == transfer["recipient_id"])

    sender["balance"] -= transfer["amount"]
    recipient["balance"] += transfer["amount"]
    transfer["status"] = "completed"

    # Log transaction
    if "transactions" not in db:
        db["transactions"] = []
    db["transactions"].append({
        "type": "transfer",
        "from": sender["id"],
        "to": recipient["id"],
        "amount": transfer["amount"]
    })

    save_db(db)
    
    log_info(f"Transfer completed: ${transfer['amount']} to {recipient['name']}", user_id)

    return {
        "message": "Transfer successful!",
        "amount": transfer["amount"],
        "recipient": recipient["name"],
        "new_balance": sender["balance"]
    }