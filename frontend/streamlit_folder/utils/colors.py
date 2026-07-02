POKEMON_TYPE_COLORS: dict[str, str] = {
    "fire": "#ff421c",
    "water": "#2c9be3",
    "grass": "#78cc55",
    "electric": "#ffd333",
    "ice": "#7ac7ff",
    "fighting": "#bb5544",
    "poison": "#aa5599",
    "ground": "#ddbb55",
    "flying": "#8899ff",
    "psychic": "#ff5599",
    "bug": "#aabb22",
    "rock": "#bbaa66",
    "ghost": "#6666bb",
    "dragon": "#7766ee",
    "dark": "#775544",
    "steel": "#aaaabb",
    "fairy": "#ee99ee",
    "normal": "#aaaa99",
}


def get_type_color(type_name: str) -> str:
    return POKEMON_TYPE_COLORS.get(type_name.lower(), "#A8A878")


def hexadecimal_to_rgba(hex_color: str, alpha: float) -> str:
    cleaned = hex_color.strip().lstrip("#")
    if len(cleaned) != 6:
        raise ValueError("El color hexadecimal debe tener 6 caracteres")

    r, g, b = (int(cleaned[i : i + 2], 16) for i in (0, 2, 4))
    return f"rgba({r}, {g}, {b}, {alpha})"
