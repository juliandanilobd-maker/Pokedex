"""
Generamos un archivo .py que es ejecutado una unica vez, al iniciar la app,
o posteriormente si lo aztualizamos;
este codigo genera un archivo .json,
que será usado como un diccionario comprimido para buscar de forma rapida y
eficiente cuando el usuario quiera usar filtros.
Implementamos un script que utiliza ThreadPoolExecutor, ya que el proceso es I/O
Bound, usamos HTTPAdapter que mantiene 15 sockets para conexión TCP/IP abiertas,
y utilizando una estrategia Backoff Exponencial para evitar sobrecarga de peticiones
"""
# ESTE MODULO NO CUMPLE EL REQUISITO DE 50 LINEAS, DEBIDO A QUE ESTE SCRIPT
# UTILIZA THREAD POOL, Y SE REQUIERE ESTABLECER LA LOGICA DE GENERACIONES
# ESTE SCRIPT GENERA EL DATASET SOBRE EL QUE FUNCIONAN VARIOS DE NUESTROS SERVICIOS
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
OUTPUT_FILE = DATA_DIR / "pokemon_dataset.json"


def get_generation_by_id(pokemon_id: int) -> int:
    """Calcula la generación por rangos ID para evitar llamadas extra innecesarias"""

    if 1 <= pokemon_id <= 151:
        return 1

    if 152 <= pokemon_id <= 251:
        return 2

    if 252 <= pokemon_id <= 386:
        return 3

    if 387 <= pokemon_id <= 493:
        return 4

    if 494 <= pokemon_id <= 649:
        return 5

    if 650 <= pokemon_id <= 721:
        return 6

    if 722 <= pokemon_id <= 809:
        return 7

    if 810 <= pokemon_id <= 898:
        return 8

    return 9  # ID's 899 y superiores pertenecen a Gen 9


# Creamos una sesión HTTP reutilizable con reintentos inteligentes y un backoff
def create_session() -> requests.Session:
    session = requests.Session()
    retries = Retry(
        total=5,  # Hasta 5 reintentos
        backoff_factor=0.5,  # Esperará incrementalmente el tiempo de espera (1, 2, etc)
        status_forcelist=[429, 500, 502, 503, 504],
        raise_on_status=False,
    )
    adapter = HTTPAdapter(pool_connections=15, pool_maxsize=15, max_retries=retries)
    session.mount("https://", adapter)
    return session


# Implementamos una función que descarga y transforma los datos de un único Pokemon
def process_single_pokemon(entry: dict, session: requests.Session) -> dict | None:
    url = entry["url"]
    name = entry["name"]

    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

    except Exception as e:
        print(f"[ERROR FINAL] {name}: {e}")
        return None

    p_id = data["id"]

    stats_map = {s["stat"]["name"]: s["base_stat"] for s in data["stats"]}

    other_sprites = data.get("sprites", {}).get("other", {})
    official_artwork = other_sprites.get("official-artwork", {})
    sprite_url = official_artwork.get("front_default", "")

    return {
        "id": p_id,
        "name": data["name"],
        "generation": get_generation_by_id(p_id),
        "types": [t["type"]["name"] for t in data["types"]],
        "hp": stats_map.get("hp", 0),
        "attack": stats_map.get("attack", 0),
        "defense": stats_map.get("defense", 0),
        "speed": stats_map.get("speed", 0),
        "base_exp": data.get("base_experience", 0),
        "sprite_url": sprite_url,
    }


def dataset_pokemon():

    url_base = "https://pokeapi.co/api/v2/pokemon?limit=1025"

    session = create_session()

    print("Generando indice primordial Pokemon... tardará unos minutos 🌐")

    try:
        response = session.get(url_base, timeout=10)
        response.raise_for_status()
        results = response.json()["results"]

    except Exception as e:
        print(f"Ha ocurrido un Error al conectar con la API: {e}")
        return

    minibiblioteca: list[dict] = []

    # Usamos un Pool para paralelizar el I/O bound de la red
    # Utilizando max_workers 10 acelera momentaneamente el script sin tumbar conexión
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [
            executor.submit(process_single_pokemon, entry, session) for entry in results
        ]

        for idx, future in enumerate(futures, 1):
            result = future.result()

            if result is not None:
                minibiblioteca.append(result)

            if idx % 100 == 0:
                print(f"Procesados{idx}/1025 Pokemon...")

        minibiblioteca.sort(key=lambda x: x["id"])

        try:
            DATA_DIR.mkdir(parents=True, exist_ok=True)

            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                json.dump(minibiblioteca, f, indent=4, ensure_ascii=False)

            print(
                f"\n¡Dataset generado con exito! Total: {len(minibiblioteca)} Pokemons"
            )

        except Exception as e:
            print(f"Error al escribir el archivo dataset: {e}")


# Carga el dataset utilizando la ruta absoluta calculada del sistema
def load_dataset():

    try:
        with open(OUTPUT_FILE, encoding="utf-8") as f:
            return json.load(f)

    except FileNotFoundError:
        print(f"[WARNING] No se encontró el dataset en {OUTPUT_FILE}")
        return []


if __name__ == "__main__":  # pragma: no cover
    dataset_pokemon()
