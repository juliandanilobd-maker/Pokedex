"""En este módulo se encuentra el encargado de enviar alertas automáticas

Se ejecuta al iniciar el CLI, antes de mostrar el menú, usando condiciones de los
datos disponibles

No requiere flujo de datos constante, evalua la info obtenida del dataset
cada vez que arranca el programa"""

# ESTE MODULO NO CUMPLE CON 50 LINEAS MAXIMO PORQUE POR NORMAS DE LONGITUD
# DE LINEA NO SE PUEDEN EXCEDER LOS 88 CARACTERES, ENTONCES SE AUMENTARON LINEAS
from __future__ import annotations

import random
from datetime import date


class AlertEngine:
    """Encapsula las distintas reglas de alerta evaluadas al iniciar el CLI."""

    def __init__(self, dataset_loader, anomalies_fetcher, teams_fetcher) -> None:
        """
        Args:
            dataset_loader: función que devuelve el dataset completo (ej. load_dataset).
            anomalies_fetcher: función sin argumentos que devuelve la lista de
                                anomalías (ej. api_get_anomalies del client_cli).
            teams_fetcher: función sin argumentos que devuelve la lista de
                            equipos guardados (ej. api_list_teams del client_cli).
        """
        self._dataset_loader = dataset_loader
        self._anomalies_fetcher = anomalies_fetcher
        self._teams_fetcher = teams_fetcher

    # Alerta 1: Pokemon del día
    def _pokemon_del_dia(self) -> dict | None:
        """Selecciona un Pokemon "del día" de forma determinística según la
        fecha actual, para que sea el mismo durante todo el día."""

        dataset = self._dataset_loader()

        if not dataset:
            return None

        # Usamos la fecha como semilla para que el resultado sea estable
        # durante el mismo día, pero cambie automáticamente al día siguiente
        seed = date.today().isoformat()
        rng = random.Random(seed)

        return rng.choice(dataset)

    # Alerta 2: anomalías detectadas en el dataset
    def _resumen_anomalias(self) -> int:
        """Devuelve cuántas anomalías hay actualmente en el dataset.
        Si falla la consulta (ej. backend apagado), devuelve 0 en lugar de
        tumbar el arranque del CLI (cumple NF2)."""

        try:
            anomalies = self._anomalies_fetcher()
            return len(anomalies)

        except Exception:
            return 0

    # Alerta 3: equipos con baja cobertura de tipos
    def _equipos_con_poca_cobertura(self, min_types: int = 3) -> list[str]:
        """Detecta equipos guardados cuya cobertura de tipos es baja
        (menos de min_types tipos distintos), lo cual es una debilidad
        estratégica relevante para el usuario."""

        try:
            teams = self._teams_fetcher()

        except Exception:
            return []

        nombres_debiles = []

        for team in teams:
            coverage = team.get("stats", {}).get("type_coverage", [])

            if len(coverage) < min_types:
                nombres_debiles.append(team.get("name", "equipo sin nombre"))

        return nombres_debiles

    # Orquestador: evalúa todas las reglas y emite las notificaciones
    def run_startup_alerts(self) -> None:
        """Evalúa todas las condiciones de alerta y las imprime en consola.
        Pensado para llamarse una vez, justo antes del menú principal."""

        print("=" * 60)
        print("🔔 ALERTAS AUTOMÁTICAS DEL DÍA")
        print("=" * 60)

        alguna_alerta = False

        pokemon = self._pokemon_del_dia()

        if pokemon:
            alguna_alerta = True
            print(
                f"🌟 Pokemon del día: {pokemon['name'].capitalize()} "
                f"(#{pokemon['id']}) — ¡no te olvides de revisarlo!"
            )

        total_anomalias = self._resumen_anomalias()

        if total_anomalias > 0:
            alguna_alerta = True
            print(
                f"⚠️ Se detectaron {total_anomalias} Pokemon con stats anómalas "
                "en el dataset. Revisa la opción de análisis de anomalías."
            )

        equipos_debiles = self._equipos_con_poca_cobertura()

        if equipos_debiles:
            alguna_alerta = True
            lista = ", ".join(equipos_debiles)
            print(
                f"🛡️ Estos equipos tienen poca variedad de tipos y son "
                f"vulnerables estratégicamente: {lista}."
            )

        if not alguna_alerta:
            print("✅ No hay alertas relevantes por el momento.")

        print("=" * 60)
