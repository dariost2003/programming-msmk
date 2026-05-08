from app.models.pokemon import TypeInfo

def parse_type_info(data: dict) -> TypeInfo:

    relations = data.get('damage_relations', {})

    return TypeInfo(
        name=data.get('name', ""),
        cuadruple_damage_from=[
            t['name']
            for t in relations.get(
                'cuadruple_damage_from',
                []
            )
        ],
        double_damage_from=[
            t['name']
            for t in relations.get(
                'double_damage_from',
                []
            )
        ],
        half_damage_from=[
            t['name']
            for t in relations.get(
                'half_damage_from',
                []
            )
        ],
        one_quarter_damage_from=[
            t['name']
            for t in relations.get(
                'one_quarter_damage_from',
                []
            )
        ],
        no_damage_from=[
            t['name']
            for t in relations.get(
                'no_damage_from',
                []
            )
        ]
    )