"""
Este módulo se encarga de procesar el conjunto de datos cargado en memoria para ejecutar
filtrados por estadisticas, generaciones y tipos, combinados
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class FilterService:
    MAX_RESULTS = 150

    def __init__(self) -> None:
        """Inicializamos el Service configurando la ruta del dataset"""
        self.data_path = (
            Path(__file__).resolve().parent.parent
            / "data"
            / "data"
            / "pokemon_dataset.json"
        )

        self._pokemon_data: list[dict[str, Any]] | None = None

    # Carga de datos segura, si no carga el dataset, no falla la app
    def _load_data(self) -> list[dict[str, Any]]:

        if not self.data_path.exists():
            print(f"[FilterService] Archivo no encontrado:{self.data_path}")
            return []

        try:
            with open(self.data_path, encoding="utf-8") as f:
                data = json.load(f)

        except json.JSONDecodeError:
            print("[FilterService] JSON corrupto en dataset")
            return []

        except Exception as e:
            print(f"[FilterService] Error cargando el dataset: {e}")
            return []

        if isinstance(data, list):
            return data

        print("[FilterService] el Dataset no tiene formato válido")
        return []

    # Programamos Lazy Loading,
    # para cargar de forma eficiente los datos filtrados
    @property
    def pokemon_data(self) -> list[dict[str, Any]]:

        if self._pokemon_data is None:
            self._pokemon_data = self._load_data()
        return self._pokemon_data

    # Recarga el dataset sin reiniciar el servidor
    def reload(self) -> None:
        self._pokemon_data = self._load_data()

    # Lógica de filtros
    def filter_pokemons(
        self,
        pokemon_type: str | None = None,
        generation: int | None = None,
        min_id: int = 0,
        max_id: int = 0,
        min_attack: int = 0,
        min_hp: int = 0,
        min_defense: int = 0,
        min_base_exp: int = 0,
        min_speed: int = 0,
    ) -> list[dict[str, Any]]:

        # Iniciamos los tipos de filtros
        filtered = self.pokemon_data

        # Normalizar los datos
        if pokemon_type:
            pokemon_type = pokemon_type.lower().strip()
            filtered = [
                pokemon
                for pokemon in filtered
                if any(
                    pokemon_type == str(t).lower().strip()
                    for t in pokemon.get("types", [])
                )
            ]

        # Generación
        if generation:
            filtered = [
                pokemon
                for pokemon in filtered
                if pokemon.get("generation") == generation
            ]
        # Filtros por estadísticas
        # Rango de IDs
        if min_id > 0:
            filtered = [
                pokemon for pokemon in filtered if int(pokemon.get("id", 0)) >= min_id
            ]

        if max_id > 0:
            filtered = [
                pokemon for pokemon in filtered if int(pokemon.get("id", 0)) <= max_id
            ]

        if min_attack > 0:
            filtered = [
                pokemon
                for pokemon in filtered
                if int(pokemon.get("attack", 0)) >= min_attack
            ]

        if min_defense > 0:
            filtered = [
                pokemon
                for pokemon in filtered
                if int(pokemon.get("defense", 0)) >= min_defense
            ]

        if min_hp > 0:
            filtered = [
                pokemon for pokemon in filtered if int(pokemon.get("hp", 0)) >= min_hp
            ]

        if min_base_exp:
            filtered = [
                pokemon
                for pokemon in filtered
                if int(pokemon.get("base_exp", 0)) >= min_base_exp
            ]

        if min_speed:
            filtered = [
                pokemon
                for pokemon in filtered
                if int(pokemon.get("speed", 0)) >= min_speed
            ]

        return filtered[: self.MAX_RESULTS]
