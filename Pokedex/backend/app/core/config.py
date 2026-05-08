from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):

    APP_NAME: str = 'PokeDex Backend'

    APP_VERSION: str = '1.0.0'

    API_PREFIX: str = '/api/v1'

    POKEAPI_BASE_URL: str = 'https://pokeapi.co/api/v2'

    CACHE_TTL: int = 3600

    CACHE_DB_PATH: str = 'pokemon_cache.db'

    REQUEST_TIMEOUT: int = 15

    MIN_REQUEST_DELAY: float = 0.1
 
    ALLOWED_ORIGINS: List[str] = [
        'http://localhost:3000',
        'http://localhost:8501',
    ]

    class Config:
        env_file = '.venv'

settings = Settings()