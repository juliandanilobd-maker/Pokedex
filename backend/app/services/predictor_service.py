""" "Este módulo contiene la predicción de tendencias estadísticas

Se entrega un tipo elemental (simple o dual) y de manera opcional
la generación, a partir de estos datos, se calcula la media de las stats
a lo largo de la generación para ese tipo y devuelve una predicción de las
stas esperadas para un Pokemon de ese tipo y generación

Utilizamos la media móvil simple usando como periodo las generaciones disponibles
máximo 3

No realiza llamadas a la PokeAPI, trabaja con el dataset local"""

# ESTE MODULO EXCEDE EL MAXIMO DE 50 DEBIDO A LA LOGICA DE PREDICCION
# DE ESTADISTICAS, REQUIERE CAPTURA DE TIPOS, Y LA RESPUESTA QUE RETORNA
# CONTIENE VARIOS PARAMETROS

from __future__ import annotations

import pandas as pd

from backend.app.models.pokemon_models import PredictionResult

STATS = ("hp", "attack", "defense", "speed")
MAX_WINDOW = 3


class PredictorService:
    """Clase que guarda la lógica de predicción de stats"""

    def __init__(self, dataset_loader) -> None:
        self._dataset_loader = dataset_loader

    def _load_dataframe(self) -> pd.DataFrame:
        dataset = self._dataset_loader()

        if not dataset:
            raise ValueError(
                "El dataset local está vacío o no se ha generado"
                "Ejecuta el script ETL antes de continuar"
            )

        return pd.DataFrame(dataset)

    def predict_stats(
        self,
        primary_type: str,
        secondary_type: str | None = None,
    ):
        """Predice las stats

        1. Filtra el dataset por tipo usando explode en caso de Pokemon dual
        2. Calcula el promedio de stats por generación y aplica una media movil
        simple

        Args:
            primary_type: tipo principal
            secondaty_type: tipo secundario, opcional

        Returns:
            PredictionResult con stats predichas y los datos del cálculo

        Raises:
            ValueError si no hay suficientes datos para calcular"""

        df = self._load_dataframe()

        primary_type = primary_type.lower().strip()

        df_exploded = df.explode("types")
        df_tipo = df_exploded[df_exploded["types"] == primary_type].copy()

        if df_tipo.empty:
            raise ValueError(
                f"No se encontráron Pokemon de tipo '{primary_type}' en el dataset "
                "Verifica que el tipo sea válido (ej. fire, water)"
            )

        if secondary_type:
            secondary_type = secondary_type.lower().strip()
            ids_con_secundario = df[
                df["types"].apply(
                    lambda t: secondary_type in t if isinstance(t, list) else False
                )
            ]["id"]

            df_tipo = df_tipo[df_tipo["id"].isin(ids_con_secundario)]

            pt = primary_type
            st = secondary_type

            if df_tipo.empty:
                raise ValueError(
                    f"No se encontráron Pokemon de tipo '{pt}'/'{st}' en el dataset "
                    "Prueba con un solo tipo u otra combinación"
                )

        sample_description = f"tipo '{primary_type}'"
        if secondary_type:
            sample_description += f"/{secondary_type}"

        gen_stats = (
            df_tipo.groupby("generation")[list(STATS)].mean().round(2).sort_index()
        )

        if len(gen_stats) < 2:
            raise ValueError(
                f"Solo hay {len(gen_stats)} generaciones para {sample_description} "
                "Se necesitan al menos 2 generaciones para calcula la media móvil"
            )

        window = min(MAX_WINDOW, len(gen_stats))
        sma = gen_stats.rolling(window=window).mean().dropna()

        predicted = sma.iloc[-1].round(2)

        group_avg = df_tipo[list(STATS)].mean().round(2)
        generations_used = sorted(gen_stats.index.tolist())

        return PredictionResult(
            primary_type=primary_type,
            secondary_type=secondary_type,
            predicted_hp=float(predicted["hp"]),
            predicted_attack=float(predicted["attack"]),
            predicted_defense=float(predicted["defense"]),
            predicted_speed=float(predicted["speed"]),
            sample_size=len(df_tipo["id"].unique()),
            generations_used=generations_used,
            window_size=window,
            group_avg_hp=float(group_avg["hp"]),
            group_avg_attack=float(group_avg["attack"]),
            group_avg_defense=float(group_avg["defense"]),
            group_avg_speed=float(group_avg["speed"]),
            description=(
                f"Predicción basada en media móvil simple (ventana={window}) "
                f"sobre {len(generations_used)} generaciones históricas "
                f"para {sample_description}. "
                f"Muestra: {len(df_tipo['id'].unique())} Pokémon únicos."
            ),
        )
