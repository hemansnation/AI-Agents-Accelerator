import requests
import os
from dotenv import load_dotenv

load_dotenv()

def enrich_data(lead_id):
    response = requests.get(f'https://jsonplaceholder.typicode.com/users/{lead_id}')
    if response.status_code == 200:
        data = response.json()
        return {
            'company': data['company']['name'],
            'industry': 'tech' if 'tech' in data['company']['catchPhrase'] else 'other'
        }
    return {}