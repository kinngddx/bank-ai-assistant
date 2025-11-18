import json 
import os

DB_PATH  =os.path.join(os.path.dirname(__file__), "mock_db.json")


def load_db():
    with open(DB_PATH, "r") as f:
        return json.load(f)
    

def save_db(data):
    with open(DB_PATH, "w") as f:
        json.dump(data, f, indent=4)