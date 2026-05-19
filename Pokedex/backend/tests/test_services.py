from backend.app.services.pokemon_service import PokemonService
from backend.app.services.type_service import TypeService


class DummyClient:
    def get_pokemon(self, identifier: str) -> dict:
        return {
            'id': 25,
            'name': 'pikachu',
            'types': [{'type': {'name': 'electric'}}],
            'stats': [{'stat': {'name': 'hp'}, 'base_stat': 35}],
            'abilities': [{'ability': {'name': 'static'}}],
            'height': 4,
            'weight': 60,
            'base_experience': 112,
            'sprites': {'other': {'official-artwork': {'front_default': 'http://example.com/pikachu.png'}}, 'front_default': 'http://example.com/pikachu_front.png'}
        }

    def get_type(self, type_name: str) -> dict:
        return {
            'name': type_name,
            'damage_relations': {
                'double_damage_from': [{'name': 'ground'}],
                'half_damage_from': [{'name': 'electric'}],
                'no_damage_from': []
            }
        }


def test_pokemon_service_returns_detail_model() -> None:
    service = PokemonService(client=DummyClient())
    pokemon = service.get_pokemon_detail('pikachu')

    assert pokemon.name == 'pikachu'
    assert pokemon.stats['hp'] == 35
    assert pokemon.sprite_url == 'http://example.com/pikachu.png'


def test_type_service_returns_type_info() -> None:
    service = TypeService(client=DummyClient())
    type_info = service.get_type_info('electric')

    assert type_info.name == 'electric'
    assert type_info.double_damage_from == ['ground']
    assert type_info.half_damage_from == ['electric']
