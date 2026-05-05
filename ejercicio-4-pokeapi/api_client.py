"""
Cliente para la PokeAPI (https://pokeapi.co/api/v2/).

Este modulo proporciona una clase que encapsula las peticiones HTTP a la API,
maneja errores, implementa rate limiting basico y utiliza cache para evitar
peticiones repetidas.
"""

import time
import requests
from cache import CacheManager


class PokeAPIClient:
    """
    Cliente para interactuar con la PokeAPI.

    Caracteristicas:
    - Cache automatico de respuestas (SQLite)
    - Rate limiting basico (pausa entre peticiones)
    - Manejo de errores HTTP
    """

    def __init__(self, cache_ttl: int = 3600):
        """
        Inicializa el cliente.

        Args:
            cache_ttl: Tiempo de vida del cache en segundos (defecto: 1 hora).
        """
        self.base_url = "https://pokeapi.co/api/v2/"
        self.cache = CacheManager()
        self.cache_ttl = cache_ttl
        self._last_request_time = 0.0
        self._min_delay = 0.1  # 100ms minimo entre peticiones

    def get(self, endpoint: str) -> dict:
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
        #Añadir una funcion que acepte URLs completas

        if endpoint.startswith('http'):
            url = endpoint
        else:             
        # Construir URL completa
            url = self.base_url + endpoint.strip("/")
        
        #Añadimos raise ValueError para evitar URLs externas
        if endpoint.startswith('http') and not endpoint.startswith(self.base_url):
            raise ValueError("URL externa no permitida")
        # Intentar obtener del cache primero
        cached = self.cache.get(url)
        if cached is not None:
            return cached

        # Rate limiting: esperar si la ultima peticion fue muy reciente
        elapsed = time.time() - self._last_request_time
        if elapsed < self._min_delay:
            time.sleep(self._min_delay - elapsed)

        # Hacer la peticion real
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            data = response.json()
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

        self._last_request_time = time.time()

        # Guardar en cache para futuras consultas
        self.cache.set(url, data, ttl=self.cache_ttl)

        return data

    # -------------------------------------------------------------------
    # Metodos especificos para cada recurso de la API
    # -------------------------------------------------------------------

    def get_pokemon(self, name_or_id) -> dict:
        """
        Obtiene los datos completos de un Pokemon.

        Args:
            name_or_id: Nombre (str) o ID (int) del Pokemon.
                        Ej: "pikachu", "charizard", 25, 6

        Returns:
            Diccionario con todos los datos del Pokemon.
            Usa models.parse_pokemon() para convertirlo a PokemonDetail.
        """
        #identifier= para poder nombrar en nuestra pokedex ya sea name or id
        identifier = str(name_or_id).lower().strip()
        return self.get(f"pokemon/{identifier}")

    def get_pokemon_list(self, limit: int = 20, offset: int = 0) -> dict:
        """
        Obtiene una lista paginada de Pokemon.

        Args:
            limit: Cantidad de resultados por pagina (max ~1000).
            offset: Desde que posicion empezar.

        Returns:
            Diccionario con:
                - count: Total de Pokemon disponibles
                - results: Lista de {name, url} para cada Pokemon
        """
        return self.get(f"pokemon?limit={limit}&offset={offset}")

    def get_type(self, name: str) -> dict:
        """
        Obtiene informacion de un tipo de Pokemon.

        Args:
            name: Nombre del tipo (ej: "fire", "water", "electric").

        Returns:
            Diccionario con datos del tipo, incluyendo relaciones de dano
            y lista de Pokemon de ese tipo.
            Usa models.parse_type_info() para convertirlo a TypeInfo.
        """
        return self.get(f"type/{name.lower().strip()}")

    def get_generation(self, gen_id: int) -> dict:
        """
        Obtiene informacion de una generacion de Pokemon.

        Args:
            gen_id: Numero de generacion (1-9).

        Returns:
            Diccionario con datos de la generacion, incluyendo
            lista de Pokemon y movimientos introducidos.
        """
        return self.get(f"generation/{gen_id}")

    def get_species(self, name_or_id) -> dict:
        """
        Obtiene datos de la especie de un Pokemon.

        Util para obtener cadena evolutiva, flavor text, habitat, etc.

        Args:
            name_or_id: Nombre o ID del Pokemon.

        Returns:
            Diccionario con datos de la especie.
        """
        identifier = str(name_or_id).lower().strip()
        return self.get(f"pokemon-species/{identifier}")

    def get_evolution_chain(self, chain_id: int) -> dict:
        """
        Obtiene una cadena evolutiva completa.

        Args:
            chain_id: ID de la cadena evolutiva.
                      (Se obtiene del campo evolution_chain.url en pokemon-species)

        Returns:
            Diccionario con la cadena evolutiva.
            Usa models.parse_evolution_chain() para convertirlo a lista de EvolutionStep.
        """
        return self.get(f"evolution-chain/{chain_id}")
