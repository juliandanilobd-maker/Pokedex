from __future__ import annotations

import json
import os
import sys
import time

import requests

from backend.app.services.alerts_service import AlertEngine
from backend.app.services.reporter_service import (
    export_filtered_pokemons_csv,
    export_top_n_csv,
    print_pokemon_stats_chart,
    print_type_average_chart,
)
from client_cli import (
    api_create_team,
    api_delete_team,
    api_get_anomalies,
    api_get_average_by_type,
    api_get_combat_effecteviness,
    api_get_evolution,
    api_get_filtered,
    api_get_pokemon,
    api_get_prediction,
    api_get_simulation,
    api_get_team,
    api_get_top,
    api_list_teams,
    load_dataset,
)


def limpiar_pantalla() -> None:
    os.system("cls" if os.name == "int" else "clear")


def pausar() -> None:
    input("\n↩️ Presiona ENTER para vovler al panel del control...")


def manejar_diagnostico(funcion_api, *args, **kwargs):
    print("-" * 60)
    print("📡 EMITIENDO LA PETICION A TRAVES DE CLIENT_CLI...")
    print("-" * 60)

    try:
        data = funcion_api(*args, **kwargs)

        print("\n✅ [HTTP 200] ESTRUCTURA DE DATOS CAPTURADA EXITOSAMENTE:\n")

        if isinstance(data, list):
            print(f"🗂️ Estructura: Lista (Contiene {len(data)} elementos)")
            print("Muesta de los primeros 2 elementos:")
            print(json.dumps(data[:2], indent=2, ensure_ascii=False))

        else:
            print(json.dumps(data, indent=2, ensure_ascii=False))

    except requests.exceptions.HTTPError as e:
        res = e.response

        if res is not None:
            print(
                f"\n❌ DETALLE DEL ERROR RETORNANDO POR FASTAPI (HTTP {res.status_code}):"
            )

            try:
                print(json.dumps(res.json(), indent=2, ensure_ascii=False))

            except Exception:
                print(res.text)

    except requests.exceptions.ConnectionError:
        print("\n🚨 ERROR: No se pudo contecta con el servidor local")
        print("💡 Consejo: Asegúrate de tener levantado uvicorn en el puerto 8000.")

    except Exception as e:
        print(f"\n⚠️ Anomalía inesperada en el laboratorio: {e}")


def menu_filtro_analitico() -> None:

    limpiar_pantalla()
    print("=============================================================")
    print("🎛️ MODULO DE PRUEBA: FILTRADO ACUMULATIVO OPTIMIZADO")
    print("=============================================================")
    tipo = input("🔹 Tipo elemental (ej. fire):").strip().lower()
    gen = input("🔹 Número de generación (1-9):").strip()
    hp = input("🔹 HP mínimo:").strip()
    attack = input("🔹 Ataque base mínimo:").strip()
    defense = input("🔹 Defensa base mínima:").strip()
    speed = input("🔹 Velocidad base mínima:").strip()
    base_exp = input("🔹 Experiencia base mínima:").strip()

    gen_val = int(gen) if gen else None
    hp_val = int(hp) if hp else 0
    attack_val = int(attack) if attack else 0
    defense_val = int(defense) if defense else 0
    speed_val = int(speed) if speed else 0
    base_exp_val = int(base_exp) if base_exp else 0

    manejar_diagnostico(
        api_get_filtered,
        tipo=tipo,
        gen=gen_val,
        hp=hp_val,
        attack=attack_val,
        defense=defense_val,
        speed=speed_val,
        base_exp=base_exp_val,
    )


def menu_detalle_pokemon() -> None:

    limpiar_pantalla()
    print("=============================================================")
    print("🔍 MODULO DE PRUEBA: DETALLE INDIVIDUAL DE POKEMON")
    print("=============================================================")
    identifier = input("📝 Ingresa Nombre o ID (ej. pikachu):").strip().lower()

    if identifier:
        manejar_diagnostico(api_get_pokemon, identifier)


def menu_arbol_evolutivo() -> None:
    limpiar_pantalla()
    print("=============================================================")
    print("🧬 MODULO DE PRUEBA: CADENAS DE EVOLUCION")
    print("=============================================================")
    identifier = input("📝 Ingresa Nombre o ID (ej. pikachu):").strip().lower()

    if identifier:
        manejar_diagnostico(api_get_evolution, identifier)


def menu_efectividad_combate() -> None:
    limpiar_pantalla()
    print("=============================================================")
    print("⚔️ MODULO DE PRUEBA: EFECTIVIDAD EN COMBATE")
    print("=============================================================")
    identifier = input("📝 Ingresa Nombre o ID (ej. pikachu):").strip().lower()

    if identifier:
        manejar_diagnostico(api_get_combat_effecteviness, identifier)


def menu_crear_equipo() -> None:

    limpiar_pantalla()
    print("=============================================================")
    print("🛡️ MODULO DE PRUEBA: CONSTRUCTOR DE EQUIPOS - CREAR EQUIPO")
    print("=============================================================")
    identifier = input("📝 Ingresa el nombre del equipo").strip()

    if not identifier:
        print("\n ⚠️ El nombre del equipo no puede estar vacío")
        return

    print(
        "Ingresa hasta 6 IDs de Pokemon separados por coma (ej: 1, 4, 6, 35, 76, 100)"
    )
    ids_raw = input(">> ").strip()
    pokemon_ids = None

    try:
        pokemon_ids = [int(x.strip()) for x in ids_raw.split(",") if x.strip()]

        if not pokemon_ids:
            print("\n ⚠️ Debes ingresar al menos un ID")
            return

    except ValueError:
        print("\n ⚠️ Los IDs deben ser números enteros separados por coma.")

    manejar_diagnostico(api_create_team, identifier, pokemon_ids)


def menu_listar_equipo() -> None:

    limpiar_pantalla()
    limpiar_pantalla()
    print("=============================================================")
    print("📋 MODULO DE PRUEBA: CONSTRUCTOR DE EQUIPOS - LISTAR EQUIPOS")
    print("=============================================================")
    manejar_diagnostico(api_list_teams)


def menu_ver_equipo() -> None:

    limpiar_pantalla()
    limpiar_pantalla()
    print("=============================================================")
    print("🔍 MODULO DE PRUEBA: CONSTRUCTOR DE EQUIPOS - DETALLE DE EQUIPO")
    print("=============================================================")
    identifier = input("📝 Ingresa el ID del equipo").strip()

    if identifier:
        manejar_diagnostico(api_get_team, identifier)


def menu_eliminar_equipo() -> None:

    limpiar_pantalla()
    print("=============================================================")
    print("🗑️ MODULO DE PRUEBA: CONSTRUCTOR DE EQUIPOS - ELIMINAR EQUIPO")
    print("=============================================================")
    identifier = input("📝 Ingresa el nombre del equipo a eliminar").strip()

    if identifier:
        manejar_diagnostico(api_delete_team, identifier)


def menu_promedio_por_tipo() -> None:

    limpiar_pantalla()
    print("=============================================================")
    print("🧮 MODULO DE PRUEBA: ANALISIS DE METRICAS - PROMEDIO POR TIPO")
    print("=============================================================")
    manejar_diagnostico(api_get_average_by_type)


def menu_top_n() -> None:

    limpiar_pantalla()
    print("=============================================================")
    print(
        "🎖️ MODULO DE PRUEBA: ANALISIS DE METRICAS - MEJORES POKEMON SEGUN ESTADISTICAS"
    )
    print("=============================================================")
    metric = input(
        "🔹 Métrica (hp/attack/defense/speed/base_exp) Ingresa una estadística:"
    ).strip()
    metric = metric or "attack"

    n_raw = input("🔹 Cantidad (N) [10]:").strip()
    n = int(n_raw) if n_raw.isdigit() else 10

    manejar_diagnostico(api_get_top, metric=metric, n=n)


def menu_anomalias() -> None:

    limpiar_pantalla()
    print("=============================================================")
    print("🚨 MODULO DE PRUEBA: ANALYTICS - DETECCION DE ANOMALIAS")
    print("=============================================================")
    manejar_diagnostico(api_get_anomalies)


def menu_exportar_filtro_csv() -> None:

    limpiar_pantalla()
    print("=============================================================")
    print("💾 MODULO DE PRUEBA: EXPORTAR RESULTADO DE FILTROS A CSV")
    print("=============================================================")
    print("Define el filtro a exportar:")

    tipo = input("🔹 Tipo elementarl (ej. fire):").strip().lower()
    gen = input("🔹 Generación (1-9):").strip()

    gen_val = int(gen) if gen else None

    try:
        resultados = api_get_filtered(
            tipo=tipo or None,
            gen=gen_val,
            hp=0,
            attack=0,
            defense=0,
            speed=0,
            base_exp=0,
        )

        ruta = export_filtered_pokemons_csv(resultados)
        print(f"\n✅ CSV generado exitosamente en: {ruta}")

    except ValueError as e:
        print(f"\n ⚠️ {e}")

    except Exception as e:
        print(f"\n ❌ Error al exportar: {e}")


def menu_exportar_top_csv() -> None:

    limpiar_pantalla()
    print("=============================================================")
    print("💾 MODULO DE PRUEBA: EXPORTAR TOP-N A CSV")
    print("=============================================================")

    metric = input("🔹 Métrica (hp/attack/defense/speed/base_exp):").strip()
    metric = metric or "attack"  # fallback

    n_raw = input("🔹 Cantidad (N) [10]:").strip()
    n = int(n_raw) if n_raw.isdigit() else 10

    try:
        resultados = api_get_top(metric=metric, n=n)
        ruta = export_top_n_csv(resultados)

        print(f"\n ✅ CSV generado exitósamente en: {ruta}")

    except ValueError as e:
        print(f"\n ⚠️ {e}")

    except Exception as e:
        print(f"\n ❌ Error al exportar: {e}")


def menu_grafico_pokemon_individual() -> None:

    limpiar_pantalla()
    print("=============================================================")
    print("📊 MODULO DE PRUEBA: GRAFICO ASCII - STATS DE POKEMON")
    print("=============================================================")
    identifier = input("📝 Ingresa Nombre o ID (ej. pikachu):").strip().lower()

    if not identifier:
        return

    try:
        pokemon = api_get_pokemon(identifier)
        print_pokemon_stats_chart(pokemon)

    except Exception as e:
        print(f"\n ❌ Error al graficar: {e}")


def menu_grafico_promedio_tipo() -> None:

    limpiar_pantalla()
    print("=============================================================")
    print("📊 MODULO DE PRUEBA: GRAFICO ASCII - PROMEDIO POR TIPO")
    print("=============================================================")
    metric = input("🔹 Metrica (avg_hp/avg_attack/avg_defense/avg_speed):").strip()

    metric = metric or "attack"  # fallback

    try:
        type_stats = api_get_average_by_type()
        print_type_average_chart(type_stats, metric=metric)

    except ValueError as e:
        print(f"\n ⚠️ {e}")

    except Exception as e:
        print(f"\n ❌ Error al graficar: {e}")

def menu_predicciones() -> None:

    limpiar_pantalla()
    print("=============================================================")
    print("🔮 MODULO DE PRUEBA: PREDICCIONES - STATS POR TIPO Y GENERACION")
    print("=============================================================")
    primary_type = input("🔹 Tipo elemental primario (ej. water, grass, fire):").strip()
    secondary_type_raw = input("🔹 Tipo elemental secundario OPCIONAL (ej. water, grass, fire):").strip()

    secondary_type = secondary_type_raw if secondary_type_raw else None


    try:
        manejar_diagnostico(api_get_prediction, primary_type, secondary_type)

    except ValueError as e:
        print(f"\n ⚠️ {e}")

    except Exception as e:
        print(f"\n ❌ Error al predecir: {e}")

def menu_simulaciones() -> None:

    limpiar_pantalla()
    print("=============================================================")
    print("🎰 MODULO DE PRUEBA: SIMULACIONES - GENERA POKEMON ALEATORIO")
    print("=============================================================")
    n = int(input("🔹 Cantidad de Pokemon a generar (máximo 1000):").strip())
    pokemon_type = input(("🔹 Tipo elemental primario (ej. water, grass, fire):")).strip()
    generation = int(input("🔹 Generación a la que pertenecerán (1-9):").strip())
    seed_raw = input("🔹 Semilla aleatoría OPCIONAL (Enter para omitir):").strip()

    seed = int(seed_raw) if seed_raw else None

    try:
        manejar_diagnostico(api_get_simulation, n, pokemon_type, generation, seed)

    except ValueError as e:
        print(f"\n ⚠️ {e}")

    except Exception as e:
        print(f"\n ❌ Error al simular: {e}")

def laboratorio_principal() -> None:
    while True:
        limpiar_pantalla()
        print("=============================================================")
        print("🧪LABORATORIO: COMPONENTES ACOPLADOS")
        print("=============================================================")
        print("[1] Auditar Ficha de Pokemon Idividual ('/pokemon/{identifier})")
        print("[2] Auditar Arbol de Evolución ('/pokemon/{identifier}/evolution)")
        print("[3] Auditar Motor de Filtros Avanzados ('/filter)")
        print(
            "[4] Auditar Cálculo de Efectividad de Combate ('/pokemon/{identifier}/effectiveness')"
        )
        print("[5] Auditar la creación de equipos Pokemon ('/teams')")
        print("[6] Auditar el listado de equipos Pokemon ('/teams')")
        print("[7] Auditar el detalle de un equipo Pokemon ('/teams/{team_id}')")
        print("[8] Auditar la eliminación de un equipo Pokemon ('/teams/{team_id}')")
        print(
            "[9] Auditar los promedios de Stats por tipo ('/analytics/average/by/type')"
        )
        print(
            "[10] Auditar el cálculo de top-n de Pokemon por métrica ('/analytics/top')"
        )
        print(
            "[11] Auditar la detección de anomalías en el Dataset ('/analytics/anomalies')"
        )
        print("[12] Auditar el resultado de filtro a CSV")
        print("[13] Auditar el resultado de Top-N a CSV")
        print("[14] Auditar el gráfico de stats de un Pokemon (ASCII)")
        print("[15] Auditar el gráfico de promedio por tipos (ASCII)")
        print("[16] Auditar la predicción de stats de un Pokemon por tipo y generación")
        print("[17] Auditar la simulación de stats de un Pokemon aleatorio")

        print("-" * 60)
        print("[0] Salir del Laboratorio Analítico")
        print("=============================================================")

        opcion = input("🤖 Elige un bloque de prueba para ejecutar: ").strip()

        if opcion == "1":
            menu_detalle_pokemon()
            pausar()

        elif opcion == "2":
            menu_arbol_evolutivo()
            pausar()

        elif opcion == "3":
            menu_filtro_analitico()
            pausar()

        elif opcion == "4":
            menu_efectividad_combate()
            pausar()

        elif opcion == "5":
            menu_crear_equipo()
            pausar()

        elif opcion == "6":
            menu_listar_equipo()
            pausar()

        elif opcion == "7":
            menu_ver_equipo()
            pausar()

        elif opcion == "8":
            menu_eliminar_equipo()
            pausar()

        elif opcion == "9":
            menu_promedio_por_tipo()
            pausar()

        elif opcion == "10":
            menu_top_n()
            pausar()

        elif opcion == "11":
            menu_anomalias()
            pausar()

        elif opcion == "12":
            menu_exportar_filtro_csv()
            pausar()

        elif opcion == "13":
            menu_exportar_top_csv()
            pausar()

        elif opcion == "14":
            menu_grafico_pokemon_individual()
            pausar()

        elif opcion == "15":
            menu_grafico_promedio_tipo()
            pausar()

        elif opcion == "16":
            menu_predicciones()
            pausar()

        elif opcion == "17":
            menu_simulaciones()
            pausar()

        elif opcion == "0":
            limpiar_pantalla()
            sys.exit(0)

        else:
            print("\n⚠️ Selección inválida.")
            time.sleep(1)


if __name__ == "__main__":
    engine = AlertEngine(
        dataset_loader=load_dataset,
        anomalies_fetcher=api_get_anomalies,
        teams_fetcher=api_list_teams,
    )

    engine.run_startup_alerts()
    pausar()
    laboratorio_principal()
