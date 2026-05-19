from backend.app.clients.pokeapi_client import PokeAPIClient


class DummyCache:
    def __init__(self):
        self.storage = {}

    def get(self, key: str):
        return self.storage.get(key)

    def set(self, key: str, value, ttl=None):
        self.storage[key] = value


def test_normalize_identifier_lowercases_and_trims() -> None:
    client = PokeAPIClient(cache=DummyCache())
    assert client.normalize_identifier('  PikAChu  ') == 'pikachu'


def test_build_url_builds_relative_endpoints() -> None:
    client = PokeAPIClient(cache=DummyCache())
    url = client._build_url('pokemon/25')
    assert url.endswith('/pokemon/25')
    assert 'pokeapi.co' in url


def test_build_url_accepts_same_base_absolute_urls() -> None:
    client = PokeAPIClient(cache=DummyCache())
    allowed_url = f'{client.base_url}/pokemon/1'
    assert client._build_url(allowed_url) == allowed_url


def test_build_url_rejects_external_urls() -> None:
    client = PokeAPIClient(cache=DummyCache())
    try:
        client._build_url('https://example.com/')
    except ValueError as exc:
        assert 'URL externa no permitida' in str(exc)
    else:
        raise AssertionError('Se esperaba ValueError para URL externa')
