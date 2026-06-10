from fastapi import Depends

from backend.app.cache.cache_manager import CacheManager
from backend.app.clients.pokeapi_client import PokeAPIClient
from backend.app.services.battle_service import BattleService
from backend.app.services.evolution_service import EvolutionService
from backend.app.services.pokemon_service import PokemonService
from backend.app.services.type_service import TypeService

# Instanciamos los componentes de infraestructura como Singletons globales,
# permitiendo que la conexión a la cache permanezca abierta, y que no se reinicie
# el estado del rate limit entre cada petición
_cache_instance = CacheManager()
_client_instance = PokeAPIClient(cache=_cache_instance)
_type_instance = TypeService(client=_client_instance)


def get_client() -> PokeAPIClient:
    return _client_instance


def get_type_service() -> TypeService:
    return _type_instance


# Inyectamos el cliente en los servicios, los servicios se instancian en cada petición.
def get_pokemon_service(client: PokeAPIClient = Depends(get_client)) -> PokemonService:
    return PokemonService(client=client)


def get_evolution_service(
    client: PokeAPIClient = Depends(get_client),
) -> EvolutionService:
    return EvolutionService(client=client)


def get_battle_service(
    type_service: TypeService = Depends(get_type_service),
) -> BattleService:
    return BattleService(type_service=type_service)
