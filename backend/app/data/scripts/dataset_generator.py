"""
Generamos un archivo .py que es ejecutado una unica vez, al iniciar la app,
o posteriormente si lo aztualizamos;
este codigo genera un archivo .json,
que será usado como un diccionario comprimido para buscar de forma rapida y
eficiente cuando el usuario quiera usar filtros.
"""

import json
import time
from pathlib import Path

import requests

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


def fetch_with_retry(session, url, name, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            if attempt == max_retries - 1:
                print(f"[ERROR FINAL] {name}: {e}")
    return None


def dataset_pokemon():

    url_base = "https://pokeapi.co/api/v2/pokemon?limit=1025"
    minibiblioteca = []

    session = requests.Session()

    print("Generando indice primordial Pokemon... tardará unos minutos 🌐")

    try:
        response = session.get(url_base, timeout=10)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Ha ocurrido un Error al conectar con la API: {e}")
        return

    for i, entry in enumerate(data["results"], 1):
        pokemon_data = fetch_with_retry(session, entry["url"], entry["name"])
        time.sleep(0.4)

        if not pokemon_data:
            continue

        p_id = pokemon_data["id"]

        # Extraemos de manera segura mediante mapeo dinámico
        # (Evitando IndexError si cambia el orden)
        stats_map = {s["stat"]["name"]: s["base_stat"] for s in pokemon_data["stats"]}

        # Extraemos de forma segura el arte oficial
        other_sprites = pokemon_data.get("sprites", {}).get("other", {})
        official_artwork = other_sprites.get("official-artwork", {})
        sprite_url = official_artwork.get("front_default", "")

        mini_datos = {
            "id": p_id,
            "name": pokemon_data["name"],
            "generation": get_generation_by_id(p_id),
            "types": [t["type"]["name"] for t in pokemon_data["types"]],
            "hp": stats_map.get("hp", 0),
            "attack": stats_map.get("attack", 0),
            "defense": stats_map.get("defense", 0),
            "speed": stats_map.get("speed", 0),
            "base_exp": pokemon_data.get("base_experience", 0),
            "sprite": sprite_url,
        }

        minibiblioteca.append(mini_datos)

        if i % 50 == 0:
            print(f"Cargados {i} Pokemon...")

    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(minibiblioteca, f, indent=4, ensure_ascii=False)

        print(f"\n¡Archivo generado correctamente en: {OUTPUT_FILE}!")

    except Exception as e:
        print(f"Error al escribir el archivo: {e}")


def load_dataset():
    """Carga el dataset utilizando la ruta absoluta calculada del sistema."""

    try:
        with open(OUTPUT_FILE, encoding="utf-8") as f:
            return json.load(f)

    except FileNotFoundError:
        print(f"[WARNING] No se encontró el dataset en {OUTPUT_FILE}")
        return []


if __name__ == "__main__":  # pragma: no cover
    dataset_pokemon()
