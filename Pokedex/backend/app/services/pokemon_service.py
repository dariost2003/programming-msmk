from __future__ import annotations

from app.models.pokemon_models import (
    PokemonBasic,
    PokemonDetail
)

from app.parsers.pokemon_parser import (
    parse_pokemon,
    parse_pokemon_basic,
    parse_pokemon_description
)

# Se encarga de la lógica de negocio de Pokemon
class PokemonService:

    def __init__(self, client) -> None:
        self.client = client

    def get_pokemon_detail(self, identifier: str) -> PokemonDetail:
        """
        Obtiene los datos completos de un Pokemon.

        Args:
            identifier: Nombre (str) o ID (int) del Pokemon, usando el arg 
                        identifier, podremos realizar nuestra busqueda por cualquiera
                        de estos parametros.
                        Ej: "pikachu", "charizard", 25, 6

        Returns:
            Diccionario con todos los datos del Pokemon.
            Usa models.parse_pokemon() para convertirlo a PokemonDetail.
        """
        data = self.client.get_pokemon(identifier)
        #identifier= para poder nombrar en nuestra pokedex ya sea name or id
        return parse_pokemon(data)

    # Obtenemos una version resumida y mas simple de la info    
    def get_pokemon_basic(self, identifier) -> PokemonBasic:
        
        data = self.client.get_pokemon(identifier)
        return parse_pokemon_basic(data)
    
    # Creamos una nueva funcion que nos sirve para obtener los datos de la especie
    def get_pokemon_species(self, identifier: str) -> dict:

        return self.client.get_species(identifier)
    
    # Creamos una funcion que nos permita obtener el flavor text de un pokemon
    def get_pokemon_description(self, identifier: str) -> str:

        species = self.client.get_species(identifier)
                
        return parse_pokemon_description(species)
    
    # Creamos una funcion que nos devuelva una lista de pokemones
    def get_pokemon_list(self, limit=20, offset=0) -> dict:

        return self.client.get_pokemon_list(
            limit=limit,
            offset=offset
        )

        
    