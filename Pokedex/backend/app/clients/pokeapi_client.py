"""
Este modulo proporciona una clase que encapsula las peticiones HTTP a la API,
maneja errores, implementa rate limiting basico y utiliza cache para evitar
peticiones repetidas.
"""

import time
import requests

from app.core.config import Settings
from app.core.constants import MIN_REQUEST_DELAY

class PokeAPIClient:
    """
    Cliente para interactuar con la PokeAPI.

    Caracteristicas:
    - Cache automatico de respuestas (SQLite)
    - Rate limiting basico (pausa entre peticiones)
    - Manejo de errores HTTP
    """

    def __init__(self, cache):
       
        self.base_url = Settings.POKEAPI_BASE_URL
        self.cache = cache
        self._last_request_time = 0  # minimo entre peticiones

    
    #A continuacion viene la base de las peticiones http
    def get(self, endpoint: str):
        """
        Hace una peticion GET a la API con cache y rate limiting.

        Args:
            endpoint: Ruta relativa al base_url (ej: "pokemon/pikachu").

        Returns:
            Diccionario con la respuesta JSON de la API.

        Raises:
            requests.exceptions.HTTPError: Si la API responde con error (404, 500, etc.)
            requests.exceptions.ConnectionError: Si no hay conexion a internet.
            requests.exceptions.Timeout: Si la peticion tarda demasiado.
        """
        
        url = self._build_url(endpoint)

        #Primero intenta obtener del cache
        cached = self.cache.get(url)
        if cached is not None:
            return cached
        
        #Usamos rate limit
        self._rate_limit()

        #Se realiza la peticion
        try:
            res = requests.get(url, timeout=15)
            res.raise_for_status()
            data = res.json()

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                raise ValueError(
                    f"No se encontro el recurso: {endpoint}. "
                    "Verifica que el nombre o ID sea correcto."
                ) from e
            raise
        except requests.exceptions.ConnectionError:
            raise ConnectionError(
                "No se pudo conectar a la PokeAPI. "
                "Verifica tu conexion a internet."
            )
        except requests.exceptions.Timeout:
            raise TimeoutError(
                "La peticion a la PokeAPI tardo demasiado. "
                "Intenta de nuevo en unos momentos."
            )

        #Establecemos un update state
        self._last_request_time = time.time()

        #Guardamos en la cache para futuras consultas
        self.cache.set(url, data)

        return data

    #Creamos una funcion que nos permita construir la URL
    def _build_url(self, endpoint: str):

        if endpoint.startswith('http'):

         
            #Añadimos raise ValueError para evitar URLs externas   
            if not endpoint.startswith(self.base_url):
                raise ValueError("URL externa no permitida")
            
            return endpoint
        
        # Construir URL completa    
        url = f"{self.base_url + endpoint.strip('/')}"
        return url
      
    #Establecemos la funcion que limita el numero de peticiones
    def _rate_limit(self):

        elapsed = time.time() - self._last_request_time
        if elapsed < MIN_REQUEST_DELAY:

            time.sleep(MIN_REQUEST_DELAY - elapsed)

    #A continuacion definimos funciones que nos entreguen los pokemones,
    #listas, especies, etc que ya solicitamos de manera limpia
    
    #Volvemos a identifier a minusculas y elimina los espacios en blanco 
    def normalize_identifier(self, value):
        return str(value).lower().strip()
    
    #Toma el identifier corregido y lo añade al endpoint para buscar un 
    #pokemon en especifico.
    def get_pokemon(self, identifier):
        normalized = self.normalize_identifier(identifier)
        return self.get(f"pokemon/{normalized}")
    
    def get_pokemon_list(self, limit=20, offset=0):

        return self.get(f'pokemon?limit={limit}%offset={offset}')

    def get_species(self, identifier):

        normalized = self.normalize_identifier(identifier)
        return self.get(f'pokemon-species/{normalized}')
    
    def get_type(self, type_name):

        normalized= self.normalize_identifier(type_name)
        return self.get(f'type_name/{normalized}')
    
    def get_evolution_chain(self, chain_id):

        return self.get(f'evolution-chain/{chain_id}')
