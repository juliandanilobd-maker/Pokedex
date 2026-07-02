"""
Módulo CLI - Herramienta de auditoria y diagnostico de la API.
Nos permite inspeccionar las respuestas del backend para trabajar con esa base
el frontend
"""

from __future__ import annotations

import requests

BASE_URL = "http://localhost:8000/api/v2"


def api_get_pokemon(identifier: str) -> dict:

    response = requests.get(f"{BASE_URL}/pokemon/{identifier}", timeout=3)
    response.raise_for_status()

    return response.json()


def api_get_evolution(identifier: str) -> dict:

    response = requests.get(f"{BASE_URL}/pokemon/{identifier}/evolution", timeout=3)
    response.raise_for_status()

    return response.json()


def api_get_combat_effecteviness(identifier: str) -> dict:

    response = requests.get(f"{BASE_URL}/pokemon/{identifier}/effectiveness", timeout=3)
    response.raise_for_status()

    return response.json()


def api_get_filtered(
    tipo: str | None,
    gen: int | None,
    hp: int,
    attack: int,
    defense: int,
    speed: int,
    base_exp: int,
) -> list[dict]:

    params: dict = {}

    if tipo:
        params["pokemon_type"] = tipo

    if gen and gen > 0:
        params["generation"] = gen

    if hp > 0:
        params["min_hp"] = hp

    if attack > 0:
        params["min_attack"] = attack

    if defense > 0:
        params["min_defense"] = defense

    if speed > 0:
        params["min_speed"] = speed

    if base_exp > 0:
        params["min_base_exp"] = speed

    response = requests.get(f"{BASE_URL}/filter", params=params, timeout=5)
    response.raise_for_status()

    return response.json()


def api_create_team(name: str, pokemon_ids: list[int]) -> dict:

    payload = {"name": name, "pokemon_ids": pokemon_ids}

    response = requests.post(f"{BASE_URL}/teams", json=payload, timeout=5)
    response.raise_for_status()

    return response.json()


def api_list_teams() -> list[dict]:

    response = requests.get(f"{BASE_URL}/teams", timeout=5)
    response.raise_for_status()

    return response.json()


def api_get_team(team_id: str) -> dict:

    response = requests.get(f"{BASE_URL}/teams/{team_id}", timeout=5)
    response.raise_for_status()

    return response.json()


def api_delete_team(team_id: str) -> None:

    response = requests.delete(f"{BASE_URL}/teams/{team_id}", timeout=5)
    response.raise_for_status()


def api_get_average_by_type() -> list[dict]:

    response = requests.get(f"{BASE_URL}/analytics/average-by-type", timeout=5)
    response.raise_for_status()

    return response.json()


def api_get_top(metric: str = "attack", n: int = 10) -> list[dict]:

    params = {"metric": metric, "n": n}

    response = requests.get(f"{BASE_URL}/analytics/top", params=params, timeout=5)
    response.raise_for_status()

    return response.json()


def api_get_anomalies() -> list[dict]:

    response = requests.get(f"{BASE_URL}/analytics/anomalies", timeout=5)
    response.raise_for_status()

    return response.json()


def load_dataset() -> list[dict]:
    return api_get_filtered(
        tipo=None, gen=None, hp=0, attack=0, defense=0, speed=0, base_exp=0
    )

def api_get_simulation(n: int, pokemon_type: str, generation: int, seed: int | None = None) -> dict:

    params = {"n":n, "pokemon_type": pokemon_type, "generation": generation}

    if seed is not None:
        params["seed"] = seed

    response = requests.post (f"{BASE_URL}/analytics/simulate", params=params, timeout=5)
    response.raise_for_status()

    return response.json()

def api_get_prediction(primary_type: str, secondary_type: str | None = None) -> list[dict]:

    params = {"primary_type": primary_type, "secondary_type": secondary_type}
    response = requests.get(f"{BASE_URL}/analytics/prediction", params=params, timeout=5)
    response.raise_for_status()

    return response.json()
