import requests
from backend.app.core.constants import POKEAPI_BASE_URL

class BackendClient:

    BASE_URL = POKEAPI_BASE_URL
    
    def get_pokemon(self, identifier: str):

        res = requests.get(f'{self.BASE_URL}/pokemons/{identifier}')

        res.raise_for_status()

        return res.json()

    def get_evolution(self, identifier: str):

        res = requests.get(f'{self.BASE_URL}/pokemons/{identifier}/evolution')

        res.raise_for_status()

        return res.json()
    
    def filter_pokemons(self, **params):

        res = requests.get(f'{self.BASE_URL}/pokemons/filter', params=params)

        res.raise_for_status()

        return res.json()
    