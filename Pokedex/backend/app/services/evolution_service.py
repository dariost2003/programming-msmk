class EvolutionService:
    
    def __init__(self, client):
        self.client = client

    #Creamos una funcion que nos de la cadena evolutiva en forma de arbol
    def get_evolution_tree(self, identifier):

        species_data = self.client.get_species(identifier)

        evo_url = species_data['evolution_chain']['url']

        evolution_data = self.client.get(evo_url)

        chain = evolution_data['chain']

        return self._build_tree('chain')

    #Limpia el arbol dado desde la PokeAPI    
    def _build_tree(self, node):

        result = {
            'name': node['species']['name'],
            'children': [],
            'evolution_details': []
        }

        evolves_to=node.get('evolves_to', [])
                
        for evolution in evolves_to:

            evolution_node = self._build_tree(
                evolution
            )

            details = evolution.get('evolution_details', [])

            if details:

                detail = details[0]

                evolution_node['evolution_details'] = {
                    'min_level': detail.get('min_level'), 
                    'item':(detail.get('item', {}).get('name')
                        if detail.get('item')
                        else None),
                    'trigger':(detail.get('trigger', {}).get('name')
                        if detail.get('trigger')
                        else None),
                    'time_of_day': detail.get('time_of_day'),
                    'min_happiness': detail.get('min_happiness')
                }
            
            
            result['children'].append(evolution_node)
            
        return result