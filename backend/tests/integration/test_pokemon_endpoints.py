import pytest
from fastapi.testclient import TestClient

from backend.app.core.config import settings
from backend.app.dependencies.dependencias import (
    get_evolution_service,
)
from backend.app.models.pokemon_models import EvolutionNode, PokemonDetail
from backend.main import app

client = TestClient(app)


# Creamos una fake class para Pokemon Service
class FakePokemonService:
    def get_pokemon_detail(self, identifier: str) -> PokemonDetail:
        if identifier in ("25", "pikachu"):
            return PokemonDetail(
                id=25,
                name="pikachu",
                types=["electric"],
                stats={"speed": 90},
                abilities=["static"],
                height=4,
                weight=60,
                base_experience=112,
                sprite_url="pika.png",
                sprite_shiny="pika_s.png",
            )
        raise ValueError(f"Pokemon {identifier} no existe en la base de datos")


class FakeEvolutionService:
    def get_evolution_tree(self, identifier: str) -> EvolutionNode:
        if identifier == "1":
            return EvolutionNode(name="bulbasaur", evolution_details=None, children=[])
        raise ValueError("Cadena evolutiva no encontrada")


# Usamos fixture para inyectar y limpiar automáticamente los fakes en cada test
@pytest.fixture(autouse=True)
def setup_integration_dependencies():
    app.dependency_overrides[get_evolution_service] = lambda: FakePokemonService()
    app.dependency_overrides[get_evolution_service] = lambda: FakeEvolutionService()
    yield
    app.dependency_overrides.clear()


# IMPLEMENTAMOS LOS TESTS DE INTEGRACIÓN
# Comprobamos que el router recibe el objeto del servicio y lo transforma en JSON
def test_integration_pokemon_success():

    endpoint_url = f"{settings.API_PREFIX}/pokemon/pikachu"
    response = client.get(endpoint_url)

    assert response.status_code == 200
    assert response.json()["name"] == "pikachu"
    assert response.json()["types"] == ["electric"]


# Comprobamos que se captura un ValueError del servicio por el catch de la ruta
# y lanza un 404
def test_integration_pokemon_not_found():
    response = client.get("/api/v1/pokemon/missing")

    assert response.status_code == 404
    assert "No se encontro el recurso" in response.json()["detail"]


# Comprobamos que se valida la estructura jerarquica del árbol evolutivo mock
def test_integration_evolution_success():
    response = client.get("/api/v1/pokemon/1/evolution")

    assert response.status_code == 200
    assert response.json()["name"] == "bulbasaur"
    assert response.json()["children"] == []
