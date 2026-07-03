"""Este módulo contiene el servicio de dominio encargado del CRUD de equipos Pokemon
No llama a la PokeAPI, resuelve los datos de cada Pokemon, utilizando el dataset local
generado con nuestro srcipt ETL, evitando peticiones a la red y garantizando mayor
velocidad en respuesta

Los datos persisten en: data/teams.json (lista de equipos)
"""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

from backend.app.models.pokemon_models import Team, TeamCreate, TeamMember, TeamStats

TEAMS_FILE = Path(__file__).resolve().parents[1] / "data" / "teams.json"
TEAM_MAX_SIZE = 6


class TeamService:
    """Esta clase encapsula el CRUD de equipos y el cálculo de sus stats agregadas"""

    def __init__(self, dataset_loader) -> None:
        # Usamos dataset_loader para inyectar la funcion load_dataset del script ETL
        self._dataset_loader = dataset_loader

    # Cargamos el dataset
    def _load_pokemon_index(self) -> dict[int, dict]:

        dataset = self._dataset_loader()
        return {entry["id"]: entry for entry in dataset}

    def _resolve_members(self, pokemon_ids: list[int]) -> list[TeamMember]:
        index = self._load_pokemon_index()
        members: list[TeamMember] = []

        for id in pokemon_ids:
            entry = index.get(id)

            if entry is None:
                raise ValueError(
                    f"No se encontró el Pokemon con ID {id} en el dataset local"
                    "Verifica que el ETL se haya ejecutado correctamente"
                )

            members.append(
                TeamMember(
                    id=entry["id"],
                    name=entry["name"],
                    types=entry["types"],
                    hp=entry["hp"],
                    attack=entry["attack"],
                    defense=entry["defense"],
                    speed=entry["speed"],
                    sprite_url=entry.get("sprite_url", ""),
                )
            )

        return members

    # Calcula las estadísticas agregadas de un equipo
    def _calcuate_stats(self, members: list[TeamMember]) -> TeamStats:

        n = len(members)

        total_hp = sum(m.hp for m in members)
        total_attack = sum(m.attack for m in members)
        total_defense = sum(m.defense for m in members)
        total_speed = sum(m.speed for m in members)

        # Establecemos la cobertura por tipos de acuerdo a todos los tipos en el equipo
        type_coverage = sorted({t for m in members for t in m.types})

        return TeamStats(
            total_hp=total_hp,
            total_attack=total_attack,
            total_defense=total_defense,
            total_speed=total_speed,
            avg_hp=round(total_hp / n, 2),
            avg_attack=round(total_attack / n, 2),
            avg_defense=round(total_defense / n, 2),
            avg_speed=round(total_speed / n, 2),
            type_coverage=type_coverage,
        )

    def _read_all_teams(self) -> list[dict]:
        if not TEAMS_FILE.exists():
            return []

        try:
            with open(TEAMS_FILE, encoding="utf-8") as f:
                return json.load(f)

        except (json.JSONDecodeError, OSError):
            return []

    def _write_all_teams(self, teams: list[dict]) -> None:
        TEAMS_FILE.parent.mkdir(parents=True, exist_ok=True)

        with open(TEAMS_FILE, "w", encoding="utf-8") as f:
            json.dump(teams, f, indent=2, ensure_ascii=False)

    def _resolve_team_id(self, identifier: str) -> str:

        teams = self._read_all_teams()

        for raw in teams:
            if raw["id"] == identifier:
                return raw["id"]

        matches = [raw for raw in teams if raw["name"].lower() == identifier.lower()]

        if len(matches) == 1:
            return matches[0]["id"]

        if len(matches) > 1:
            raise ValueError(
                f"Existen: '{len(matches)} equipos con el nombre {identifier}'"
            )

        raise ValueError(f"No se encontró ningún equipo llamado: '{identifier}'")

    # OPERACIONES CRUD
    def create_team(self, payload: TeamCreate) -> Team:

        if len(payload.pokemon_ids) > TEAM_MAX_SIZE:
            raise ValueError(
                f"Un equipo no puede tener más de {TEAM_MAX_SIZE} Pokemon"
                f"(se recibieron {len(payload.pokemon_ids)})"
            )

        members = self._resolve_members(payload.pokemon_ids)
        stats = self._calcuate_stats(members)

        team = Team(
            id=str(uuid.uuid4()),
            name=payload.name,
            members=members,
            stats=stats,
            created_at=datetime.now(timezone.utc).isoformat(),
        )

        teams = self._read_all_teams()
        teams.append(json.loads(team.model_dump_json()))
        self._write_all_teams(teams)

        return team

    def list_teams(self) -> list[Team]:

        teams_raw = self._read_all_teams()
        result: list[Team] = []

        for raw in teams_raw:
            # Recalculamos las stats, en caso de que existan cambios en el dataset
            pokemons_ids = [m["id"] for m in raw["members"]]

            try:
                members = self._resolve_members(pokemons_ids)
                stats = self._calcuate_stats(members)

            except ValueError:
                members = [TeamMember(**m) for m in raw["members"]]
                stats = TeamStats(**raw["stats"])

            result.append(
                Team(
                    id=raw["id"],
                    name=raw["name"],
                    members=members,
                    stats=stats,
                    created_at=raw["created_at"],
                )
            )

        return result

    def get_team(self, team_id: str) -> Team:

        real_id = self._resolve_team_id(team_id)

        for team in self.list_teams():
            if team.id == real_id:
                return team

        raise ValueError(f"No se encontró ningún equipo con ID '{real_id}'.")

    def update_team(self, team_id: str, payload: TeamCreate) -> Team:

        if len(payload.pokemon_ids) > TEAM_MAX_SIZE:
            raise ValueError(
                f"Un equipo no puede tener más de {TEAM_MAX_SIZE} Pokemon"
                f"Se recibieron {len(payload.pokemon_ids)}."
            )

        real_id = self._resolve_team_id(team_id)

        teams = self._read_all_teams()
        index = next((i for i, t in enumerate(teams) if t["id"] == real_id), None)

        if index is None:
            raise ValueError(f"No se encontró ningún equipo con ID '{real_id}'")

        members = self._resolve_members(payload.pokemon_ids)
        stats = self._calcuate_stats(members)

        update_team = Team(
            id=team_id,
            name=payload.name,
            members=members,
            stats=stats,
            created_at=teams[index]["created_at"],
        )

        teams[index] = json.loads(update_team.model_dump_json())
        self._write_all_teams(teams)

        return update_team

    def delete_team(self, team_id: str) -> None:

        real_id = self._resolve_team_id(team_id)

        teams = self._read_all_teams()
        filtered = [t for t in teams if t["id"] != real_id]

        if len(filtered) == len(teams):
            raise ValueError(f"No se encontró ningún equipo con ID '{team_id}'.")

        self._write_all_teams(filtered)
