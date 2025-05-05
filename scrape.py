from fastapi import FastAPI
import requests
import re
import threading
import time

app = FastAPI()

# Tu API Key de ScraperAPI
API_KEY = '8434e1feaa5b735ea88308c68361f8e0'
# La URL de la página de Fear and Greed
TARGET_URL = 'https://edition.cnn.com/markets/fear-and-greed'

# Variable global para almacenar el último valor
latest_index = None

def get_fear_and_greed_index():
    payload = {
        'api_key': API_KEY,
        'url': TARGET_URL,
        'render': 'true'
    }
    try:
        response = requests.get('https://api.scraperapi.com/', params=payload, timeout=60)
        html = response.text
        match = re.search(r'<span class="market-fng-gauge__dial-number-value">(\d+)</span>', html)
        if match:
            print(f"Nuevo índice obtenido: {match.group(1)}")
            return match.group(1)
    except Exception as e:
        print(f"Error al obtener índice: {e}")
    return None

def update_index_periodically():
    global latest_index
    while True:
        index = get_fear_and_greed_index()
        if index:
            latest_index = index
        time.sleep(3600)  # Espera una hora (3600 segundos)

@app.on_event("startup")
def start_background_task():
    thread = threading.Thread(target=update_index_periodically)
    thread.daemon = True
    thread.start()

@app.get("/fear-and-greed")
def read_fear_and_greed():
    if latest_index is not None:
        return {"fear_and_greed_index": latest_index}
    else:
        return {"error": "Índice no disponible todavía, inténtalo más tarde."}
