from __future__ import annotations

import argparse
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
    os.system("cls" if os.name == "nt" else "clear")


def pausar() -> None:
    input("\n↩️ Presiona ENTER para volver al panel del control...")


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

            if len(data) > 2:
                _submenu_resultados(data)
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


def _submenu_resultados(data: list) -> None:

    total = len(data)

    while True:
        print(f"\n📦 Total de resultados disponibles: {total}")
        print("-" * 60)
        print("[1] Ver más resultados (indicar cantidad):")
        print("[2] Ver TODOS los resultados:")
        print("[3] Buscar un resultado por nombre específico:")
        print("[0] Volver")
        print("-" * 60)

        opcion = input("🔎 Qué quieres hacer con los resultados").strip()

        if opcion == "1":
            n_raw = input(f"¿Cuántods quieres ver? (1-{total}):").strip()
            if not n_raw.isdigit():
                print("⚠️ Ingresa un número válido")
                continue

            n = min(int(n_raw), total)
            print(f"\n📋 Mostrando {n} de {total} resultados:\n")
            print(json.dumps(data[:n], indent=2, ensure_ascii=False))

        elif opcion == "2":
            print(f"\n📋 Mostrando los {total} resultados:\n")
            print(json.dumps(data, indent=2, ensure_ascii=False))

        elif opcion == "3":
            termino = input("🔎 Nombre a buscar:").strip().lower()
            if not termino:
                print("⚠️ El término no puede estar vacío")
                continue

            coincidencias = [
                item
                for item in data
                if termino in str(item.get(next(iter(item)), "")).lower()
            ]
            if not coincidencias:
                print(f"❌ No se encontraron resultados con '{termino}'")

            else:
                print(f"\n✅ {len(coincidencias)} resultado(s) encontrado(s):\n")
                print(json.dumps(coincidencias, indent=2, ensure_ascii=False))

        elif opcion == "0":
            break
        else:
            print("⚠️ Opción inválida")


def cmd_pokemon(args: argparse.Namespace) -> None:
    manejar_diagnostico(api_get_pokemon, args.identifier)


def cmd_evolution(args: argparse.Namespace) -> None:
    manejar_diagnostico(api_get_evolution, args.identifier)


def cmd_effectiveness(args: argparse.Namespace) -> None:
    manejar_diagnostico(api_get_combat_effecteviness, args.identifier)


def cmd_filter(args: argparse.Namespace) -> None:
    manejar_diagnostico(
        api_get_filtered,
        tipo=args.type,
        gen=args.gen,
        hp=args.hp,
        attack=args.attack,
        defense=args.defense,
        speed=args.speed,
        base_exp=args.base_exp,
    )


def cmd_team_create(args: argparse.Namespace) -> None:
    manejar_diagnostico(api_create_team, args.name, args.ids)


def cmd_team_list(args: argparse.Namespace) -> None:
    manejar_diagnostico(api_list_teams)


def cmd_team_get(args: argparse.Namespace) -> None:
    manejar_diagnostico(api_get_team, args.team_id)


def cmd_team_delete(args: argparse.Namespace) -> None:
    manejar_diagnostico(api_delete_team, args.team_id)


def cmd_average(args: argparse.Namespace) -> None:
    manejar_diagnostico(api_get_average_by_type)


def cmd_top(args: argparse.Namespace) -> None:
    manejar_diagnostico(api_get_top, metric=args.metric, n=args.n)


def cmd_anomalies(args: argparse.Namespace) -> None:
    manejar_diagnostico(api_get_anomalies)


def cmd_prediction(args: argparse.Namespace) -> None:
    manejar_diagnostico(
        api_get_prediction,
        args.primary_type,
        args.secondary_type,
    )


def cmd_simulate(args: argparse.Namespace) -> None:
    manejar_diagnostico(
        api_get_simulation,
        args.n,
        args.type,
        args.gen,
        args.seed,
    )


def cmd_export_filter(args: argparse.Namespace) -> None:
    try:
        resultados = api_get_filtered(
            tipo=args.type,
            gen=args.gen,
            hp=0,
            attack=0,
            defense=0,
            speed=0,
            base_exp=0,
        )
        ruta = export_filtered_pokemons_csv(resultados)
        print(f"\n✅ CSV generado en: {ruta}")
    except Exception as e:
        print(f"\n❌ Error al exportar: {e}")


def cmd_export_top(args: argparse.Namespace) -> None:
    try:
        resultados = api_get_top(metric=args.metric, n=args.n)
        ruta = export_top_n_csv(resultados)
        print(f"\n✅ CSV generado en: {ruta}")
    except Exception as e:
        print(f"\n❌ Error al exportar: {e}")


def cmd_chart_pokemon(args: argparse.Namespace) -> None:
    try:
        pokemon = api_get_pokemon(args.identifier)
        print_pokemon_stats_chart(pokemon)
    except Exception as e:
        print(f"\n❌ Error al graficar: {e}")


def cmd_chart_type(args: argparse.Namespace) -> None:
    try:
        type_stats = api_get_average_by_type()
        print_type_average_chart(type_stats, metric=args.metric)
    except Exception as e:
        print(f"\n❌ Error al graficar: {e}")


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
    secondary_type_raw = input(
        "🔹 Tipo elemental secundario OPCIONAL (ej. water, grass, fire):"
    ).strip()

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
    pokemon_type = input(
        ("🔹 Tipo elemental primario (ej. water, grass, fire):")
    ).strip()
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

    acciones = {
        "1": menu_detalle_pokemon,
        "2": menu_arbol_evolutivo,
        "3": menu_filtro_analitico,
        "4": menu_efectividad_combate,
        "5": menu_crear_equipo,
        "6": menu_ver_equipo,
        "7": menu_ver_equipo,
        "8": menu_eliminar_equipo,
        "9": menu_promedio_por_tipo,
        "10": menu_top_n,
        "11": menu_anomalias,
        "12": menu_exportar_filtro_csv,
        "13": menu_exportar_top_csv,
        "14": menu_grafico_pokemon_individual,
        "15": menu_grafico_promedio_tipo,
        "16": menu_predicciones,
        "17": menu_simulaciones,
    }
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

        if opcion == "0":
            limpiar_pantalla()
            sys.exit(0)

        elif opcion in acciones:
            acciones[opcion]()
            pausar()

        else:
            print("\n⚠️ Selección inválida.")
            time.sleep(1)


def contruir_parser() -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser(
        prog="cli",
        description="🧪 Laboratorio Pokédex — audita la API directamente desde la terminal.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
        ejemplos de uso:
            python cli.py pokemon pikachu
            python cli.py evolution charmander
            python cli.py effectiveness charizard
            python cli.py filter --type fire --gen 1 --attack 60
            python cli.py team create "Equipo A" 1 4 7
            python cli.py team list
            python cli.py team get abc-123
            python cli.py team delete abc-123
            python cli.py analitics average
            python cli.py analytics top --metric attack --n 5
            python cli.py analytics anomalies
            python cli.py analytics prediction fire --secondary flying
            python cli.py analytics simulate --type water --gen 2 --n 20 --seed 42
            python cli.py export filter --type grass
            python cli.py export top --metric hp --n 10
            python cli.py chart pokemon pikachu
            python cli.py chart type --metric avg_speed""",
    )

    sub = parser.add_subparsers(dest="comando", metavar="comando")

    p_pokemon = sub.add_parser("pokemon", help="Detalle de un Pokemon por nombre o ID")
    p_pokemon.add_argument("identifier", help="Nombre o ID (ej. pikachu, 25)")
    p_pokemon.set_defaults(func=cmd_pokemon)

    p_evo = sub.add_parser("evolution", help="Árbol evolutivo de un Pokemon")
    p_evo.add_argument("identifier", help="Nombre o ID")
    p_evo.set_defaults(func=cmd_evolution)

    p_eff = sub.add_parser("effectiveness", help="Efectividad de combate de un Pokemon")
    p_eff.add_argument("identifier", help="Nombre o ID")
    p_eff.set_defaults(func=cmd_effectiveness)

    p_filter = sub.add_parser(
        "filter", help="Filtrar Pokemon por tipo, generación y stats"
    )
    p_filter.add_argument(
        "--type", dest="type", default=None, help="Tipo elemental (ej. fire)"
    )
    p_filter.add_argument(
        "--gen", dest="gen", type=int, default=None, help="Generación (1-9)"
    )
    p_filter.add_argument("--hp", dest="hp", type=int, default=0, help="HP mínimo")
    p_filter.add_argument(
        "--attack", dest="attack", type=int, default=0, help="Ataque mínimo"
    )
    p_filter.add_argument(
        "--defense", dest="defense", type=int, default=0, help="Defensa mínima"
    )
    p_filter.add_argument(
        "--speed", dest="speed", type=int, default=0, help="Velocidad mínima"
    )
    p_filter.add_argument(
        "--base-exp",
        dest="base_exp",
        type=int,
        default=0,
        help="Experiencia base mínima",
    )
    p_filter.set_defaults(func=cmd_filter)

    p_team = sub.add_parser("team", help="Gestión de equipos Pokemon")
    team_sub = p_team.add_subparsers(dest="team_cmd", metavar="acción")

    t_create = team_sub.add_parser("create", help="Crear un equipo")
    t_create.add_argument("name", help="Nombre del equipo")
    t_create.add_argument(
        "ids", type=int, nargs="+", metavar="ID", help="IDs de Pokemon (máx 6)"
    )
    t_create.set_defaults(func=cmd_team_create)

    t_list = team_sub.add_parser("list", help="Listar todos los equipos")
    t_list.set_defaults(func=cmd_team_list)

    t_get = team_sub.add_parser("get", help="Ver detalle de un equipo")
    t_get.add_argument("team_id", help="ID del equipo")
    t_get.set_defaults(func=cmd_team_get)

    t_delete = team_sub.add_parser("delete", help="Eliminar un equipo")
    t_delete.add_argument("team_id", help="ID del equipo")
    t_delete.set_defaults(func=cmd_team_delete)

    p_analytics = sub.add_parser("analytics", help="Análisis estadístico del dataset")
    analytics_sub = p_analytics.add_subparsers(dest="analytics_cmd", metavar="análisis")

    analytics_sub.add_parser(
        "average", help="Promedios de stats por tipo elemental"
    ).set_defaults(func=cmd_average)

    a_top = analytics_sub.add_parser("top", help="Top-N Pokemon por métrica")
    a_top.add_argument(
        "--metric",
        default="attack",
        choices=["hp", "attack", "defense", "speed", "base_exp"],
        help="Estadística a ordenar (default: attack)",
    )
    a_top.add_argument(
        "--n", type=int, default=10, help="Cantidad de resultados (default: 10)"
    )
    a_top.set_defaults(func=cmd_top)

    analytics_sub.add_parser(
        "anomalies", help="Detectar Pokemon con stats anómalas"
    ).set_defaults(func=cmd_anomalies)

    a_pred = analytics_sub.add_parser("prediction", help="Predecir stats para un tipo")
    a_pred.add_argument("primary_type", help="Tipo elemental primario (ej. fire)")
    a_pred.add_argument(
        "--secondary",
        dest="secondary_type",
        default=None,
        help="Tipo secundario opcional (ej. flying)",
    )
    a_pred.set_defaults(func=cmd_prediction)

    a_sim = analytics_sub.add_parser("simulate", help="Generar Pokemon sintéticos")
    a_sim.add_argument(
        "--n", type=int, default=10, help="Cantidad a generar (default: 10)"
    )
    a_sim.add_argument(
        "--type", dest="type", default="normal", help="Tipo elemental (default: normal)"
    )
    a_sim.add_argument(
        "--gen", dest="gen", type=int, default=1, help="Generación (default: 1)"
    )
    a_sim.add_argument(
        "--seed", dest="seed", type=int, default=None, help="Semilla aleatoria opcional"
    )
    a_sim.set_defaults(func=cmd_simulate)

    p_export = sub.add_parser("export", help="Exportar resultados a CSV")
    export_sub = p_export.add_subparsers(dest="export_cmd", metavar="destino")

    e_filter = export_sub.add_parser(
        "filter", help="Exportar resultado de filtro a CSV"
    )
    e_filter.add_argument("--type", dest="type", default=None, help="Tipo elemental")
    e_filter.add_argument(
        "--gen", dest="gen", type=int, default=None, help="Generación"
    )
    e_filter.set_defaults(func=cmd_export_filter)

    e_top = export_sub.add_parser("top", help="Exportar Top-N a CSV")
    e_top.add_argument(
        "--metric",
        default="attack",
        choices=["hp", "attack", "defense", "speed", "base_exp"],
    )
    e_top.add_argument("--n", type=int, default=10)
    e_top.set_defaults(func=cmd_export_top)

    p_chart = sub.add_parser("chart", help="Gráficos ASCII en consola")
    chart_sub = p_chart.add_subparsers(dest="chart_cmd", metavar="gráfico")

    c_poke = chart_sub.add_parser("pokemon", help="Stats de un Pokemon en barras ASCII")
    c_poke.add_argument("identifier", help="Nombre o ID")
    c_poke.set_defaults(func=cmd_chart_pokemon)

    c_type = chart_sub.add_parser("type", help="Promedio por tipo en barras ASCII")
    c_type.add_argument(
        "--metric",
        default="avg_attack",
        choices=["avg_hp", "avg_attack", "avg_defense", "avg_speed"],
        help="Métrica a graficar (default: avg_attack)",
    )
    c_type.set_defaults(func=cmd_chart_type)

    return parser


if __name__ == "__main__":
    parser = contruir_parser()
    args = parser.parse_args()

    if not args.comando:
        engine = AlertEngine(
            dataset_loader=load_dataset,
            anomalies_fetcher=api_get_anomalies,
            teams_fetcher=api_list_teams,
        )

        engine.run_startup_alerts()
        pausar()
        laboratorio_principal()

    elif not hasattr(args, "func"):
        parser.parse_args([args.comando, "--help"])

    else:
        args.func(args)
