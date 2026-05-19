from app.models.pokemon_models import TypeInfo


def parse_type_info(data: dict) -> TypeInfo:

    relations = data.get('damage_relations', {})

    return TypeInfo(
        name=data.get('name', ""),
        double_damage_from=[
            t.get('name', "")
            for t in relations.get(
                'double_damage_from',
                []
            )
        ],
        half_damage_from=[
            t.get('name', "")
            for t in relations.get(
                'half_damage_from',
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