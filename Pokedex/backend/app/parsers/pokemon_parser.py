from app.models.pokemon import PokemonDetail, PokemonBasic

def parse_pokemon(data: dict) -> PokemonDetail:

    types = [
        t['type']['name']
        for t in data.get('types', [])
    ]

    stats = {
        stat['stat']['name']: stat['base_stat']
        for stat in data.get('stats', [])
    }

    abilities = [
        a['ability']['name']
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

    return PokemonDetail(
        id=data.get('id', 0),
        name=data.get('name', " "),
        types=types,
        stats=stats,
        abilities=abilities,
        height=data.get('height', 0),
        weight=data.get('weight', 0),
        base_experience=data.get('base_experience', 0) or 0,
        sprite_url=sprite_url
    )

def parse_pokemon_basic(data: dict) -> PokemonBasic:

    types = [
        t['type']['name']
        for t in data.get('types', [])
    ]

    sprite = (
        data.get('sprites', {})
        .get('front_default', "")
    )

    return PokemonBasic(
        id=data.get('id', 0),
        name=data.get('name', 0),
        types=types,
        sprite_url=sprite
    )