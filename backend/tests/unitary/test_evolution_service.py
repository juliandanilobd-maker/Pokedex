from backend.app.services.evolution_service import EvolutionService


class MockClient:
    def get_species(self, identifier):

        return {"evolution_chain": {"url": "test_url"}}

    def get(self, url):

        return {
            "chain": {
                "species": {"name": "bulbasaur"},
                "evolves_to": [],
            }
        }


def test_get_evolution_tree():

    service = EvolutionService(MockClient())

    tree = service.get_evolution_tree("1")

    assert tree.name == "bulbasaur"
