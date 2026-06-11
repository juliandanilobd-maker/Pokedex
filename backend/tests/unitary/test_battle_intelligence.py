from unittest.mock import MagicMock

import pytest

from backend.app.services.battle_service import BattleService


@pytest.fixture
def mock_type_service():
    return MagicMock()


@pytest.fixture
def battle_service(mock_type_service):
    return BattleService(type_service=mock_type_service)


# Comprobamos el cálculo de estadisticas para un tipo dual
def test_battle_intelligence_dual_type(battle_service, mock_type_service):

    def side_effect(type_name):

        if type_name == "fire":
            return {
                "double_damage_from": ["water", "ground", "rock"],
                "half_damage_from": ["fire", "grass", "ice", "bug", "steel", "fairy"],
                "no_damage_from": [],
            }

        if type_name == "flying":
            return {
                "double_damage_from": ["electric", "ice", "rock"],
                "half_damage_from": ["grass", "fighting", "bug"],
                "no_damage_from": ["ground"],
            }

        return {"double_damage_from": [], "half_damage_from": [], "no_damage_from": []}

    mock_type_service.get_damage_relations.side_effect = side_effect

    result = battle_service.calculate_effectiveness(["fire", "flying"])

    assert "ground" in result["immunities"]
    assert "rock" in result["weaknesses"]
    assert "water" in result["weaknesses"]
    assert "ice" not in result["weaknesses"]
    assert "ice" not in result["resistances"]
