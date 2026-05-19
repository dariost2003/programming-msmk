from __future__ import annotations

from typing import Any
import requests

# Cliente encargado de comunicarse con el backend FastAPI
class BackendClient:

    BASE_URL = 'http://localhost:8000/api/v1'
    TIMEOUT = 15
    
    # Metodo reutilizable para requests GET
    def _get(self, endpoint: str, params: dict[str, Any] | None=None) -> Any:
        
        url = f'{self.BASE_URL}{endpoint}'

        try:
            response = requests.get(url, params=params, timeout=self.TIMEOUT)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError as e:
            raise RuntimeError(f'Error HTTP en backend: {e}') from e

        except requests.exceptions.ConnectionError as e:
            raise RuntimeError('No se pudo conectar con el backend') from e

        except requests.exceptions.Timeout as e:
            raise RuntimeError('El backend tardó demasiado en responder') from e

    def get_pokemon(self, identifier: str) -> dict[str, Any]:
        return self._get(f'/pokemon/{identifier}')
    
    def get_evolution(self, identifier: str) -> dict[str, Any]:
        return self._get(f'/pokemon/{identifier}/evolution')

    def get_type(self, type_name: str) -> dict[str, Any]:
        return self._get(f'/types/{type_name}')

    def filter_pokemons(self, **params: Any) -> list[dict[str, Any]]:
        return self._get('/pokemon/filter', params=params)

    def get_effectiveness(self, identifier: str) -> dict[str, Any]:
        return self._get(f'/pokemon/{identifier}/effectiveness')

    def get_flavor_text(self, identifier: str) -> dict[str, Any]:
        return self._get(f'/pokemon/{identifier}/flavor_text')

