from fastapi import FastAPI
from fastapi.responses import JSONResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from threading import Thread, Lock
import time

app = FastAPI()

# Cache compartido
cached_value = None
last_updated = 0
cache_lock = Lock()
UPDATE_INTERVAL = 60 * 10  # 10 minutos

def get_fear_and_greed():
    url = "https://edition.cnn.com/markets/fear-and-greed"
    service = Service('chromedriver.exe')
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        time.sleep(5)  # Espera a que cargue bien el contenido
        element = driver.find_element(By.CLASS_NAME, "market-fng-gauge__dial-number-value")
        value = element.text.strip()
        return value
    except Exception as e:
        print("Error al obtener índice:", e)
        return None
    finally:
        driver.quit()

def background_updater():
    global cached_value, last_updated
    while True:
        print("Actualizando índice Fear and Greed...")
        new_value = get_fear_and_greed()
        if new_value:
            with cache_lock:
                cached_value = new_value
                last_updated = time.time()
                print(f"Índice actualizado: {new_value}")
        else:
            print("No se pudo actualizar el índice.")
        time.sleep(UPDATE_INTERVAL)

@app.on_event("startup")
def start_updater_thread():
    updater_thread = Thread(target=background_updater, daemon=True)
    updater_thread.start()

@app.get("/getData")
def read_fear_and_greed():
    with cache_lock:
        if cached_value is None:
            return JSONResponse(status_code=503, content={"error": "Data not available yet"})
        return {
            "fear_and_greed_index": cached_value,
            "last_updated": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_updated))
        }
