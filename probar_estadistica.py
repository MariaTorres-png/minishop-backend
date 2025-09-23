import requests
from datetime import date

BASE_URL = "http://127.0.0.1:5000"

# Tomamos fecha de hoy para probar
hoy = date.today().isoformat()

params = {
    "fecha_inicio": "2025-09-01",  # fecha vieja para asegurar rango amplio
    "fecha_fin": hoy
}

response = requests.get(f"{BASE_URL}/estadisticas/ventas", params=params)
print(f"Status code: {response.status_code}")
print(response.json())

