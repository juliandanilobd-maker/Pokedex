"""
Este módulo es el servicio de dominio encargado de coordinar la construcción del
árbol evolutivo
"""

from backend.app.parsers.evolution_parser import parse_evolution_tree


class EvolutionService:
    def __init__(self, client):
        self.client = client

    def get_evolution_tree(self, identifier: str):
        # La PokeAPI no permite consultar directamente las evoluciones, por lo que
        # primero se debe consultar el endpoint de la especie para obtener la URL
        species_data = self.client.get_species(identifier)

        evo_url = species_data.get("evolution_chain", {}).get("url")

        if not evo_url:
            return None

        # Con la URL se puede solicitar los datos completos
        evolution_data = self.client.get(evo_url)

        # Se delega el parseo y construcción del árbol al parser evolutivo, abstrayendo
        # el servicio, reduciendo su complejidad.
        return parse_evolution_tree(evolution_data["chain"])
