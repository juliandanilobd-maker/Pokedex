"""
En este módulo se parsea de un Pokemon obtenidos de la PokeAPI.

Tranformamos la estructura de diccionarios dinámicos en un parser que extrae datos
de forma segura y escalable.
"""

from backend.app.models.pokemon_models import FlavorText, PokemonBasic, PokemonDetail


def extract_types(data):
    """Extrae los nombres de los tipos elementales"""
    return [
        t.get("type", {}).get("name", "")
        for t in data.get("types", [])
        if t.get("type")
    ]


# Cambiamos la configuración para evitar busgs con nombres o diccionarios vacíos
def parse_pokemon(
    data: dict, flavor_text_entry: FlavorText | None = None
) -> PokemonDetail:
    """
    Transformamos la respuesta de la API en un modelo de dominio PokemonDetail

    Implementa desestructuración defensiva para prevenir fallos por diccionarios vacíos
    o campos nulos en estadisticas y sprites.
    """
    types = extract_types(data)

    stats = {
        stat.get("stat", {}).get("name", "unknown"): stat.get("base_stat", 0)
        for stat in data.get("stats", [])
        if stat.get("stat")
    }

    abilities = [
        a.get("ability", {}).get("name", "") for a in data.get("abilities", [])
    ]

    sprites = data.get("sprites", {})

    # Estrategia de fallback para imagenes sprite: priorizando la imagen oficial,
    # si no está disponible se utiliza un sprite clásico,
    sprite_url = (
        sprites.get("other", {}).get("official-artwork", {}).get("front_default")
        or sprites.get("front_default")
        or ""
    )

    sprite_shiny = (
        sprites.get("other", {}).get("official-artwork", {}).get("front_shiny")
        or sprites.get("front_shiny")
        or sprite_url
    )

    return PokemonDetail(
        id=data.get("id", 0),
        name=data.get("name", ""),
        types=types,
        stats=stats,
        abilities=abilities,
        height=data.get("height", 0),
        weight=data.get("weight", 0),
        base_experience=data.get("base_experience", 0),
        sprite_url=sprite_url,
        sprite_shiny=sprite_shiny,
        flavor_text_entry=flavor_text_entry,
    )


def parse_pokemon_basic(data: dict) -> PokemonBasic:
    """
    Transforma los datos indispensables para obtener info de manera rápida
    """
    types = extract_types(data)
    sprite = data.get("sprites", {}).get("front_default", "")

    return PokemonBasic(
        id=data.get("id", 0),
        name=data.get("name", ""),
        types=types,
        sprite_url=sprite,
    )


def parse_pokemon_description(species: dict) -> FlavorText:
    """
    Extrae y parsea la descripción del Pokemon en el idioma especificado
    """
    entries = species.get("flavor_text_entries", [])

    for entry in entries:
        language = entry.get("language", {}).get("name", "")
        # Prioriza español con fallback automático a ingles
        if language == "es":
            # Parseo y limpieza: las descripciones de la PokeAPI conservan
            # ROMs originales de GameBoy/DS y mantienen saltos de línea (\n),
            # saltos de página (\f), los cuales normalizamos.
            cleaned_text = (
                entry.get("flavor_text", "")
                .replace("\n", " ")
                .replace("\f", " ")
                .replace("\r", " ")
                .strip()
            )
            version_name = entry.get("version", {}).get("name", "Desconocida")

            return FlavorText(text=cleaned_text, language="es", version=version_name)

    for entry in entries:
        language = entry.get("language", {}).get("name", "")

        if language == "en":
            cleaned_text = (
                entry.get("flavor_text", "")
                .replace("\n", " ")
                .replace("\f", " ")
                .replace("\r", " ")
                .strip()
            )
            version_name = entry.get("version", {}).get("name", "Desconocido")

            return FlavorText(text=cleaned_text, language="en", version=version_name)

    return FlavorText(
        text="Sin descripción registrada en los archivos de la Pokedex.",
        language="es",
        version="Desconocida",
    )
