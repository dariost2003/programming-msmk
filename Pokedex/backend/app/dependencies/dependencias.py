from app.cache.cache_manager import CacheManager
from app.clients.pokeapi_client import PokeAPIClient

from app.services.pokemon_service import PokemonService
from app.services.evolution_service import EvolutionService
from app.services.type_service import TypeService
from app.services.filter_service import FilterService
from app.utils.stats import get_offensive_brief
cache = CacheManager()

client = PokeAPIClient(
    cache=cache
)

pokemon_service = PokemonService(
    client=client
)

evolution_service = EvolutionService(
    client=client
)

type_service = TypeService(
    client=client
)

filter_service = FilterService()



