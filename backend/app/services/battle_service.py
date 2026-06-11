from __future__ import annotations

from backend.app.services.type_service import TypeService


class BattleService:
    POKEMON_TYPES: tuple[str, ...] = (
        "normal",
        "fire",
        "water",
        "grass",
        "electric",
        "ice",
        "fighting",
        "poison",
        "ground",
        "flying",
        "psychic",
        "bug",
        "rock",
        "ghost",
        "dragon",
        "dark",
        "steel",
        "fairy",
    )

    def __init__(self, type_service: TypeService) -> None:
        self.type_service = type_service

    # Calculamos los multiplicadoras de forma dinámica, combinando los tipos de Pokemon
    def _calculate_multipliers(self, types: list[str]) -> dict[str, float]:

        multipliers = dict.fromkeys(self.POKEMON_TYPES, 1.0)

        for type in types:
            relations = self.type_service.get_damage_relations(type)

            for weak_type in relations.get("double_damage_from", []):
                if weak_type in multipliers:
                    multipliers[weak_type] *= 2.0

            for resist_type in relations.get("half_damage_from", []):
                if resist_type in multipliers:
                    multipliers[resist_type] *= 0.5

            for immune_type in relations.get("no_damage_from", []):
                if immune_type in multipliers:
                    multipliers[immune_type] *= 0.0

        return multipliers

    # Transformamos los multiplicadores en listas estructurales
    def calculate_effectiveness(self, types: list[str]) -> dict[str, list[str]]:

        multipliers = self._calculate_multipliers(types)

        weaknesses = []
        resistances = []
        immunities = []

        for attacker_type, value in multipliers.items():
            if value > 1.0:
                weaknesses.append(attacker_type)
            elif 0.0 < value < 1.0:
                resistances.append(attacker_type)
            elif value == 0.0:
                immunities.append(attacker_type)

        return {
            "weaknesses": sorted(weaknesses),
            "resistances": sorted(resistances),
            "immunities": sorted(immunities),
        }
