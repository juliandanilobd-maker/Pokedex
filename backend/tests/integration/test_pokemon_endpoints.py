from __future__ import annotations

from unittest.mock import patch

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from backend.app.core.config import settings
from backend.app.dependencies.dependencias import (
    get_analyzer_service,
    get_battle_service,
    get_evolution_service,
    get_pokemon_service,
    get_team_service,
)
from backend.app.models.pokemon_models import (
    AnomalyEntry,
    EvolutionNode,
    PokemonDetail,
    Team,
    TeamCreate,
    TeamMember,
    TeamStats,
    TopPokemonEntry,
    TypeAverageStats,
)
from backend.main import app

client = TestClient(app)


# Creamos helpers para testear nuevas rutas implementadas
def _make_member():
    return TeamMember(
        id=1,
        name="bulbasaur",
        types=["grass"],
        hp=45,
        attack=49,
        defense=49,
        speed=45,
        sprite_url="",
    )


def _make_stats():
    return TeamStats(
        total_hp=45,
        total_attack=49,
        total_defense=49,
        total_speed=45,
        avg_hp=45.0,
        avg_attack=49.0,
        avg_defense=49.0,
        avg_speed=45.0,
        type_coverage=["grass"],
    )


def _make_team(id="abc-123", name="Equipo Test"):
    return Team(
        id=id,
        name=name,
        members=[_make_member()],
        stats=_make_stats(),
        created_at="20-24-01-01T00:00:00+00:00",
    )


# Creamos fake clases para comprobar correctamente los endpoints y evitar llamadas
# reales que puedan ralentizar la batería de tests
class FakePokemonService:
    async def get_pokemon_detail(self, identifier: str) -> PokemonDetail:
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
    async def get_evolution_tree(self, identifier: str) -> EvolutionNode:
        if identifier == "1":
            return EvolutionNode(
                id=1,
                name="bulbasaur",
                evolution_details=None,
                children=[],
                sprite_url="",
            )
        raise ValueError("Cadena evolutiva no encontrada")


class FakeBattleService:
    def calculate_effectiveness(self, types: list[str]) -> dict[str, list[str]]:
        if "electric" in types:
            return {
                "weaknesses": ["ground"],
                "resistances": ["electric", "flying", "steel"],
                "immunities": [],
            }

        return {"weaknesses": [], "resistances": [], "immunities": []}


class FakeTeamService:
    def create_team(self, payload: TeamCreate) -> Team:
        return _make_team(name=payload.name)

    def list_teams(self) -> list[Team]:
        return [_make_team()]

    def get_team(self, team_id: str) -> Team:
        if team_id == "abc-123":
            return _make_team()
        raise ValueError(f"No se encontró ningún equipo con ID '{team_id}'")

    def update_team(self, team_id: str, payload: TeamCreate) -> Team:
        if team_id == "abc-123":
            return _make_team(name=payload.name)
        raise ValueError(f"No se encontró ningún equipo con ID '{team_id}'")

    def delete_team(self, team_id: str) -> None:
        if team_id != "abc-123":
            raise ValueError(f"No se encontró ningún equipo con ID '{team_id}'")


class FakeAnalyzerService:
    def average_stats_by_type(self) -> list[TypeAverageStats]:
        return [
            TypeAverageStats(
                type_name="fire",
                sample_size=3,
                avg_hp=58.3,
                avg_attack=66.0,
                avg_defense=59.7,
                avg_speed=81.7,
            )
        ]

    def top_n(self, metric: str = "attack", n: int = 10) -> list[TopPokemonEntry]:
        if metric not in ("hp", "attack", "defense", "speed", "base_exp"):
            raise ValueError(f"Métrica '{metric}' no válida.")
        return [
            TopPokemonEntry(
                id=6,
                name="charizard",
                types=["fire", "flying"],
                value=84,
                metric=metric,
            )
        ]

    def detect_anomalies(
        self, stdev_threshold: float = 2.0, percentile_threshold: float = 0.05
    ) -> list[AnomalyEntry]:
        return [
            AnomalyEntry(
                id=150,
                name="mewtwo",
                types=["psychic"],
                stat_total=436,
                type_average=300.0,
                deviation=2.5,
                method="stddev",
                reason="Outlier",
            )
        ]


# Usamos fixture para inyectar y limpiar automáticamente los fakes en cada test
@pytest.fixture(autouse=True)
def setup_integration_dependencies():
    app.dependency_overrides[get_pokemon_service] = lambda: FakePokemonService()
    app.dependency_overrides[get_evolution_service] = lambda: FakeEvolutionService()
    app.dependency_overrides[get_battle_service] = lambda: FakeBattleService()
    app.dependency_overrides[get_team_service] = lambda: FakeTeamService()
    app.dependency_overrides[get_analyzer_service] = lambda: FakeAnalyzerService()
    yield

    del app.dependency_overrides[get_pokemon_service]
    del app.dependency_overrides[get_evolution_service]
    del app.dependency_overrides[get_battle_service]
    del app.dependency_overrides[get_team_service]
    del app.dependency_overrides[get_analyzer_service]


# IMPLEMENTAMOS LOS TESTS DE INTEGRACIÓN
def test_integration_pokemon_success():
    """Comprobamos que el router dirige la peticion al endpoint /pokemon/{identifier},
    este recibe los datos y los transforma en un JSON, con los valores correctos"""
    endpoint_url = f"{settings.API_PREFIX}/pokemon/pikachu"
    response = client.get(endpoint_url)

    assert response.status_code == 200
    assert response.json()["name"] == "pikachu"
    assert response.json()["types"] == ["electric"]


def test_integration_pokemon_not_found():
    """Este test comprueba que se captura un Value Error y se lanza un 404 Not found,
    en caso de no encontrarse el objeto de busqueda, en una busqueda individual,
    por nombre o ID"""
    response = client.get("/api/v2/pokemon/missing")
    data = response.json()

    assert response.status_code == 404
    assert "Pokemon missing no existe en la base de datos" in data["detail"]


def test_integration_pokemon_generic_exception():
    """Este test comprueba que se captura un Exception y se lanza un 500 fallo del
    servidor en caso de otro error, en ua busqueda individual"""
    with patch(
        "backend.tests.integration.test_pokemon_endpoints.FakePokemonService.get_pokemon_detail",
        side_effect=RuntimeError("Fallo crítico del servidor"),
    ):
        response = client.get("/api/v2/pokemon/25")
        data = response.json()

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert (
        "Error interno al procesar el motor analítico: Fallo crítico del servidor"
        in data["detail"]
    )


def test_integration_evolution_success():
    """Comprobamos que el router dirige la peticion al endpoint /evolution, este recibe
    los datos, los transforma en un JSON, y que se valida correctamente la estructura
    del árbol evolutivo"""
    response = client.get("/api/v2/pokemon/1/evolution")

    assert response.status_code == 200
    assert response.json()["name"] == "bulbasaur"
    assert response.json()["children"] == []


def test_integration_evolution_not_found():
    """Este test comprueba que se captura un Value Error y se lanza un 404 Not found,
    en caso de no encontrarse el objeto de busqueda, en una busqueda de un árbol
    evolutivo, por nombre o ID"""
    response = client.get("/api/v2/pokemon/2/evolution")
    data = response.json()

    assert response.status_code == 404
    assert "Cadena evolutiva no encontrada" in data["detail"]


def test_integration_evolution_generic_exception():
    """Este test comprueba que se captura un Exception y se lanza un 500
    fallo del servidor en caso de otro error, en ua busqueda de un árbol evolutivo"""
    with patch(
        "backend.tests.integration.test_pokemon_endpoints.FakeEvolutionService.get_evolution_tree",
        side_effect=RuntimeError("Fallo crítico del servidor"),
    ):
        response = client.get("/api/v2/pokemon/1/evolution")
        data = response.json()

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert (
        "Error interno al procesar el motor analítico: Fallo crítico del servidor"
        in data["detail"]
    )


def test_integration_effectiveness_success():
    """Comprobamos que el router dirige la peticion al endpoint /effectiveness,
    este recibe los datos y los transforma en un JSON, con los valores correctos de
    efectividad en combate"""
    response = client.get("/api/v2/pokemon/pikachu/effectiveness")
    data = response.json()

    assert response.status_code == 200
    assert "ground" in data["weaknesses"]
    assert "electric" in data["resistances"]
    assert len(data["immunities"]) == 0


def test_integration_effectiveness_not_found():
    """Este test comprueba que se captura un Value Error y se lanza un 404 Not found,
    en caso de no encontrarse el objeto de busqueda, en una busqueda de efectividad en
    combate"""
    response = client.get("/api/v2/pokemon/missing/effectiveness")
    data = response.json()

    assert response.status_code == 404
    assert "Pokemon missing no existe en la base de datos" in data["detail"]


def test_integration_effectiveness_generic_exception():
    """Este test comprueba que se captura un Exception y se lanza un 500 fallo del
    servidor en caso de otro error, en ua busqueda de efectividad en combate"""
    with patch(
        "backend.tests.integration.test_pokemon_endpoints.FakeBattleService.calculate_effectiveness",
        side_effect=RuntimeError("Fallo crítico del servidor"),
    ):
        response = client.get("/api/v2/pokemon/pikachu/effectiveness")
        data = response.json()

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert (
        "Error interno al procesar el motor analítico: Fallo crítico del servidor"
        in data["detail"]
    )


def test_create_team_success():
    """Comprobamos que se crea un equipo correctamente"""
    response = client.post(
        "/api/v2/teams", json={"name": "Mi Equipo", "pokemon_ids": [1]}
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["name"] == "Mi Equipo"


def test_create_team_value_error_returns_400():
    """Comprobamos que un ValueError al crear equipo devuelve 400"""
    with patch.object(
        FakeTeamService, "create_team", side_effect=ValueError("Demasiados Pokemon")
    ):
        response = client.post("/api/v2/teams", json={"name": "X", "pokemon_ids": [1]})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Demasiados Pokemon" in response.json()["detail"]


def test_create_team_generic_exception_returns_500():
    """Comprobamos que una excepción genérica al crear equipo devuelve 500"""
    with patch.object(
        FakeTeamService, "create_team", side_effect=RuntimeError("Fallo interno")
    ):
        response = client.post("/api/v2/teams", json={"name": "X", "pokemon_ids": [1]})
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


def test_list_teams_success():
    """Comprobamos que se listan los equipos correctamente"""
    response = client.get("/api/v2/teams")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
    assert response.json()[0]["name"] == "Equipo Test"


def test_list_teams_generic_exception_returns_500():
    """Comprobamos que una excepción genérica al listar equipos devuelve 500"""
    with patch.object(
        FakeTeamService, "list_teams", side_effect=RuntimeError("Error DB")
    ):
        response = client.get("/api/v2/teams")
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


def test_get_team_success():
    """Comprobamos que se obtiene un equipo por ID correctamente"""
    response = client.get("/api/v2/teams/abc-123")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == "abc-123"


def test_get_team_not_found_returns_404():
    """Comprobamos que un equipo inexistente devuelve 404"""
    response = client.get("/api/v2/teams/no-existe")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_team_generic_exception_returns_500():
    """Comprobamos que una excepción genérica al obtener equipo devuelve 500"""
    with patch.object(FakeTeamService, "get_team", side_effect=RuntimeError("Error")):
        response = client.get("/api/v2/teams/abc-123")
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


def test_update_team_success():
    """Comprobamos que se actualiza un equipo correctamente"""
    response = client.put(
        "/api/v2/teams/abc-123", json={"name": "Actualizado", "pokemon_ids": [1]}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "Actualizado"


def test_update_team_not_found_returns_404():
    """Comprobamos que actualizar un equipo inexistente devuelve 404"""
    response = client.put(
        "/api/v2/teams/no-existe", json={"name": "X", "pokemon_ids": [1]}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_team_generic_exception_returns_500():
    """Comprobamos que una excepción genérica al actualizar equipo devuelve 500"""
    with patch.object(
        FakeTeamService, "update_team", side_effect=RuntimeError("Crash")
    ):
        response = client.put(
            "/api/v2/teams/abc-123", json={"name": "X", "pokemon_ids": [1]}
        )
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


def test_delete_team_success():
    """Comprobamos que se elimina un equipo correctamente"""
    response = client.delete("/api/v2/teams/abc-123")
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_team_not_found_returns_404():
    """Comprobamos que eliminar un equipo inexistente devuelve 404"""
    response = client.delete("/api/v2/teams/no-existe")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_team_generic_exception_returns_500():
    """Comprobamos que una excepción genérica al eliminar equipo devuelve 500"""
    with patch.object(
        FakeTeamService, "delete_team", side_effect=RuntimeError("Crash")
    ):
        response = client.delete("/api/v2/teams/abc-123")
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


def test_average_by_type_success():
    """Comprobamos que se obtienen los promedios por tipo correctamente"""
    response = client.get("/api/v2/analytics/average-by-type")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0]["type_name"] == "fire"


def test_average_by_type_value_error_returns_404():
    """Comprobamos que un ValueError en average-by-type devuelve 404"""
    with patch.object(
        FakeAnalyzerService,
        "average_stats_by_type",
        side_effect=ValueError("Sin datos"),
    ):
        response = client.get("/api/v2/analytics/average-by-type")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_average_by_type_generic_exception_returns_500():
    """Comprobamos que una excepción genérica en average-by-type devuelve 500"""
    with patch.object(
        FakeAnalyzerService, "average_stats_by_type", side_effect=RuntimeError("Crash")
    ):
        response = client.get("/api/v2/analytics/average-by-type")
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


def test_top_pokemon_success():
    """Comprobamos que se obtiene el top de Pokemon correctamente"""
    response = client.get("/api/v2/analytics/top?metric=attack&n=5")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0]["name"] == "charizard"


def test_top_pokemon_invalid_metric_returns_400():
    """Comprobamos que una métrica inválida en top devuelve 400"""
    with patch.object(
        FakeAnalyzerService, "top_n", side_effect=ValueError("Métrica no válida")
    ):
        response = client.get("/api/v2/analytics/top?metric=stamina")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_top_pokemon_generic_exception_returns_500():
    """Comprobamos que una excepción genérica en top devuelve 500"""
    with patch.object(FakeAnalyzerService, "top_n", side_effect=RuntimeError("Crash")):
        response = client.get("/api/v2/analytics/top")
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


def test_anomalies_success():
    """Comprobamos que se detectan anomalías correctamente"""
    response = client.get("/api/v2/analytics/anomalies")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data[0]["name"] == "mewtwo"
    assert data[0]["method"] == "stddev"


def test_anomalies_value_error_returns_404():
    """Comprobamos que un ValueError en anomalies devuelve 404"""
    with patch.object(
        FakeAnalyzerService, "detect_anomalies", side_effect=ValueError("Sin datos")
    ):
        response = client.get("/api/v2/analytics/anomalies")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_anomalies_generic_exception_returns_500():
    """Comprobamos que una excepción genérica en anomalies devuelve 500"""
    with patch.object(
        FakeAnalyzerService, "detect_anomalies", side_effect=RuntimeError("Crash")
    ):
        response = client.get("/api/v2/analytics/anomalies")
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
