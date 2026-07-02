"""
Este es nuestro módulo de rutas, se establece un orquestador de nuestro backend.

El manejo de de rutas se realiza de la siguiente manera:
return
Ej ->
1. Ingreso de petición: /pokemon/{identifier}/effectiveness.
2. Usa DI, FastAPI intercepta la llamada e inyecta los diferentes servicios.
3. Se orquestan los diferentes servicios y sus llamados.
4. Moldeo de la respuesta, recibe los datos y los empaqueta dentro del modelo en models.
5. Devuelve el modelo, FastAPI valida con las reglas de acuerdo al modelo establecido.
"""

import asyncio

from fastapi import APIRouter, Depends, HTTPException, status

from backend.app.core.config import settings
from backend.app.dependencies.dependencias import (
    get_analyzer_service,
    get_battle_service,
    get_evolution_service,
    get_filter_service,
    get_pokemon_service,
    get_predictor_service,
    get_simulator_service,
    get_team_service,
)
from backend.app.models.pokemon_models import (
    AnomalyEntry,
    EvolutionNode,
    PokemonDetail,
    PokemonEffectiveness,
    PokemonFilter,
    PredictionResult,
    SimulatorResult,
    Team,
    TeamCreate,
    TopPokemonEntry,
    TypeAverageStats,
)
from backend.app.services.analyzer_service import AnalyzerService
from backend.app.services.battle_service import BattleService
from backend.app.services.evolution_service import EvolutionService
from backend.app.services.filter_service import FilterService
from backend.app.services.pokemon_service import PokemonService
from backend.app.services.predictor_service import PredictorService
from backend.app.services.simulator_service import SimulatorService
from backend.app.services.team_service import TeamService

# Iniciamos un subenrutador utilizando el prefijo de la API
router = APIRouter(prefix=settings.API_PREFIX)

# ENDPOINTS CON DEPENDENCY INJECTION


# Utilizamos el decorador router, para establecer el comportamiento de FastAPI
@router.get(
    "/filter",
    tags=["Filter"],  # Permite agrupar la documentacion en futuro de Swagger UI
    response_model=list[
        dict
    ],  # la respuesta no debe ser todos los parametros del filtro, sino una lista
    status_code=status.HTTP_200_OK,  # Si la respuesta cumple los parametros = 200 Ok
    summary="Obtener filtros de estadistica, generación o tipo de un Pokemon",
)

# Usamos funciones asincronas para usar bucles de eventos. La función no espera
# la respuesta de la API para atender otras peticiones
async def get_filtered_pokemons(
    filters: PokemonFilter = Depends(),
    filter_service: FilterService = Depends(get_filter_service),
) -> list[dict]:
    """Este endpoint se encarga de ejecutar las llamadas internas a FilterService"""

    try:
        return filter_service.filter_pokemons(**filters.model_dump())

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al procesar el motor analítico: {e!s}",
        ) from e


@router.get(
    "/pokemon/{identifier}/evolution",
    tags=["Evolution"],
    response_model=EvolutionNode,  # Establece el parametro de una respuesta 200 OK
    status_code=status.HTTP_200_OK,
    summary="Obtener las evoluciones de un Pokemon y sus requisitos",
)
async def get_evolution_chain(
    identifier: str,
    # Usamos inyeccion de dependencias, permitiendo que FastAPI instancie el servicio
    # Es decir, no se necesitan conectar a bases de datos o realizar llamadas, FastAPI
    # Entrega el servicio directo a routes
    evolution_service: EvolutionService = Depends(get_evolution_service),
):
    """Este endpoint se encarga de ejecutar las llamadas internas a EvolutionService"""
    try:
        # Presentamos un nodo tipado con un Dataclass, y lo serializamos a diccionario
        # para poder procesar la respuesta JSON.
        return await evolution_service.get_evolution_tree(identifier)

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al procesar el motor analítico: {e!s}",
        ) from e


@router.get(
    "/pokemon/{identifier}/effectiveness",
    tags=["Battle"],
    response_model=PokemonEffectiveness,
    status_code=status.HTTP_200_OK,
    summary="Obtener la efectividad elemental estrategica de un Pokemon",
)
async def get_pokemon_effectiveness(
    identifier: str,
    pokemon_service: PokemonService = Depends(get_pokemon_service),
    battle_service: BattleService = Depends(get_battle_service),
) -> PokemonEffectiveness:
    """Este endpoint se encarga de ejecutar las llamadas internas a BattleService"""
    try:
        pokemon_data = await pokemon_service.get_pokemon_detail(identifier)
        pokemon_types = pokemon_data.types

        effectiveness = battle_service.calculate_effectiveness(pokemon_types)

        return PokemonEffectiveness(
            weaknesses_x4=effectiveness.get("weaknesses_x4", []),
            weaknesses=effectiveness.get("weaknesses", []),
            resistances=effectiveness.get("resistances", []),
            resistances_x025=effectiveness.get("resistances_x025", []),
            immunities=effectiveness.get("immunities", []),
        )

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al procesar el motor analítico: {e!s}",
        ) from e


@router.get(
    "/pokemon/{identifier}",
    tags=["Pokemon"],
    response_model=PokemonDetail,
    status_code=status.HTTP_200_OK,
    summary="Obtener los detalles de un Pokemon",
)
async def get_pokemon(
    identifier: str, pokemon_service: PokemonService = Depends(get_pokemon_service)
):
    """Este endpoint se encarga de ejecutar las llamadas internas a PokemonService"""
    try:
        return await pokemon_service.get_pokemon_detail(identifier)

    except ValueError as e:
        # Se captura el error con un Value Error si la API devuelve un 404
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al procesar el motor analítico: {e!s}",
        ) from e


@router.get(
    "/pokemon/{identifier}/full-detail",
    tags=["Pokemon"],
    status_code=status.HTTP_200_OK,
    summary="Obtener detalles, evoluciones y efectividad en una única llamada paralela",
)
async def get_pokemon_full_detail(
    identifier: str,
    pokemon_service: PokemonService = Depends(get_pokemon_service),
    evolution_service: EvolutionService = Depends(get_evolution_service),
    battle_service: BattleService = Depends(get_battle_service),
):
    """Construímos un endpoint que orqueste todas las llamadas internas a los servicios
    en paralelo usando asyncio.gather, reduciendo el tiempo de respuesta"""

    try:
        tarea_pokemon = pokemon_service.get_pokemon_detail(identifier)
        tarea_evolution = evolution_service.get_evolution_tree(identifier)

        pokemon_data, evo_data = await asyncio.gather(tarea_pokemon, tarea_evolution)

        effectiveness_data = battle_service.calculate_effectiveness(pokemon_data.types)

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno en el orquestador: {e!s}",
        ) from e

    else:
        effectiveness = PokemonEffectiveness(
            weaknesses_x4=effectiveness_data.get("weaknesses_x4", []),
            weaknesses=effectiveness_data.get("weaknesses", []),
            resistances=effectiveness_data.get("resistances", []),
            resistances_x025=effectiveness_data.get("resistances_x025", []),
            immunities=effectiveness_data.get("immunities", []),
        )

        return {
            "pokemon": pokemon_data,
            "evolution": evo_data,
            "effectiveness": effectiveness,
        }


@router.post(
    "/teams",
    tags=["Teams"],
    response_model=Team,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo equipo Pokemon (máximo 6 integrantes)",
)
async def create_team(
    payload: TeamCreate, team_service: TeamService = Depends(get_team_service)
) -> Team:

    try:
        return team_service.create_team(payload)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al crear el equipo: {e!s}",
        ) from e


@router.get(
    "/teams",
    tags=["Teams"],
    response_model=list[Team],
    status_code=status.HTTP_200_OK,
    summary="Listar todos los equipos guardados",
)
async def list_teams(
    team_service: TeamService = Depends(get_team_service),
) -> list[Team]:

    try:
        return team_service.list_teams()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al listar los equipos: {e!s}",
        ) from e


@router.get(
    "/teams/{team_id}",
    tags=["Teams"],
    response_model=Team,
    summary="Obtener el detalle de un equipo por ID",
)
async def get_team(
    team_id: str, team_service: TeamService = Depends(get_team_service)
) -> Team:

    try:
        return team_service.get_team(team_id)

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al obtener el equipo: {e!s}",
        ) from e


@router.put(
    "/teams/{team_id}",
    tags=["Teams"],
    response_model=Team,
    status_code=status.HTTP_200_OK,
    summary="Actualizar el nombre o los integrantes de un equipo",
)
async def update_team(
    team_id: str,
    payload: TeamCreate,
    team_service: TeamService = Depends(get_team_service),
) -> Team:

    try:
        return team_service.update_team(team_id, payload)

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al actualizar el equipo: {e!s}",
        ) from e


@router.delete(
    "/teams/{team_id}",
    tags=["Teams"],
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un equipo por ID",
)
async def delete_team(
    team_id: str, team_service: TeamService = Depends(get_team_service)
) -> None:

    try:
        team_service.delete_team(team_id)

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al eliminar el equipo: {e!s}",
        ) from e


@router.get(
    "/analytics/average-by-type",
    tags=["Analytics"],
    response_model=list[TypeAverageStats],
    status_code=status.HTTP_200_OK,
    summary="Promedio de stats (hp/attack/defense/speed) agrupado por tipo elemental",
)
async def get_average_stats_by_type(
    analyzer_service: AnalyzerService = Depends(get_analyzer_service),
) -> list[TypeAverageStats]:

    try:
        return analyzer_service.average_stats_by_type()

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al calcular estadísticas: {e!s}",
        ) from e


@router.get(
    "/analytics/top",
    tags=["Analytics"],
    response_model=list[TopPokemonEntry],
    status_code=status.HTTP_200_OK,
    summary="Top-N de Pokemon según una métrica (hp, attack, defense, speed, base_exp)",
)
async def get_top_pokemon(
    metric: str = "attack",
    n: int = 10,
    analyzer_service: AnalyzerService = Depends(get_analyzer_service),
) -> list[TopPokemonEntry]:

    try:
        return analyzer_service.top_n(metric=metric, n=n)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al calcular el ranking: {e!s}",
        ) from e


@router.get(
    "/analytics/anomalies",
    tags=["Analytics"],
    response_model=list[AnomalyEntry],
    status_code=status.HTTP_200_OK,
    summary="Detecta Pokemon con stats anómalas respecto a su tipo o al dataset global",
)
async def get_anomalies(
    stddev_threshold: float = 2.0,
    percentile_threshold: float = 0.05,
    analyzer_service: AnalyzerService = Depends(get_analyzer_service),
) -> list[AnomalyEntry]:

    try:
        return analyzer_service.detect_anomalies(
            stdev_threshold=stddev_threshold, percentile_threshold=percentile_threshold
        )

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al detectar anomalías: {e!s}",
        ) from e

@router.get(
    "/analytics/prediction",
    tags=["Analytics"],
    response_model=PredictionResult,
    status_code=status.HTTP_200_OK,
    summary="Predicción de stats para un tipo elemental usando media móvil simple"
)
async def get_prediction(
    primary_type: str,
    secondary_type: str | None = None,
    reference_generation: int | None = None,
    predictor_service: PredictorService = Depends(get_predictor_service),
) -> PredictionResult:

    try:
        return predictor_service.predict_stats(
            primary_type=primary_type,
            secondary_type=secondary_type,
        )

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al calcular la predicción: {e!s}",
        ) from e

@router.post(
    "/analytics/simulate",
    tags=["Analytics"],
    response_model=SimulatorResult,
    status_code=status.HTTP_200_OK,
    summary="Genera Pokemon sintético y los acumula en un CSV"
)
async def simulate_pokemons(
    n: int = 10,
    pokemon_type: str = "normal",
    generation: int = 1,
    seed: int | None = None,
    simulator_service: SimulatorService = Depends(get_simulator_service),
) -> SimulatorResult:

    try:
        return simulator_service.generate(
            n=n,
            pokemon_type=pokemon_type,
            generation=generation,
            seed=seed,
        )

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al calcular la predicción: {e!s}",
        ) from e
