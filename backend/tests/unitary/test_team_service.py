from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from backend.app.models.pokemon_models import Team, TeamCreate
from backend.app.services.team_service import TeamService

# Configuramos un mock dataset para iniciar los tests
FAKE_DATASET = [
    {
        "id": 1,
        "name": "bulbasaur",
        "types": ["grass", "poison"],
        "hp": 45,
        "attack": 49,
        "defense": 49,
        "speed": 45,
        "sprite_url": "bulba.png",
    },
    {
        "id": 4,
        "name": "charmander",
        "types": ["fire"],
        "hp": 39,
        "attack": 52,
        "defense": 43,
        "speed": 65,
        "sprite_url": "char.png",
    },
    {
        "id": 7,
        "name": "squirtle",
        "types": ["water"],
        "hp": 44,
        "attack": 48,
        "defense": 65,
        "speed": 43,
        "sprite_url": "squi.png",
    },
    {
        "id": 25,
        "name": "pikachu",
        "types": ["electric"],
        "hp": 35,
        "attack": 55,
        "defense": 40,
        "speed": 90,
        "sprite_url": "pika.png",
    },
]


def fake_loader():
    return FAKE_DATASET


def make_service() -> TeamService:
    return TeamService(dataset_loader=fake_loader)


def test_resolve_members_return_team_members():
    """Este test comprueba que se devuelve correctamente los miembros del equipo"""

    service = make_service()
    members = service._resolve_members([1, 4])

    assert len(members) == 2
    assert members[0].name == "bulbasaur"
    assert members[1].name == "charmander"


def test_resolve_members_not_found_id():
    """Este test comprueba el manejo del error en caso de un ID no encontrado"""

    service = make_service()
    with pytest.raises(ValueError, match="999"):
        service._resolve_members([999])


def test_resolver_members_types_asigned_correctly():
    """Este test comprueba que se asigna correctamente el tipo al Pokemon"""

    service = make_service()
    members = service._resolve_members([25])

    assert members[0].types == ["electric"]


def test_calculate_total_stats_correctly():
    """Este test comprueba que se calcule correctamente las estadísticas
    sumadas del equipo"""

    service = make_service()
    members = service._resolve_members([1, 4])
    stats = service._calcuate_stats(members)

    assert stats.total_hp == 45 + 39
    assert stats.total_attack == 49 + 52
    assert stats.total_defense == 49 + 43
    assert stats.total_speed == 45 + 65


def test_calculate_avg_stats():
    """Este test comprueba que se calculen correctamente el promedio
    de las estadísticas"""

    service = make_service()
    members = service._resolve_members([1, 4])
    stats = service._calcuate_stats(members)

    assert stats.avg_hp == round((45 + 39) / 2, 2)
    assert stats.avg_attack == round((49 + 52) / 2, 2)


def test_calculate_stats_coverage_for_types():
    """Este test comprueba que se calcule correctamente la cobertura de
    tipos del equipo"""

    service = make_service()
    members = service._resolve_members([1, 4, 7])  # grass/poison, fire, water
    stats = service._calcuate_stats(members)

    assert "fire" in stats.type_coverage
    assert "water" in stats.type_coverage
    assert "grass" in stats.type_coverage
    assert stats.type_coverage == sorted(stats.type_coverage)


def test_create_team_valid_team(tmp_path):
    """Este test comprueba que se crea correctamente el equipo"""

    service = make_service()
    payload = TeamCreate(name="Equipo A", pokemon_ids=[1, 4])

    with patch("backend.app.services.team_service.TEAMS_FILE", tmp_path / "teams.json"):
        team = service.create_team(payload)

    assert isinstance(team, Team)
    assert team.name == "Equipo A"
    assert len(team.members) == 2


def test_create_team_persistance_json(tmp_path):
    """Este test comprueba que el equipo creado persiste en un formato
    JSON en local"""

    import json

    service = make_service()
    payload = TeamCreate(name="Equipo B", pokemon_ids=[7])

    teams_file = tmp_path / "teams.json"
    with patch("backend.app.services.team_service.TEAMS_FILE", teams_file):
        service.create_team(payload)

    data = json.loads(teams_file.read_text(encoding="utf-8"))
    assert len(data) == 1
    assert data[0]["name"] == "Equipo B"


def test_create_6_member_team_raises_error():
    """Este test comprueba que no se puede crear un equipo de 6 miembros"""

    service = make_service()

    with pytest.raises(ValueError, match="más de"):
        # TeamCreate ya valida max_length=6, así que lo probamos
        # directamente en el servicio con un mock del payload
        mock_payload = MagicMock()
        mock_payload.pokemon_ids = [1, 4, 7, 25, 1, 4, 7]
        mock_payload.name = "Gigante"
        service.create_team(mock_payload)


def test_list_teams_returns_saved_teams(tmp_path):
    """Este test comprueba que se listan correctamente los equipos guardados"""

    service = make_service()
    payload = TeamCreate(name="Equipo C", pokemon_ids=[1])
    teams_file = tmp_path / "teams.json"

    with patch("backend.app.services.team_service.TEAMS_FILE", teams_file):
        service.create_team(payload)
        teams = service.list_teams()

    assert len(teams) == 1
    assert teams[0].name == "Equipo C"


def test_list_teams_returns_empty_list_when_no_saved_teams(tmp_path):
    """Este test comprueba que si no se han guardado equipos,
    se retorna una lista vacía"""

    service = make_service()
    with patch(
        "backend.app.services.team_service.TEAMS_FILE", tmp_path / "no_existe.json"
    ):
        result = service.list_teams()
    assert result == []


def test_get_team_for_id_returns_correct_team(tmp_path):
    """Este test comprueba que si se busca por ID un equipo, se devuelva
    correctamente"""

    service = make_service()
    payload = TeamCreate(name="Equipo D", pokemon_ids=[4])
    teams_file = tmp_path / "teams.json"

    with patch("backend.app.services.team_service.TEAMS_FILE", teams_file):
        created = service.create_team(payload)
        found = service.get_team(created.id)

    assert found.id == created.id
    assert found.name == "Equipo D"


def test_get_team_id_no_match_raises_error(tmp_path):
    """Este test comprueba que se captura el error en caso de un ID
    inválido"""

    service = make_service()
    teams_file = tmp_path / "teams.json"

    with (
        patch("backend.app.services.team_service.TEAMS_FILE", teams_file),
        pytest.raises(ValueError),
    ):
        service.get_team("id-inexistente")


def test_update_team_changes_name_and_members(tmp_path):
    """Este test comprueba que al usar update team, se cambia el nombre
    y los miembros en el"""

    service = make_service()
    teams_file = tmp_path / "teams.json"

    with patch("backend.app.services.team_service.TEAMS_FILE", teams_file):
        created = service.create_team(TeamCreate(name="Original", pokemon_ids=[1]))
        updated = service.update_team(
            created.id, TeamCreate(name="Actualizado", pokemon_ids=[4, 7])
        )

    assert updated.name == "Actualizado"
    assert len(updated.members) == 2


def test_update_team_no_id_raises_error(tmp_path):
    """Este test comprueba que se captura el error en caso de actualizar
    un equipo en caso de un ID inválido"""

    service = make_service()
    teams_file = tmp_path / "teams.json"

    with (
        patch("backend.app.services.team_service.TEAMS_FILE", teams_file),
        pytest.raises(ValueError),
    ):
        service.update_team("no-existe", TeamCreate(name="X", pokemon_ids=[1]))


def test_delete_team_correctly(tmp_path):
    """Este test comprueba que se elimina correctamente un equipo"""

    service = make_service()
    teams_file = tmp_path / "teams.json"

    with patch("backend.app.services.team_service.TEAMS_FILE", teams_file):
        created = service.create_team(TeamCreate(name="Borrar", pokemon_ids=[1]))
        service.delete_team(created.id)
        teams = service.list_teams()

    assert len(teams) == 0


def test_delete_team_no_id_raises_error(tmp_path):
    """Este test comprueba que se captura el error en caso de eliminar
    un equipo en caso de un ID inválido"""

    service = make_service()
    teams_file = tmp_path / "teams.json"

    with (
        patch("backend.app.services.team_service.TEAMS_FILE", teams_file),
        pytest.raises(ValueError),
    ):
        service.delete_team("fantasma")


def test_read_all_teams_invalid_json_returns_empty(tmp_path):
    """Este test comprueba la captura del error en caso de JSON inválido"""

    service = make_service()

    teams_file = tmp_path / "teams.json"
    teams_file.write_text("{json invalido}", encoding="utf-8")

    with patch("backend.app.services.team_service.TEAMS_FILE", teams_file):
        assert service._read_all_teams() == []


def test_load_pokemon_index_builds_dictionary():
    """Este test comprueba que se carga el dataset"""

    service = make_service()

    index = service._load_pokemon_index()

    assert len(index) == 4
    assert index[25]["name"] == "pikachu"


def test_get_team_by_name(tmp_path):
    """Este test comprueba que se puede buscar correctamente un equipo
    por nombre"""

    service = make_service()
    teams_file = tmp_path / "teams.json"

    with patch("backend.app.services.team_service.TEAMS_FILE", teams_file):
        created = service.create_team(
            TeamCreate(name="Equipo Especial", pokemon_ids=[1])
        )

        found = service.get_team("Equipo Especial")

    assert found.id == created.id
    assert found.name == created.name


def test_get_team_duplicate_name_raises_error(tmp_path):
    """Este test comprueba que se levanta un error cuando existen dos equipos
    con el mismo nombre"""

    service = make_service()
    teams_file = tmp_path / "teams.json"

    with patch("backend.app.services.team_service.TEAMS_FILE", teams_file):
        service.create_team(TeamCreate(name="Duplicado", pokemon_ids=[1]))
        service.create_team(TeamCreate(name="Duplicado", pokemon_ids=[4]))

        with pytest.raises(ValueError, match="Duplicado"):
            service.get_team("Duplicado")


def test_list_teams_uses_saved_members_if_dataset_changes(tmp_path):
    """Este test comprueba que si el dataset cambia, los miembros del equipo
    permanecen, ya que el servicio utiliza los datos almacenados"""

    teams_file = tmp_path / "teams.json"

    normal_service = make_service()

    with patch("backend.app.services.team_service.TEAMS_FILE", teams_file):
        normal_service.create_team(TeamCreate(name="Equipo", pokemon_ids=[1]))

        broken_service = TeamService(dataset_loader=lambda: [])

        teams = broken_service.list_teams()

        assert len(teams) == 1
        assert teams[0].members[0].name == "bulbasaur"


def test_update_team_more_than_6_members_raises_error(tmp_path):
    """Este test comprueba que no se puede actualizar un equipo con más
    de 6 Pokemon"""

    service = make_service()
    teams_file = tmp_path / "teams.json"

    with patch("backend.app.services.team_service.TEAMS_FILE", teams_file):
        created = service.create_team(TeamCreate(name="Original", pokemon_ids=[1]))

        payload = MagicMock()
        payload.name = "Gigante"
        payload.pokemon_ids = [1, 2, 3, 4, 5, 6, 7]

        with pytest.raises(ValueError, match="más de"):
            service.update_team(created.id, payload)
