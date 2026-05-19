from backend.app.parsers.pokemon_parser import (
    parse_pokemon,
    parse_pokemon_basic,
    parse_pokemon_description,
)
from backend.app.parsers.type_parser import parse_type_info


def test_parse_pokemon_basic_extracts_fields() -> None:
    raw_data = {
        'id': 25,
        'name': 'pikachu',
        'types': [{'type': {'name': 'electric'}}],
        'sprites': {'front_default': 'http://example.com/pikachu.png'}
    }

    pokemon = parse_pokemon_basic(raw_data)

    assert pokemon.id == 25
    assert pokemon.name == 'pikachu'
    assert pokemon.types == ['electric']
    assert pokemon.sprite_url == 'http://example.com/pikachu.png'


def test_parse_pokemon_detail_builds_full_model() -> None:
    raw_data = {
        'id': 150,
        'name': 'mewtwo',
        'types': [{'type': {'name': 'psychic'}}],
        'stats': [
            {'stat': {'name': 'hp'}, 'base_stat': 106},
            {'stat': {'name': 'attack'}, 'base_stat': 110}
        ],
        'abilities': [{'ability': {'name': 'pressure'}}],
        'height': 20,
        'weight': 1220,
        'base_experience': 306,
        'sprites': {
            'other': {'official-artwork': {'front_default': 'http://example.com/mewtwo.png'}}
        }
    }

    pokemon = parse_pokemon(raw_data)

    assert pokemon.id == 150
    assert pokemon.stats['hp'] == 106
    assert pokemon.abilities == ['pressure']
    assert pokemon.sprite_url == 'http://example.com/mewtwo.png'


def test_parse_pokemon_description_prefers_es_or_en() -> None:
    species_data = {
        'flavor_text_entries': [
            {'flavor_text': 'Texto en español', 'language': {'name': 'es'}},
            {'flavor_text': 'English flavor text', 'language': {'name': 'en'}}
        ]
    }

    result = parse_pokemon_description(species_data)
    assert 'Texto en español' in result or 'English flavor text' in result


def test_parse_type_info_extracts_damage_relations() -> None:
    raw_data = {
        'name': 'fire',
        'damage_relations': {
            'double_damage_from': [{'name': 'water'}],
            'half_damage_from': [{'name': 'fire'}],
            'no_damage_from': [{'name': 'ground'}]
        }
    }

    type_info = parse_type_info(raw_data)

    assert type_info.name == 'fire'
    assert type_info.double_damage_from == ['water']
    assert type_info.half_damage_from == ['fire']
    assert type_info.no_damage_from == ['ground']
