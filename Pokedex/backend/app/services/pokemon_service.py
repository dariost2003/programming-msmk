from app.parsers.pokemon_parser import (
    parse_pokemon,
    parse_pokemon_basic
)
class PokemonService:

    def __init__(self, client):
        self.client = client

    def get_pokemon_detail(self, identifier):
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

    #Creamos un pokemon para obtener una version resumida y mas simple de la info    
    def get_pokemon_basic(self, identifier):
        
        data = self.client.get_pokemon(identifier)
        return parse_pokemon_basic(data)
    
    #Creamos una nueva funcion que nos sirve para obtener los datos de la especie
    def get_pokemon_species(self, identifier):

        return self.client,self.get_species(identifier)
    
    #Creamos una funcion que nos permita obtener el flavor text de un pokemon
    def get_pokemon_description(self, identifier):

        species = self.client.get_species(identifier)
        entries = species.get('flavor_text_entries', [])

        for entry in entries:

            language = entry['language']['name']

            if language in ['es', 'en']:

                return (
                    entry['flavor_text']
                    .replace('\n', ' ')
                    .replace('\f', ' ')
                    .replace('\r', ' ')
                )
        
        return 'Descripcion no disponible'
    
    #Creamos una funcion que nos devuelva una lista de pokemones

    def get_pokemon_list(self, limit=20, offset=0):

        return self.client.get_pokemon_list(
            limit=limit,
            offset=offset
        )

        
    