from app.models.pokemon import EvolutionNode

def parse_evolution_chain(node: dict) -> EvolutionNode:

    name = node['species']['name']

    children = [
        parse_evolution_chain(child)
        for child in node.get('evolves_to', [])
    ]

    details = None

    if node.get('evolution-details'):

        d= node['evolution_details'][0]

        details = {
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

    return EvolutionNode(
        name=name,
        children=children,
        evolution_details=details
    )