"""
Biblioteka modeli routerów - router_database.py
Zawiera bazę 500+ modeli routerów z lat 2015-2025
"""

import csv
import os

def load_router_database(csv_file='router_database.csv'):
    """
    Ładuje bazę routerów z pliku CSV
    
    Args:
        csv_file (str): Ścieżka do pliku CSV z bazą routerów
        
    Returns:
        dict: Słownik z modelami routerów (klucz: nazwa modelu, wartość: specyfikacja)
    """
    database = {}
    
    # Sprawdź czy plik istnieje
    if not os.path.exists(csv_file):
        print(f"BŁĄD: Nie znaleziono pliku {csv_file}")
        return database
    
    try:
        with open(csv_file, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                model = row.get('Model')
                if model:  # Sprawdź czy model nie jest pusty
                    database[model] = row
        
        print(f"✓ Załadowano {len(database)} modeli routerów z bazy danych")
        return database
        
    except Exception as e:
        print(f"BŁĄD podczas ładowania bazy: {e}")
        return {}

# Główna baza danych routerów
ROUTER_DATABASE = load_router_database()

def get_router_info(model_name):
    """
    Pobiera informacje o konkretnym modelu routera
    
    Args:
        model_name (str): Nazwa modelu routera
        
    Returns:
        dict: Specyfikacja routera lub None jeśli nie znaleziono
    """
    return ROUTER_DATABASE.get(model_name)

def get_all_models():
    """
    Zwraca listę wszystkich dostępnych modeli routerów
    
    Returns:
        list: Lista nazw modeli
    """
    return sorted(list(ROUTER_DATABASE.keys()))

def get_models_by_producer(producer):
    """
    Zwraca modele routerów danego producenta
    
    Args:
        producer (str): Nazwa producenta
        
    Returns:
        list: Lista modeli danego producenta
    """
    return [model for model, spec in ROUTER_DATABASE.items() 
            if spec.get('Producent') == producer]

def get_producers():
    """
    Zwraca listę wszystkich producentów w bazie
    
    Returns:
        list: Posortowana lista producentów
    """
    producers = set()
    for spec in ROUTER_DATABASE.values():
        producer = spec.get('Producent')
        if producer:  # Sprawdź czy producent nie jest None lub pusty
            producers.add(producer)
    return sorted(producers)

def search_routers(keyword):
    """
    Wyszukuje routery po słowie kluczowym w nazwie modelu
    
    Args:
        keyword (str): Słowo kluczowe do wyszukania
        
    Returns:
        list: Lista modeli pasujących do zapytania
    """
    keyword_lower = keyword.lower()
    matches = [model for model in ROUTER_DATABASE.keys() 
               if keyword_lower in model.lower()]
    return sorted(matches)
