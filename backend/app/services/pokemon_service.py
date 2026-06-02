from __future__ import annotations

from backend.app.models.pokemon_models import PokemonDetail
from backend.app.parsers.pokemon_parser import parse_pokemon


# Se encarga de la lógica de negocio de Pokemon
class PokemonService:
    def __init__(self, client) -> None:
        self.client = client

    def get_pokemon_detail(self, identifier: str) -> PokemonDetail:
        """
        Obtiene los datos completos de un Pokemon.

        Args:
            identifier: Nombre (str) o ID (int) del Pokemon, usando el arg
                        identifier,
                        podremos realizar nuestra busqueda por cualquiera
                        de estos parametros.
                        Ej: "pikachu", "charizard", 25, 6

        Returns:
            Diccionario con todos los datos del Pokemon.
            Usa models.parse_pokemon() para convertirlo a PokemonDetail.
        """
        data = self.client.get_pokemon(identifier)
        # identifier= para poder nombrar en nuestra pokedex ya sea name or id
        return parse_pokemon(data)
