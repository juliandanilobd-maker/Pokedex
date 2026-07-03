from __future__ import annotations

"""
Este módulo contienela lógica del cálculo de interacciones de Pokemón de acuerdo a
sus tipos, funciona de la siguiente manera:


* Cada tipo de Pokemon tiene ciertas debilidades o resistencias, dentro del combate,
cuando un Pokemon de cierto tipo recibe daño, el daño se calcula en base al tipo del
que recibe el daño y las resistencias o debilidades que tenga frente a ese tipo

Si es resistente a ese tipo, el daño recibido es la mitad (x0.5)
Si es debil frente a ese tipo, el daño recibido es el doble (x2)
Si no es ni débil ni resistente, el daño permanece igual (x1)

Surge una situación interesante cuando existen Pokemones con tipos duales

En estas circunstancias, las debilidades o resistencias se multiplican:

* Si los dos tipos son debiles al atacante, se multiplica dos veces por 2 = x4
* Si los dos tipos son resistentes al atacante, se multiplica dos veces por 0.5 = x0.24

Y en ambas circunstancias si un tipo es inmune se multiplica por cero el daño
"""
# Optimizamos la extracción de efectividades de combate mediante la implementación
# de un diccionario con las debilidades preestablecidas, evitando llamadas a la API
INTERACTIONS_DATESET = {
    "normal": {"resist": ["ghost"], "weak": ["fighting"]},
    "fire": {
        "resist": ["fire", "grass", "ice", "bug", "steel", "fairy"],
        "weak": ["water", "ground", "rock"],
    },
    "water": {
        "resist": ["fire", "water", "ice", "steel"],
        "weak": ["grass", "electric"],
    },
    "grass": {
        "resist": ["water", "ground", "electric"],
        "weak": ["fire", "ice", "poison", "bug", "flying"],
    },
    "electric": {"resist": ["electric", "flying", "steel"], "weak": ["ground"]},
    "ice": {"resist": ["ice"], "weak": ["fire", "fighting", "rock", "steel"]},
    "fighting": {
        "resist": ["bug", "rock", "dark"],
        "weak": ["flying", "psychic", "fairy"],
    },
    "poison": {
        "resist": ["grass", "fighting", "poison", "bug", "fairy"],
        "weak": ["ground", "psychic"],
    },
    "ground": {
        "resist": ["poison", "rock"],
        "weak": ["water", "grass", "ice"],
        "immune": ["electric"],
    },
    "flying": {
        "resist": ["grass", "fighting", "bug"],
        "weak": ["electric", "ice", "rock"],
        "immune": ["ground"],
    },
    "psychic": {"resist": ["flying", "psychic"], "weak": ["bug", "ghost", "dark"]},
    "bug": {
        "resist": ["grass", "fighting", "ground"],
        "weak": ["fire", "flying", "rock"],
    },
    "rock": {
        "resist": ["normal", "fire", "poison", "flying"],
        "weak": ["water", "grass", "fighting", "ground", "steel"],
    },
    "ghost": {
        "resist": ["poison", "bug"],
        "weak": ["ghost", "dark"],
        "immune": ["normal", "fighting"],
    },
    "dragon": {
        "resist": ["fire", "water", "grass", "electric"],
        "weak": ["ice", "dragon", "fairy"],
    },
    "dark": {
        "resist": ["ghost", "dark"],
        "weak": ["fighting", "bug", "fairy"],
        "immune": ["psychic"],
    },
    "steel": {
        "resist": [
            "normal",
            "grass",
            "ice",
            "flying",
            "psychic",
            "bug",
            "rock",
            "dragon",
            "steel",
            "fairy",
        ],
        "weak": ["fire", "fighting", "ground"],
        "immune": ["poison"],
    },
    "fairy": {
        "resist": ["fighting", "bug", "dark"],
        "weak": ["poison", "steel"],
        "immune": ["dragon"],
    },
}


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

    # Calculamos los multiplicadoras de forma dinámica, combinando los tipos de Pokemon
    def _calculate_multipliers(self, types: list[str]) -> dict[str, float]:

        # Creamos una lista llamada multipliers en donde las claves
        # son los tipos de Pokemon, y les asignamos el valor por defecto 1
        multipliers = dict.fromkeys(self.POKEMON_TYPES, 1.0)

        # Iteramos en cada tipo de Pokemon de la lista de tipos obtenida de Pokemon
        for type in types:
            # Buscamos que tipo coincide y obtenemos las relaciones del diccionario
            relations = INTERACTIONS_DATESET.get(type.lower(), {})

            # sobreescribimos la lista multipliers dejando unicamente los calculados
            # a continuacion
            for weak_type in relations.get("weak", []):
                if weak_type in multipliers:
                    multipliers[weak_type] *= 2.0

            for resist_type in relations.get("resist", []):
                if resist_type in multipliers:
                    multipliers[resist_type] *= 0.5

            for immune_type in relations.get("immune", []):
                if immune_type in multipliers:
                    multipliers[immune_type] *= 0.0

        return multipliers

    # Transformamos los multiplicadores en listas estructurales
    def calculate_effectiveness(self, types: list[str]) -> dict[str, list[str]]:

        multipliers = self._calculate_multipliers(types)

        weaknesses_x4 = []
        weaknesses = []
        resistances = []
        resistances_x025 = []
        immunities = []

        for attacker_type, value in multipliers.items():
            if value == 4.0:
                weaknesses_x4.append(attacker_type)
            if value == 2.0:
                weaknesses.append(attacker_type)
            elif value == 0.5:
                resistances.append(attacker_type)
            elif value == 0.25:
                resistances_x025.append(attacker_type)
            elif value == 0.0:
                immunities.append(attacker_type)

        return {
            "weaknesses_x4": sorted(weaknesses_x4),
            "weaknesses": sorted(weaknesses),
            "resistances": sorted(resistances),
            "resistances_x025": sorted(resistances_x025),
            "immunities": sorted(immunities),
        }
