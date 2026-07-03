# INTRODUCCION Y OBJETIVOS
A continuación se presenta el plan de testing para la Pokedex, aplicación web,
construida con FastAPI (backend) y Streamlit (Frontend) que permite consultar y filtrar cualquier tipo de Pokemon, visualizar sus características, estadísticas y descripciones.

## OBJETIVOS
- Garantizar que cada módulo funcione correctamente.
- Verificar que los módulos interactuan entre sí sin errores.
- Verificar que el sistema responde correctamente.

# ESTRATEGIA GENERAL
Se opta por tests en 3 niveles:
1. Tests unitarios.
2. Tests de integración.
3. Tests funcionales e2e.

| NIVEL | ¿QUE VERIFICA? | HERRAMIENTAS | MINIMO REQUERIDO |
| :---: | :------------: | :----------: | :---------------:|
| Unitario | Comportamiento aislado de una función | pytest + AsyncMock | 1 fichero por módulo principal
| Integración | Integración correcta entre módulos | pytest + TestClient | 3 tests documentados |
| Funcional | Flujos completos con API real | pytest + TestClient | Cobertura de happy path y error path |
| Rendimiento | 10k registros en menos de 3 segundos | pytest + time | 1 módulo
| Casos límite | Captura de errores por datos incorrectos ingresados | pytest | 5 casos límites cubiertos, integradas dentro de tests unitarios/integración/funcionales
|Tests de error controlado | Lanza excepciones correctas | pytest + mock | 4 tests por error, integradas dentro de tests unitarios/integración/funcionales

# COBERTURA OBJETIVO
La cobertura mínima exigida por los requisitos es de un 80%, sin embargo por rigurosidad y aumento de la calidad, se implementa un mínimo del 90%

```Required test coverage of 90% reached.```

![COBERTURA MINIMA](/docs/documentacion_testing/images/image.png)

# TIPOS DE TESTS
Todos los tests superan las 50 lineas de codigo, debido a la amplitud de los servicios y logica interna, los varios errores capturados y excepciones
## TESTS UNITARIOS
Los tests unitarios verifican el comportamiento de cada función y método de forma aislada, sin depender de la red, la base de datos ni otros módulos. Se usan AsyncMock para reemplazar dependencias asíncronas y monkeypatch para interceptar llamadas a httpx.AsyncClient.

test_alerts_service.py
test_analyzer_service.py
test_battle_intelligence.py
test_cache_manager.py
test_dataset.py
test_evolution_parser.py
test_evolution_service.py
test_filter_service.py
test_pokeapi_client.py
test_pokemon_parser.py
test_pokemon_service.py
test_predictor_service.py
test_reporter_service.py
test_server.py
test_simulator_service.py
test_team_service.py

## TESTS DE INTEGRACION

test_filter_integration.py
test_pokemon_endpoints.py

Dentro de los ficheros se encuentran 32 tests que cubre happy path y error path, excepciones, y manejos de casos límite

## TESTS FUNCIONALES

test_infraestructure.py
test_pokedex_e2e.py

Dentro de los ficheros se encuentran 14 tests que cubre happy path y error path, excepciones, y manejos de casos límite

## TESTS DE RENDIMIENTO
test_simulator_service.py/test_generate_n_mayor_10000_less_3_sec() -> comprueba que se genera un csv con 10000 Pokemon en menos de 3 segundos

Como parte de tests de rendimiento se comprueba que el cache responde más rápido que una llamada a la API

## TESTS DE CASO LIMITE

test_alert_service.py/def test_pokemon_of_day_empty_dataset_returns_none()

test_alert_service.py/def test_anomalies_return_zero_with_empty_list()

test_analyzer_service.py/def test_load_dataset_empty_raises_value_error()

test_analyzer_service.py/def test_avg_stats_by_type_empty_list_return_error()

test_evolution_parser.py/def test_parse_evolution_empty_node()

Se detallan 5 tests que manejan el comportamiento del servicio ante entradas vacías, sin embargo, en cada módulo se encuentran varios tests más acerca de caso límite.

## TEST DE ERROR CONTROLADO

test_pokedex_e2e.py/def test_e2e_effectiveness_not_found()

test_pokedex_e2e.py/def test_get_evolution_chain_e2e_not_found()

test_filter_integration.py/def test_integration_filter_not_found()

test_filter_integration.py/def test_integration_filter_generic_exception()

Se detallan 4 tests que cubren las excepciones de captura de errores (bloques try except), sin embargo, en cada fichero tests se encuentran más tests acerca de errores controlados.

# HERRAMIENTAS

| HERRAMIENTA | USO | CONFIGURACION |
| :---------: | :-: | :------------:|
|pytest|Framework principal de testing|pyproject.toml|
|asyncio|Soporte para tests async/await|asuncio_mode = auto|
|pytest-cov|Medición de cobertura de tests|fail under 90%|
|AsyncMock|Mock de funciones async|unittest.mock.AsyncMock|
|monkeypatch| Parcheo de métodos runtime| Nativo de pytest|
|Ruff| Análisis estático, cumplimiento de PEP8, y formateador automático de código|pyproject.toml|

# EJECUCION
Para ejecutar la batería de tests, sigue los siguientes pasos:

1. Dirigete al backend
```cd backend```

2. Ejecutar comando
```pytest```

Actualmente gracias a la configuración implementada en el fichero pyproject.toml

[tool.pytest.ini_options]
addopts = "--cov=app --cov-report=term-missing --cov-fail-under=90"

Ejecutando el comando pytest, se ejecuta automáticamente la cobertura y fallo en caso de menor al 90%, si no mantienes el archivo .toml, recuerda utilizar el comando completo.
