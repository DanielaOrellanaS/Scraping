import requests
import re

# Tu API Key de ScraperAPI
API_KEY = '8434e1feaa5b735ea88308c68361f8e0'
# La URL de la página de Fear and Greed
TARGET_URL = 'https://edition.cnn.com/markets/fear-and-greed'

# Construimos la URL de ScraperAPI con el parámetro render
payload = {
    'api_key': API_KEY,
    'url': TARGET_URL,
    'render': 'true'  # Habilitamos renderizado de JS
}

# Hacemos la solicitud a ScraperAPI
response = requests.get('https://api.scraperapi.com/', params=payload)

# Si todo fue bien, obtenemos el HTML renderizado
html = response.text

# Buscamos el valor del índice usando una expresión regular
match = re.search(r'<span class="market-fng-gauge__dial-number-value">(\d+)</span>', html)

if match:
    print(f"Fear and Greed Index: {match.group(1)}")
else:
    print("No se encontró el índice.")
