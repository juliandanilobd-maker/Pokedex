"""Este módulo contiene el servicio de dominio encargado de las estadísticas
descriptivas y la detección de anomalías sobre el dataset Pokemon

No realiza llamadas a la PokeAPI: trabaja sobre el dataset ya creado y en local

Utiliza pandas como motor principal, aprovechando las funciones de agrupación:
1. groupby, que permite agrupar filas con un mismo valor
2. explode, que permite separar varios valores dentro de una celda
3. nlargest, que permite obtener las filas con los valores más altos en sus columnas

e integración:
1. mean, que calcula el promedio
2. std, que calcula la desviación estándar
3. quantile, que divide en cuantiles, los percentiles

Estas funciones simplifican el código y reduce el procesamiento de datasets grandes"""

# ESTE MODULO EXCEDE EL MAXIMO DE 50 LINEAS, DEBIDO A QUE CONTIENE LA LOGICA DE CALCULO
# DE MEDIAS, Y TOPS, A PESAR DE QUE EL USO DE PANDAS REDUCE LA CANTIDAD DE CODIGO
# MANUAL

from __future__ import annotations

import pandas as pd

from backend.app.models.pokemon_models import (
    AnomalyEntry,
    TopPokemonEntry,
    TypeAverageStats,
)

VALID_METRICS = ("hp", "attack", "defense", "speed", "base_exp")


class AnalyzerService:
    """Esta clase encapsula el análisis estadístico del dataset completo"""

    def __init__(self, dataset_loader) -> None:

        self._dataset_loader = dataset_loader

    def _load_dataframe(self) -> pd.DataFrame:
        """Carga el dataset y lo convierte en un Dataframe

        Returns:
            Devuelve un Dataframe con una fila por pokemon y como columnas id,
            name, types, sprite y las respectivas columnas de las métricas válidas

        Raises:
            ValueError, si el dataset está vacío o no se ha generado"""

        dataset = self._dataset_loader()

        if not dataset:
            raise ValueError(
                "El dataset local está vacío o no se ha guardado correctamente"
                "Ejecuta el script ETL antes de continuar"
            )

        df = pd.DataFrame(dataset)

        if "types" in df.columns:
            df["primary_type"] = df["types"].apply(
                lambda x: x[0] if isinstance(x, list) and len(x) > 0 else None
            )
            df["secondary_type"] = df["types"].apply(
                lambda x: x[1] if isinstance(x, list) and len(x) > 1 else None
            )

        return df

    # ESTADISTICAS DESCRIPTIVAS BASICAS
    def average_stats_by_type(self) -> list[TypeAverageStats]:
        """Calcula el promedio de las metricas agrupado por tipo usando groupby
        y explode

        Usamos explode para permitir el uso de Pokemon con tipo dual.

        Returns:
            Lista de Type AverageStats ordenada alfabéticamente"""

        df = self._load_dataframe()

        primary = df.copy()
        primary["type_name"] = primary["primary_type"]

        secondary = df.copy()
        secondary["type_name"] = secondary["secondary_type"]

        df_types = pd.concat([primary, secondary], ignore_index=True)
        df_types = df_types[df_types["type_name"].notna()]

        grouped = (
            df_types.groupby("type_name")[["hp", "attack", "defense", "speed"]]
            .mean()
            .round(2)
        )

        sample_sizes = df_types.groupby("type_name").size().rename("sample_size")
        grouped = grouped.join(sample_sizes).reset_index()

        return [
            TypeAverageStats(
                type_name=row["type_name"],
                sample_size=int(row["sample_size"]),
                avg_hp=row["hp"],
                avg_attack=row["attack"],
                avg_defense=row["defense"],
                avg_speed=row["speed"],
            )
            for _, row in grouped.sort_values("type_name").iterrows()
        ]

    def top_n(self, metric: str = "attack", n: int = 10) -> list[TopPokemonEntry]:
        """Devuelve el Top-N de Pokemons ordenados de mayor a menor según la métrica,
        para ello usamos nlargest

        Args:
            metric: la columna con la estadística
            n: la cantidad de resultados a devolver

        Returns:
            Lista de TopPokemonEntry ordenada de mayor a menor

        Raises:
            ValueError si la métrica no es válida"""

        if metric not in VALID_METRICS:
            raise ValueError(
                f"Métrica '{metric}' no válida. Usa una de {', '.join(VALID_METRICS)}"
            )

        if n <= 0:
            raise ValueError("El parámetro 'n' debe ser un entero positivo")

        df = self._load_dataframe()

        top = df.nlargest(n, metric)

        return [
            TopPokemonEntry(
                id=int(row["id"]),
                name=row["name"],
                types=row["types"],
                value=int(row[metric]),
                metric=metric,
            )
            for _, row in top.iterrows()
        ]

    # DETECCION DE ANOMALIAS
    def detect_anomalies(
        self, stdev_threshold: float = 2.0, percentile_threshold: float = 0.05
    ) -> list[AnomalyEntry]:
        """Detecta Pokemon anómalos combinando dos métodos:

        1. Desviación estándar (método principal): un Pokemon es anómalo si
           su stat_total se aleja más de `stddev_threshold` desviaciones
           estándar del promedio de SU tipo principal.

        2. Percentil (método de apoyo): un Pokemon es anómalo si su
           stat_total está en el top o bottom `percentile_threshold` del
           dataset completo (ej. 0.05 = 5% más alto o más bajo).

        Un mismo Pokemon puede aparecer marcado por ambos métodos; en ese
        caso se reporta solo una vez, priorizando el método de desviación
        estándar en la justificación.

        Args:
            stddev_threshold: el umbral mínimo de desviaciones estándares
            para considerar anómalo a un Pokemon = 2.0
            percentile_threshold: el umbral mínimo de corte del percentil = 0.05
            == 5%

        Returns:
            Lista AnomalyEntry ordenada de forma descendente
        """

        df = self._load_dataframe()

        # Iniciamos calculando el stat_total como suma vectorizada
        df["stat_total"] = df[["hp", "attack", "defense", "speed"]].sum(axis=1)  # fila

        anomalies: dict[int, AnomalyEntry] = {}

        # Iniciamos con la desviación estándar, usando groupby y agg
        type_stats = (
            df.groupby("primary_type")["stat_total"]
            .agg(["mean", "std"])
            .rename(columns={"mean": "type_mean", "std": "type_std"})
        )

        df_merged = df.merge(type_stats, on="primary_type", how="left")

        # Evitamos diviosnes por 0 si todos los Pokemon tiene el mismo stat total
        df_merged["deviation"] = (
            df_merged["stat_total"] - df_merged["type_mean"]
        ) / df_merged["type_std"]

        df_merged["deviation"] = df_merged["deviation"].where(
            df_merged["type_std"] > 0, 0.0
        )

        stddev_anomalies = df_merged[df_merged["deviation"].abs() >= stdev_threshold]

        for _, row in stddev_anomalies.iterrows():
            direction = "por encima" if row["deviation"] > 0 else "por debajo"
            deviation = round(float(row["deviation"]), 2)

            anomalies[int(row["id"])] = AnomalyEntry(
                id=int(row["id"]),
                name=row["name"],
                types=row["types"],
                stat_total=int(row["stat_total"]),
                type_average=round(float(row["type_mean"]), 2),
                deviation=deviation,
                method="stddev",
                reason=(
                    f"Stat total {int(row['stat_total'])} está {abs(deviation)} "
                    f"desviaciones estándar {direction} del promedio del tipo"
                    f"'{row['primary_type']}' ({round(float(row['type_mean']), 2)})."
                ),
            )

        # Seguimos con el percentil global (añadimos solo aquellos que el
        # método desviación estandar no se calculó)
        lower_cutoff = df["stat_total"].quantile(percentile_threshold)
        upper_cutoff = df["stat_total"].quantile(1 - percentile_threshold)

        percentile_anomalies = df[
            (df["stat_total"] <= lower_cutoff) | (df["stat_total"] >= upper_cutoff)
        ]

        global_mean = round(float(df["stat_total"].mean()), 2)

        for _, row in percentile_anomalies.iterrows():
            if int(row["id"]) in anomalies:
                continue

            total = int(row["stat_total"])
            percentile_label = (
                f"interior al {int(percentile_threshold * 100)}%"
                if total <= lower_cutoff
                else f"superior al {int((1 - percentile_threshold) * 100)}%"
            )

            anomalies[int(row["id"])] = AnomalyEntry(
                id=int(row["id"]),
                name=row["name"],
                types=row["types"],
                stat_total=total,
                type_average=global_mean,
                deviation=0.0,
                method="percentile",
                reason=(
                    f"Stat total {total} se encuentra en el percentil"
                    f"{percentile_label} de todo el dataset."
                ),
            )

        return sorted(anomalies.values(), key=lambda a: abs(a.deviation), reverse=True)
