import pickle
import re

# Load vectorizer + model
with open("ml/vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

with open("ml/intent_model.pkl", "rb") as f:
    model = pickle.load(f)

def extract_amount(text: str):
    match = re.search(r"\b(\d+)\b", text)
    return int(match.group()) if match else None

def extract_recipient(text: str):
    words = text.split()
    possible_names = ["raju", "mom", "dad", "rahul", "sister", "brother"]
    for w in words:
        if w.lower() in possible_names:
            return w.capitalize()
    return None

def predict_intent(text: str):
    # Convert text to vector
    X = vectorizer.transform([text])
    intent = model.predict(X)[0]

    entities = {}

    if intent == "TransferMoney":
        amount = extract_amount(text)
        recipient = extract_recipient(text)
        if amount:
            entities["amount"] = amount
        if recipient:
            entities["recipient"] = recipient

    if intent == "VerifyOTP":
        otp = extract_amount(text)
        if otp:
            entities["otp"] = otp

    return {
        "intent": intent,
        "entities": entities
    }
