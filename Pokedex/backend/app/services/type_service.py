from app.parsers.type_parser import parse_type_info

class TypeService:

    def __init__(self, client):
        self.client=client

    #Creamos una funcion que nos de la informacion de un tipo de pokemon
    def get_type_info(self, type_name):

        data = self.client.get_type(type_name)

        return parse_type_info(data)
    
    def get_damage_relations(self, type_name):

        type_info = self.get_type_info(type_name)

        return {
            'cuadruple_damage_from': type_info.cuadruple_damage_from,
            'double_damage_from': type_info.double_damage_from,
            'half_damage_from': type_info.half_damage_from,
            'one_quarter_damage_from': type_info.one_quarter_damage_from,
            'no_damage_from': type_info.no_damage_from
        }
