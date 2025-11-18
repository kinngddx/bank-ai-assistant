import json
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Load training data
with open("ml/training_data.json", "r") as f:
    data = json.load(f)

texts = []
labels = []

for intent, examples in data.items():
    for ex in examples:
        texts.append(ex)
        labels.append(intent)

# Vectorizer
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)

# Model (Logistic Regression)
model = LogisticRegression(max_iter=200)
model.fit(X, labels)

# Save model
with open("ml/intent_model.pkl", "wb") as f:
    pickle.dump(model, f)

# Save vectorizer
with open("ml/vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

print("Training complete. Model saved!")
