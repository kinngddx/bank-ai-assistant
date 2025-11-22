import pickle
import re
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "../../ml/intent_model.pkl")
VECTORIZER_PATH = os.path.join(os.path.dirname(__file__), "../../ml/vectorizer.pkl")

# Load model
try:
    with open(VECTORIZER_PATH, "rb") as f:
        vectorizer = pickle.load(f)
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    MODEL_LOADED = True
except:
    MODEL_LOADED = False

def extract_amount(text: str):
    match = re.search(r"\b(\d+)\b", text)
    return int(match.group()) if match else None

def extract_recipient(text: str):
    names = ["raju", "mom", "dad", "rahul", "john", "sarah"]
    for word in text.lower().split():
        if word in names:
            return word.capitalize()
    return None

def predict_intent(text: str):
    if not MODEL_LOADED:
        # Fallback: keyword-based
        text_lower = text.lower()
        if any(w in text_lower for w in ["balance", "how much", "money have"]):
            intent = "CheckBalance"
        elif any(w in text_lower for w in ["transfer", "send", "pay"]):
            intent = "TransferMoney"
        elif any(w in text_lower for w in ["otp", "verify", "code"]):
            intent = "VerifyOTP"
        else:
            intent = "Unknown"
    else:
        X = vectorizer.transform([text])
        intent = model.predict(X)[0]

    entities = {}
    if intent == "TransferMoney":
        if amt := extract_amount(text):
            entities["amount"] = amt
        if rec := extract_recipient(text):
            entities["recipient"] = rec
    if intent == "VerifyOTP":
        if otp := extract_amount(text):
            entities["otp"] = otp

    return {"intent": intent, "entities": entities}