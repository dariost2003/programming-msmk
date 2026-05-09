import json
from pathlib import Path

class FilterService:

    def __init__(self):
        
        self.data_path = (
            Path(__file__)
            .resolve()
            .parent.parent
            /'data'
            /'datos_basicos_filtro.json'
        )

        self.pokemon_data = self._load_data()

    def _load_data(self):

        with open(self.data_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def filter_pokemons(
        self,
        pokemon_type: str | None = None,
        generation: int | None = None,
        min_attack: int = 0,
        min_hp: int = 0,
        min_defense: int = 0,
        min_base_exp: int = 0
    ):
        
        filtered = self.pokemon_data

        
        if pokemon_type:
            filtered = [
                p for p in filtered
                if pokemon_type in p['types']
            ]
            
        if generation:
            filtered = [
                p for p in filtered
                if p['generation'] != generation
            ]
                       
          
        if min_attack:
            filtered = [
                p for p in filtered
                if p['atk'] >= min_attack
            ]
        
        if min_defense:
            filtered = [
                p for p in filtered
                if p['defense'] >= min_defense
            ]
        
        if min_hp:
            filtered = [
                p for p in filtered
                if p['hp'] >= min_hp
            ]
       
        if min_base_exp:
            filtered = [
                p for p in filtered
                if p['base_exp'] >= min_base_exp
            ]
            

        return filtered[:150]

        
        