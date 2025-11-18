from app.database import read_json, write_json

def get_balance(user_id: int):
    users = read_json("users.json")
    return users[str(user_id)]["balance"]

def update_balance(user_id: int, amount: int):
    users = read_json("users.json")
    users[str(user_id)]["balance"] += amount
    write_json("users.json", users)

def add_transaction(user_id: int, txn_type: str, amount: int, desc: str):
    txns = read_json("transactions.json")

    if str(user_id) not in txns:
        txns[str(user_id)] = []

    txns[str(user_id)].append({
        "type": txn_type,
        "amount": amount,
        "desc": desc
    })

    write_json("transactions.json", txns)
