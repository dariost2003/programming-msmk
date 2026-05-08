from fastapi import APIRouter, HTTPException

from app.dependencies.dependencias import (pokemon_service, evolution_service, type_service, filter_service) 


router = APIRouter(prefix='/api/v1')

# Endpoint Pokemon
@router.get('/pokemon/{identifier}')
async def get_pokemon(identifier: str):

    try:
        return pokemon_service.get_pokemon_detail(identifier)
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    

# Endpoint Evolution
@router.get('/pokemons/{identifier}/evolution')
async def get_evolution_chain(identifier: str):

    try:
        return evolution_service.get_evolution_tree(identifier)
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    

# Endpoint Tipos
@router.get('/types/{type_name}')
async def get_type(type_name: str):

    try:
        return type_service.get_type_info(type_name)
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=(e))
    

# Endpoint Filtros
@router.get('/pokemon/filter')
async def filter_pokemons(
    type: str | None=None,
    generation: int | None=None,
    min_attack: int=0,
    min_hp: int=0,
    min_defense: int=0,
    min_base_exp: int=0
):
    
    return filter_service.filter_pokemons(
        pokemon_type=type,
        generation=generation,
        min_attack=min_attack,
        min_hp=min_hp,
        min_defense=min_defense,
        min_base_exp=min_base_exp
    )