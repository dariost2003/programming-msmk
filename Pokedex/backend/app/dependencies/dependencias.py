from app.cache.cache_manager import CacheManager
from app.clients.pokeapi_client import PokeAPIClient
from app.services.pokemon_service import PokemonService
from app.services.evolution_service import EvolutionService
from app.services.type_service import TypeService
from app.services.filter_service import FilterService

_cache = CacheManager()

_client = PokeAPIClient(
    cache=_cache
)

pokemon_service = PokemonService(
    client=_client
)

evolution_service = EvolutionService(
    client=_client
)

type_service = TypeService(
    client=_client
)

filter_service = FilterService(
    client=_client
)

