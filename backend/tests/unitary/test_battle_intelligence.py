from backend.app.services.battle_service import BattleService


def test_battle_intelligence_dual_type():
    """Este test comprueba la obtención correcta de los valores de efectividad en
    combate"""
    battle_service = BattleService()

    result = battle_service.calculate_effectiveness(["fire", "flying"])

    assert "ground" in result["immunities"]
    assert "rock" in result["weaknesses_x4"]
    assert "water" in result["weaknesses"]
    assert "electric" in result["weaknesses"]
    assert "fighting" in result["resistances"]
    assert "fire" in result["resistances"]
    assert "fairy" in result["resistances"]
    assert "steel" in result["resistances"]
    assert "bug" in result["resistances_x025"]
    assert "grass" in result["resistances_x025"]
