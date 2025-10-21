"""
Router Database Library
"""

import csv
import os

DB_FILE = 'router_database.csv'
ROUTER_DATABASE = {}

def load_database():
    global ROUTER_DATABASE
    if not os.path.exists(DB_FILE):
        print(f"⚠ Brak pliku: {DB_FILE}")
        return
    with open(DB_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            model = row.get('Model', '')
            if model:
                ROUTER_DATABASE[model] = row
    print(f"✓ Załadowano {len(ROUTER_DATABASE)} routerów")

def get_all_models():
    return sorted(ROUTER_DATABASE.keys())

def get_producers():
    producers = set()
    for spec in ROUTER_DATABASE.values():
        if spec.get('Producent'):
            producers.add(spec['Producent'])
    return sorted(producers)

def search_routers(keyword):
    return sorted([m for m in ROUTER_DATABASE if keyword.lower() in m.lower()])

load_database()
