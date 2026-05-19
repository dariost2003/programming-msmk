from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class PokemonBasic:
    id: int
    name: str
    types: List[str]
    sprite_url: str

@dataclass
class PokemonDetail:
    id: int
    name: str
    types: List[str]
    stats: Dict[str, int]
    abilities: List[str]
    height: int
    weight: int
    base_experience: int
    sprite_url: str
    sprite_shiny: Optional[str] = None

@dataclass
class TypeInfo:
    name: str
    double_damage_from: List[str]
    half_damage_from: List[str]
    no_damage_from: List[str] 

@dataclass
class EvolutionNode:
    name: str
    children: List[EvolutionNode] = field(default_factory=list)
    evolution_details: Optional[dict] = None
    