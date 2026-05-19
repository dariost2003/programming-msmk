from fastapi import APIRouter, HTTPException, Query

from app.core.config import settings
from app.dependencies.dependencias import (
    pokemon_service,
    evolution_service,
    type_service,
    filter_service
)
from dataclasses import asdict
from app.utils.stats import get_offensive_brief


router = APIRouter(prefix=settings.API_PREFIX)

# Endpoint Filtros (registrado antes de la ruta dinámica)
@router.get('/pokemon/filter')
async def filter_pokemons(
    pokemon_type: str | None = Query(None),
    generation: int | None = Query(None),
    min_id: int = Query(0),
    max_id: int = Query(0),
    min_attack: int = Query(0),
    min_hp: int = Query(0),
    min_defense: int = Query(0),
    min_base_exp: int = Query(0)
):
    
    return filter_service.filter_pokemons(
        pokemon_type=pokemon_type,
        generation=generation,
        min_id=min_id,
        max_id=max_id,
        min_attack=min_attack,
        min_hp=min_hp,
        min_defense=min_defense,
        min_base_exp=min_base_exp
    )


# Endpoint Tipos
@router.get('/types/{type_name}')
async def get_type(type_name: str):

    try:
        return type_service.get_type_info(type_name)
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    

# Endpoint Evolution
@router.get('/pokemon/{identifier}/evolution')
async def get_evolution_chain(identifier: str):

    try:
        node = evolution_service.get_evolution_tree(identifier)
        # Convierte un dataclass en un dict, para poder extraer todos los datos de un diccionario
        return asdict(node) if node is not None else None
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get('/pokemon/{identifier}/effectiveness')
async def get_combat_effectiveness(identifier: str):

    try:
        pokemon = pokemon_service.get_pokemon_detail(identifier)

        types = pokemon.types

        return get_offensive_brief(types)
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    
@router.get('/pokemon/{identifier}/flavor_text')
async def get_flavor_text(identifier: str):

    try:
        flavor_text = pokemon_service.get_pokemon_description(identifier)
        return {'flavor_text': flavor_text}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Endpoint Pokemon (ruta genérica debe quedar al final)
@router.get('/pokemon/{identifier}')
async def get_pokemon(identifier: str):

    try:
        return pokemon_service.get_pokemon_detail(identifier)
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
