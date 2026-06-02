from backend.app.clients.pokeapi_client import PokeAPIClient

from backend.app.services.pokemon_service import PokemonService
from backend.app.services.evolution_service import EvolutionService
from backend.app.cache.cache_manager import CacheManager

cache = CacheManager()

client = PokeAPIClient(cache)

pokemon_service = PokemonService(client)

evolution_service = EvolutionService(client)
