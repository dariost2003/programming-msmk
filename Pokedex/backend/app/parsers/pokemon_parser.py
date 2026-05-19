from app.models.pokemon_models import PokemonDetail, PokemonBasic

def extract_types(data):
    types = [
        t.get('type', {}).get('name', {})
        for t in data.get('types', [])
    ]
    return types

def parse_pokemon(data: dict) -> PokemonDetail:

    types = extract_types(data)

    stats = {
        stat['stat']['name']: stat.get('base_stat', 0)
        for stat in data.get('stats', [])
    }

    abilities = [
        a.get('ability', {}).get('name', "")
        for a in data.get('abilities', [])
    ]

    sprites = data.get('sprites', {})

    sprite_url = (
        sprites.get('other', {})
        .get('official-artwork', {})
        .get('front_default')
        or sprites.get('front_default')
        or ""
    )

    sprite_shiny = (
        sprites.get('other', {})
        .get('official-artwork', {})
        .get('front_shiny')
        or sprites.get('front_shiny')
        or sprite_url
    )

    return PokemonDetail(
        id=data.get('id', 0),
        name=data.get('name', ""),
        types=types,
        stats=stats,
        abilities=abilities,
        height=data.get('height', 0),
        weight=data.get('weight', 0),
        base_experience=data.get('base_experience', 0),
        sprite_url=sprite_url,
        sprite_shiny=sprite_shiny
    )

def parse_pokemon_basic(data: dict) -> PokemonBasic:
    
    types = extract_types(data)

    sprite = (
        data.get('sprites', {})
        .get('front_default', "")
    )

    return PokemonBasic(
        id=data.get('id', 0),
        name=data.get('name', ""),
        types=types,
        sprite_url=sprite
    )

def parse_pokemon_description(species: dict) -> str:
    
    entries = species.get('flavor_text_entries', [])

    for entry in entries:

        language = entry.get('language', {}).get('name') in ('es', 'en')
        
        if language:
            return (
                entry.get('flavor_text', "")
                .replace('\n', ' ')
                .replace('\f', ' ')
                .replace('\r', ' ')
                .strip()
            )
    return ""