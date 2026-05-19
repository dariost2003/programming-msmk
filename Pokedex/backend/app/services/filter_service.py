from __future__ import annotations

import json
from pathlib import Path
from typing import List, Dict, Optional, Any

# El servicio que usa el dataset local para aplicar los filtros de busqueda
class FilterService:

    MAX_RESULTS = 150

    def __init__(self) -> None:
        
        self.data_path = (
            Path(__file__)
            .resolve()
            .parent.parent
            /'data'
            /'datos_basicos_filtro.json'
        )

        self._pokemon_data: Optional[List[Dict[str, Any]]] = None

    # Carga de datos segura, si no carga el dataset, no falla la app
    def _load_data(self) -> List[Dict[str, Any]]:

        try:
            if not self.data_path.exists():
                print(f'[FilterService] Archivo no encontrado:' 
                      '{self.data_path}')
                return []
        
            with open(self.data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if not isinstance(data, list):
                print(f'[FilterService] El dataset no tiene formato válido')

                return []
            
            return data

        except json.JSONDecodeError:
            print(f'[FilterService] JSON corrupto en dataset')
            return []
        
        except Exception as e:
            print(f'[FilterService] Error cargando el dataset: {e}')
            return []

    # Programamos Lazy Loading para cargar de forma eficiente los datos filtrados    
    @property
    def pokemon_data(self) -> List[Dict[str, Any]]:

        if self._pokemon_data is None:
            self._pokemon_data = self._load_data()
        return self._pokemon_data

    # Recarga el dataser sin reiniciar el servidor
    def reload(self) -> None:
        self._pokemon_data = self._load_data()

    #Lógica de filtros
    def filter_pokemons(
        self,
        pokemon_type: Optional[str] | None = None,
        generation: Optional[int] | None = None,
        min_id: int = 0,
        max_id: int = 0,
        min_attack: int = 0,
        min_hp: int = 0,
        min_defense: int = 0,
        min_base_exp: int = 0
    ) -> List[Dict[str, Any]]:
        
        # Iniciamos los tipos de filtros
        filtered = self.pokemon_data

        # Normalizar los datos
        if pokemon_type:
            pokemon_type = pokemon_type.lower().strip()

        # Tipo
        if pokemon_type:
            filtered = [
                pokemon
                for pokemon in filtered
                if pokemon_type in pokemon.get('types', [])
            ]

        # Generación   
        if generation:
            filtered = [
                pokemon
                for pokemon in filtered
                if pokemon.get('generation') == generation
            ]
        #Filtros por estadísticas
        # Rango de IDs
        if min_id > 0:
            filtered = [
                pokemon
                for pokemon in filtered
                if pokemon.get('id', 0) >= min_id
            ]

        if max_id > 0:
            filtered = [
                pokemon
                for pokemon in filtered
                if pokemon.get('id', 0) <= max_id
            ]

        if min_attack > 0:
            filtered = [
                pokemon
                for pokemon in filtered
                if pokemon.get('atk', 0) >= min_attack
            ]
        
        if min_defense > 0:
            filtered = [
                pokemon
                for pokemon in filtered
                if pokemon.get('def', 0) >= min_defense
            ]
        
        if min_hp:
            filtered = [
                pokemon
                for pokemon in filtered
                if pokemon.get('hp', 0) >= min_hp
            ]
       
        if min_base_exp:
            filtered = [
                pokemon
                for pokemon in filtered
                if pokemon.get('base_exp', 0) >= min_base_exp
            ]

        return filtered[:self.MAX_RESULTS]

        
        