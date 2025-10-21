# router_comparison.py
"""
Router Comparison Module
Compares multiple routers from the database by key specs
"""
from router_database import ROUTER_DATABASE

def compare_routers(models):
    """
    models: list of model names
    Returns formatted comparison text
    """
    specs_to_compare = [
        'Producent', 'Data produkcji', 'Rodzaj sygnału WiFi', 'Maksymalna przepustowość WiFi',
        'Maksymalna przepustowość Ethernet', 'Lista funkcji'
    ]
    # Header
    table = """
Comparison Results:

"""
    # Column headings
    header = "Model".ljust(30)
    for m in models:
        header += m.ljust(30)
    table += header + "\n" + "-"* (30*(len(models)+1)) + "\n"
    # Rows
    for key in specs_to_compare:
        row = key.ljust(30)
        for m in models:
            val = ROUTER_DATABASE.get(m, {}).get(key, 'N/A')
            row += str(val)[:28].ljust(30)
        table += row + "\n"
    return table
