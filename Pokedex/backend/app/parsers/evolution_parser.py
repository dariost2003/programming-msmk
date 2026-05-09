from app.models.pokemon import EvolutionNode

def parse_evolution_chain(node):

    evolution = {
        'name': node['species']['name'],
        'children': []}

    evolves_to = node.get('evolves_to', [])

    for evo in evolves_to:

        child = parse_evolution_chain(evo)

        details = evo.get('evolution_details', [])

        if details:

            d = details[0]

            child['requirements'] = {
                'min_level': d.get('min_level'),
                'item': (d.get('item', {}).get('name')
                        if d.get('item')
                        else None
                        ),
                'trigger': (d.get('trigger', {}).get('name')
                            if d.get('trigger')
                            else None
                        ),
                'min_happiness': d.get('min_happiness'),
                'time_of_day': d.get('time_of_day')            
            }
        
        evolution['children'].append(child)

    return evolution
        