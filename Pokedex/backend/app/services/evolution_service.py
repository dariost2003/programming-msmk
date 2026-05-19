from app.parsers.evolution_parser import parse_evolution_tree

class EvolutionService:

    
    def __init__(self, client):
        self.client = client

    #Creamos una funcion que nos de la cadena evolutiva en forma de arbol
    def get_evolution_tree(self, identifier: str):

        species_data = self.client.get_species(identifier)

        evo_url = (
            species_data
            .get('evolution_chain', {})
            .get('url')
        )

        if not evo_url:
            return None
        
        evolution_data = self.client.get(evo_url)

        return parse_evolution_tree(evolution_data['chain'])

