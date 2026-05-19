from __future__ import annotations

from app.parsers.type_parser import parse_type_info
from app.models.pokemon_models import TypeInfo

# Maneja la lógica de los tipos de Pokemon.
class TypeService:

    def __init__(self, client) -> None:
        self.client= client

    # Creamos una funcion que nos de la informacion de un tipo de pokemon
    # Args: nombre del tipo, ej: 'water', 'fire', 'steel'
    def get_type_info(self, type_name: str) -> TypeInfo:

        data = self.client.get_type(type_name)

        # Devuelve TypeInfo parseado y estructurado
        return parse_type_info(data)
    
    # Función para obtener las relaciones de daño
    def get_damage_relations(self, type_name: str) -> dict[str, list[str]]:
        

        type_info = self.get_type_info(type_name)


        return {
            'double_damage_from': type_info.double_damage_from,
            'half_damage_from': type_info.half_damage_from,
            'no_damage_from': type_info.no_damage_from
        }
