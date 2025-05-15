import os
import json
from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.getenv("DB_PATH", "")
DATABASE_FILE = os.getenv("DATABASE_FILE", "pokemon_collection.json")
FULL_DB_PATH = os.path.join(DB_PATH, DATABASE_FILE)

def load_pokemon_data():
    try:
        if not os.path.exists(FULL_DB_PATH):
            print(f"Database file '{FULL_DB_PATH}' not found. Starting with an empty collection.")
            return {}

        with open(FULL_DB_PATH, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Error decoding JSON from '{FULL_DB_PATH}'. Starting with an empty collection.")
        return {}
    except Exception as e:
        print(f"Unexpected error while loading data: {e}")
        return {}

def save_pokemon_data(pokemon_data):
    try:
        os.makedirs(os.path.dirname(FULL_DB_PATH), exist_ok=True)
        with open(FULL_DB_PATH, 'w') as f:
            json.dump(pokemon_data, f, indent=2)
        print(f"Pokemon data saved to '{FULL_DB_PATH}'.")
    except Exception as e:
        print(f"Unexpected error while saving data: {e}")
