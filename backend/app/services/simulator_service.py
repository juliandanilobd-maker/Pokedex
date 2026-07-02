"""Este módulo contiene el simulador de datos sintéticos

Genera estadísticas realistas para un Pokemon ficticio, basando
sus estadísticas en el mean +- std del dataset real.

Se acumulan en un fichero csv único, que se va llenando con cada simulación
sin borrar las filas anteriores"""

from __future__ import annotations

import random
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from backend.app.models.pokemon_models import SimulatorResult

SYNTHETIC_CSV = Path(__file__).resolve().parents[3] / "data" / "pokemon_sinteticos.csv"

VALID_TYPES = (
    "normal",
    "fire",
    "water",
    "grass",
    "electric",
    "ice",
    "fighting",
    "poison",
    "ground",
    "flying",
    "psychic",
    "bug",
    "rock",
    "ghost",
    "dragon",
    "dark",
    "steel",
    "fairy",
)

FALLBACK_RANGES = {
    "hp": {"mean": 65.0, "std": 25.0},
    "attack": {"mean": 75.0, "std": 30.0},
    "defense": {"mean": 70.0, "std": 28.0},
    "speed": {"mean": 65.0, "std": 28.0},
}

STAT_MIN = 1
STAT_MAX = 255


class SimulatorService:
    """Genera datasets sinteticos de un Pokemon ficticio"""

    def __init__(self, dataset_loader) -> None:
        self._dataset_loader = dataset_loader

    def _build_type_ranges(self) -> dict[str, dict[str, dict[str, float]]]:
        """Calcula mean y std de cada stat agrupados por tipo elemental"""

        try:
            dataset = self._dataset_loader()

            if not dataset:
                return {}

            df = pd.DataFrame(dataset)
            df_exploded = df.explode("types").rename(columns={"types": "type_name"})

            agg = (
                df_exploded.groupby("type_name")[["hp", "attack", "defense", "speed"]]
                .agg(["mean", "std"])
                .fillna(10)
            )

            ranges: dict[str, dict[str, dict[str, float]]] = {}

            for type_name in agg.index:
                ranges[type_name] = {}

                for stat in ("hp", "attack", "defense", "speed"):
                    ranges[type_name][stat] = {
                        "mean": float(agg.loc[type_name, (stat, "mean")]),  # type: ignore[arg-type]
                        "std": max(float(agg.loc[type_name, (stat, "std")]), 5.0),  # type: ignore[arg-type]
                    }

        except Exception:
            return {}

        return ranges

    def _sample_stat(self, stat: str, type_name: str, type_ranges: dict) -> int:
        """Genera un valor de stat usando la distribución de los parámetros/fallback"""

        if type_name in type_ranges and stat in type_ranges[type_name]:
            mean = type_ranges[type_name][stat]["mean"]
            std = type_ranges[type_name][stat]["std"]
        else:
            mean = FALLBACK_RANGES[stat]["mean"]
            std = FALLBACK_RANGES[stat]["std"]

        value = int(np.random.normal(mean, std))
        return max(STAT_MIN, min(STAT_MAX, value))

    def generate(
        self,
        n: int = 10,
        pokemon_type: str = "normal",
        generation: int = 1,
        seed: int | None = None,
    ) -> SimulatorResult:
        """Genera un Pokemon sintético y los acumula en el CSV

        Args:
            n: cantidad de Pokemon a generar
            pokemon_type: tipo elemental base para los nuevos Pokemon
            generation: generación a la que pertenecerán
            seed: semilla aleatoria

        Returns:
            SimulatorResult con el patch del CSV, cantidad y total en el fichero

        Raises:
            ValueError si los parámetros no entran en rango"""

        if not 1 <= n <= 1000:
            raise ValueError("El número de Pokemon a generar debe estar entre 1 y 1000")

        if pokemon_type.lower() not in VALID_TYPES:
            raise ValueError(
                f"Tipo '{pokemon_type}' no válidoUsa uno de: {', '.join(VALID_TYPES)}"
            )

        if not 1 <= generation <= 9:
            raise ValueError("La generación debe ser entre 1-9")

        if seed is not None:
            np.random.seed(seed)
            random.seed(seed)

        pokemon_type = pokemon_type.lower()
        type_ranges = self._build_type_ranges()
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")

        rows = []

        for i in range(1, n + 1):
            rows.append(
                {
                    "id": f"SIM-{pokemon_type}-gen{generation}-{timestamp}-{i:04d}",
                    "name": f"fakemon_{pokemon_type}_{timestamp}_{i:04d}",
                    "types": pokemon_type,
                    "generation": generation,
                    "hp": self._sample_stat("hp", pokemon_type, type_ranges),
                    "attack": self._sample_stat("attack", pokemon_type, type_ranges),
                    "defense": self._sample_stat("defense", pokemon_type, type_ranges),
                    "speed": self._sample_stat("speed", pokemon_type, type_ranges),
                    "is_synthetic": True,
                    "generated_at": timestamp,
                }
            )

        df_new = pd.DataFrame(rows)

        # Generamos la acumulación de datos en el CSV usando el mode='a'
        SYNTHETIC_CSV.parent.mkdir(parents=True, exist_ok=True)
        file_exists = SYNTHETIC_CSV.exists()

        df_new.to_csv(
            SYNTHETIC_CSV,
            mode="a" if file_exists else "w",
            header=not file_exists,
            index=False,
            encoding="utf-8",
        )

        try:
            with open(SYNTHETIC_CSV, encoding="utf-8") as f:
                total_accumulated = sum(1 for _ in f) - 1

        except Exception:
            total_accumulated = n

        return SimulatorResult(
            csv_path=str(SYNTHETIC_CSV),
            generated_count=n,
            total_accumulated=total_accumulated,
            pokemon_type=pokemon_type,
            generation=generation,
            message=(
                f"Se generaron {n} Pokémon sintéticos de tipo '{pokemon_type}' "
                f"(gen {generation}) y se añadieron al dataset acumulativo. "
                f"Total en el fichero: {total_accumulated} registros."
            ),
        )
