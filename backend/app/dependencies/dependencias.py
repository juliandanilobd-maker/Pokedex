import asyncio

from fastapi import Depends

from backend.app.cache.cache_manager import CacheManager
from backend.app.clients.pokeapi_client import PokeAPIClient
from backend.app.data.scripts.dataset_generator import load_dataset
from backend.app.services.analyzer_service import AnalyzerService
from backend.app.services.battle_service import BattleService
from backend.app.services.evolution_service import EvolutionService
from backend.app.services.filter_service import FilterService
from backend.app.services.pokemon_service import PokemonService
from backend.app.services.predictor_service import PredictorService
from backend.app.services.simulator_service import SimulatorService
from backend.app.services.team_service import TeamService

# Instanciamos los componentes de infraestructura como Singletons globales,
# permitiendo que la conexión a la cache permanezca abierta, y que no se reinicie
# el estado del rate limit entre cada petición
_cache_instance = CacheManager()
_client_instance: PokeAPIClient | None = None
_client_loop: asyncio.AbstractEventLoop | None = None


async def get_client() -> PokeAPIClient:
    global _client_instance, _client_loop

    try:
        current_loop = asyncio.get_running_loop()
    except RuntimeError:
        current_loop = None

    if _client_instance is None or _client_loop is not current_loop:
        _client_instance = PokeAPIClient(cache=_cache_instance)
        _client_loop = current_loop

    return _client_instance


# Inyectamos el cliente en los servicios, los servicios se instancian en cada petición.
def get_pokemon_service(client: PokeAPIClient = Depends(get_client)) -> PokemonService:
    return PokemonService(client=client)


def get_evolution_service(
    client: PokeAPIClient = Depends(get_client),
) -> EvolutionService:
    return EvolutionService(client=client)


# A pesar de ser una clase autosuficiente, es decir, no requiere de llamadas a la API u
# otros servicios, en teoría no se inyecta nada, sin embargo, mantenemos la inyección,
# para permitir que el endpoint BattleService se maneje de forma eficiente, facilitando
# escalabilidad a futuro, para implementación de logs, métricas o cambios en la clase
def get_battle_service() -> BattleService:
    return BattleService()


def get_filter_service() -> FilterService:
    return FilterService()


def get_team_service() -> TeamService:
    return TeamService(dataset_loader=load_dataset)


def get_analyzer_service() -> AnalyzerService:
    return AnalyzerService(dataset_loader=load_dataset)


def get_predictor_service() -> PredictorService:
    return PredictorService(dataset_loader=load_dataset)


def get_simulator_service() -> SimulatorService:
    return SimulatorService(dataset_loader=load_dataset)
