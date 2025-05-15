import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
BASE_POKEAPI_URL = os.getenv("BASE_POKEAPI_URL", "https://pokeapi.co/api/v2/")

def get_pokemon_list():
    try:
        response = requests.get(f"{BASE_POKEAPI_URL}pokemon?limit=1000")
        response.raise_for_status()
        data = response.json()
        return [entry['name'] for entry in data.get('results', [])]
    except Exception as e:
        print(f"Error fetching Pokemon list: {e}")
        return None

def get_pokemon_details(name):
    try:
        response = requests.get(f"{BASE_POKEAPI_URL}pokemon/{name}")
        response.raise_for_status()
        data = response.json()
        return {
            "id": data['id'],
            "name": data['name'],
            "height": data['height'],
            "weight": data['weight'],
            "order": data['order']
        }
    except Exception as e:
        print(f"Error fetching details for {name}: {e}")
        return None
