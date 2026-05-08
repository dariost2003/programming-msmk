"""
Modelos de datos para estructurar las respuestas de la PokeAPI.

La API devuelve JSONs grandes y complejos. Estos dataclasses extraen
solo la informacion relevante y la organizan de forma limpia.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class PokemonBasic:
    """Informacion basica de un Pokemon (para listas y busquedas)."""
    id: int
    name: str
    types: List[str]
    sprite_url: str


@dataclass
class PokemonDetail:
    """Informacion completa de un Pokemon (para vista de detalle)."""
    id: int
    name: str
    types: List[str]
    stats: Dict[str, int]  # hp, attack, defense, sp_attack, sp_defense, speed
    abilities: List[str]
    height: int        # en decimetros (dividir entre 10 para metros)
    weight: int        # en hectogramos (dividir entre 10 para kg)
    base_experience: int
    sprite_url: str


@dataclass
class TypeInfo:
    """Informacion de un tipo de Pokemon y sus relaciones de dano."""
    name: str
    double_damage_from: List[str]   # Tipos que hacen x2 dano a este tipo
    half_damage_from: List[str]     # Tipos que hacen x0.5 dano a este tipo
    no_damage_from: List[str]       # Tipos que hacen x0 dano a este tipo


@dataclass
class EvolutionStep:
    """Un paso en la cadena evolutiva de un Pokemon."""
    name: str
    level: Optional[int]     # Nivel requerido para evolucionar (puede ser None)
    method: str              # Metodo de evolucion (ej: "level-up", "trade", "use-item")


# ---------------------------------------------------------------------------
# Funciones auxiliares para parsear las respuestas crudas de la API
# ---------------------------------------------------------------------------

def parse_pokemon(api_response: dict) -> PokemonDetail:
    """
    Convierte la respuesta cruda de la PokeAPI en un PokemonDetail limpio.

    La respuesta de GET /pokemon/{name} tiene muchos campos anidados.
    Esta funcion extrae solo lo que necesitamos.

    Args:
        api_response: Diccionario con la respuesta completa de la API.

    Returns:
        PokemonDetail con los datos estructurados.

    Ejemplo de uso:
        >>> data = api_client.get_pokemon("pikachu")
        >>> pokemon = parse_pokemon(data)
        >>> print(pokemon.name)  # "pikachu"
        >>> print(pokemon.stats["attack"])  # 55
    """
    # Extraer tipos (ej: ["electric"] para Pikachu, ["fire", "flying"] para Charizard)
    types = [
        t["type"]["name"]
        for t in api_response.get("types", [])
    ]

    # Extraer estadisticas base
    # La API usa nombres como "special-attack", los mapeamos a nombres mas cortos
    stat_name_map = {
        "hp": "hp",
        "attack": "attack",
        "defense": "defense",
        "special-attack": "sp_attack",
        "special-defense": "sp_defense",
        "speed": "speed",
    }
    stats = {}
    for stat_entry in api_response.get("stats", []):
        api_name = stat_entry["stat"]["name"]
        clean_name = stat_name_map.get(api_name, api_name)
        stats[clean_name] = stat_entry["base_stat"]

    # Extraer habilidades
    abilities = [
        ab["ability"]["name"]
        for ab in api_response.get("abilities", [])
    ]

    # Extraer sprite (imagen)
    sprites = api_response.get("sprites", {})
    sprite_url = (
        sprites.get("other", {}).get("official-artwork", {}).get("front_default")
        or sprites.get("front_default")
        or ""
    )

    return PokemonDetail(
        id=api_response.get("id", 0),
        name=api_response.get("name", "desconocido"),
        types=types,
        stats=stats,
        abilities=abilities,
        height=api_response.get("height", 0),
        weight=api_response.get("weight", 0),
        base_experience=api_response.get("base_experience", 0) or 0,
        sprite_url=sprite_url,
    )


def parse_pokemon_basic(api_response: dict) -> PokemonBasic:
    """
    Convierte la respuesta cruda en un PokemonBasic (version simplificada).

    Util para listas donde no necesitas todos los detalles.

    Args:
        api_response: Diccionario con la respuesta completa de la API.

    Returns:
        PokemonBasic con id, nombre, tipos y sprite.
    """
    types = [
        t["type"]["name"]
        for t in api_response.get("types", [])
    ]

    sprites = api_response.get("sprites", {})
    sprite_url = sprites.get("front_default", "")

    return PokemonBasic(
        id=api_response.get("id", 0),
        name=api_response.get("name", "desconocido"),
        types=types,
        sprite_url=sprite_url,
    )


def parse_type_info(api_response: dict) -> TypeInfo:
    """
    Convierte la respuesta de GET /type/{name} en un TypeInfo.

    Args:
        api_response: Diccionario con la respuesta de la API para un tipo.

    Returns:
        TypeInfo con las relaciones de dano.
    """
    damage_relations = api_response.get("damage_relations", {})

    return TypeInfo(
        name=api_response.get("name", "desconocido"),
        double_damage_from=[
            t["name"] for t in damage_relations.get("double_damage_from", [])
        ],
        half_damage_from=[
            t["name"] for t in damage_relations.get("half_damage_from", [])
        ],
        no_damage_from=[
            t["name"] for t in damage_relations.get("no_damage_from", [])
        ],
    )


def parse_evolution_chain(chain_data: dict) -> List[EvolutionStep]:
    """
    Convierte la respuesta de GET /evolution-chain/{id} en una lista de pasos.

    La estructura de la API es recursiva (chain -> evolves_to -> evolves_to...),
    esta funcion la aplana en una lista simple.

    Args:
        chain_data: El campo "chain" de la respuesta de evolution-chain.

    Returns:
        Lista de EvolutionStep en orden de evolucion.
    """
    steps = []

    def _walk(node, is_first=True):
        # El primer Pokemon de la cadena no tiene requisito de evolucion
        if is_first:
            steps.append(EvolutionStep(
                name=node["species"]["name"],
                level=None,
                method="base",
            ))
        else:
            # Extraer detalles de evolucion del primer metodo disponible
            details = node.get("evolution_details", [])
            if details:
                detail = details[0]
                level = detail.get("min_level")
                trigger = detail.get("trigger", {}).get("name", "desconocido")
            else:
                level = None
                trigger = "desconocido"

            steps.append(EvolutionStep(
                name=node["species"]["name"],
                level=level,
                method=trigger,
            ))

        # Continuar con las evoluciones siguientes
        for next_evo in node.get("evolves_to", []):
            _walk(next_evo, is_first=False)

    _walk(chain_data)
    return steps
