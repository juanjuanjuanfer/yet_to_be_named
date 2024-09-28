import json

def read_json(file):
    with open(file, 'r', encoding='utf-8') as file:
        return json.load(file)
    
