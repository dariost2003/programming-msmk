# Ejercicio 4: PokeDex Avanzado con PokeAPI

## Descripcion

En este ejercicio vas a construir un **PokeDex interactivo** usando la [PokeAPI](https://pokeapi.co/api/v2/), una API REST gratuita con datos de todos los Pokemon.

El objetivo es practicar:
- Consumo de APIs REST con `requests`
- Manejo de respuestas JSON complejas
- Cache de datos para optimizar peticiones
- Construccion de interfaces con Streamlit
- Visualizacion de datos con Plotly

## Que se proporciona

Ya tienes la base lista para trabajar:

| Archivo | Descripcion |
|---------|-------------|
| `api_client.py` | Cliente HTTP con cache, rate limiting y manejo de errores |
| `cache.py` | Cache basado en SQLite para no repetir peticiones a la API |
| `models.py` | Dataclasses y funciones para parsear las respuestas de la API |
| `app_ejemplo.py` | App minima de ejemplo que demuestra como funciona todo |
| `requirements.txt` | Dependencias del proyecto |

## Como ejecutar el ejemplo

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Ejecutar la app de ejemplo
streamlit run app_ejemplo.py
```

Se abrira una ventana en tu navegador donde puedes buscar un Pokemon por nombre.

## Tareas

Tu objetivo es crear un archivo `app.py` con el PokeDex completo. Debes implementar las siguientes funcionalidades:

### Tarea 1: Buscador avanzado
- Busqueda por nombre (con autocompletado o sugerencias)
- Busqueda por ID (rango de 1 a 1010)
- Mostrar una lista de resultados con sprite, nombre y tipos

### Tarea 2: Filtros
- Filtrar Pokemon por tipo (fire, water, grass, etc.)
- Filtrar por generacion (1-9)
- Filtrar por rango de estadisticas (ej: "ataque mayor a 100")
- Combinar multiples filtros

### Tarea 3: Vista de detalle
- Al seleccionar un Pokemon, mostrar toda su informacion:
  - Sprite grande (artwork oficial)
  - Estadisticas con grafico de radar o barras
  - Tabla de tipos (debilidades y resistencias)
  - Cadena evolutiva con sprites de cada etapa
  - Descripcion del Pokemon (flavor text de la especie)

### Tarea 4: Comparador de Pokemon
- Seleccionar 2 o 3 Pokemon para comparar
- Grafico superpuesto de estadisticas
- Tabla comparativa de tipos, habilidades, peso, altura
- Indicar cual tiene ventaja de tipo sobre el otro

### Tarea 5: Constructor de equipo
- Permitir seleccionar 6 Pokemon para un equipo
- Analisis de cobertura de tipos del equipo
- Debilidades y resistencias combinadas
- Estadisticas promedio del equipo
- Sugerencias para mejorar el equipo (tipos no cubiertos)

## Documentacion de la PokeAPI

La documentacion completa esta en: https://pokeapi.co/docs/v2

### Endpoints que vas a necesitar

| Endpoint | Descripcion | Ejemplo |
|----------|-------------|---------|
| `pokemon/{name o id}` | Datos de un Pokemon | `pokemon/pikachu` |
| `pokemon?limit=N&offset=M` | Lista paginada | `pokemon?limit=20&offset=0` |
| `type/{name}` | Info de un tipo | `type/fire` |
| `generation/{id}` | Pokemon por generacion | `generation/1` |
| `pokemon-species/{name}` | Especie (flavor text, evolucion) | `pokemon-species/pikachu` |
| `evolution-chain/{id}` | Cadena evolutiva | `evolution-chain/10` |

### Estructura de la respuesta de `pokemon/{name}`

Los campos mas utiles:

```
{
  "id": 25,
  "name": "pikachu",
  "types": [{"type": {"name": "electric"}}],
  "stats": [{"base_stat": 35, "stat": {"name": "hp"}}, ...],
  "abilities": [{"ability": {"name": "static"}}, ...],
  "height": 4,       // decimetros
  "weight": 60,      // hectogramos
  "base_experience": 112,
  "sprites": {
    "front_default": "url...",
    "other": {"official-artwork": {"front_default": "url..."}}
  }
}
```

## Consejos

### Rate limiting
La PokeAPI es gratuita y no requiere autenticacion, pero tiene limites de uso. El `api_client.py` ya incluye una pausa minima entre peticiones. Ademas, el cache evita peticiones repetidas.

### Como funciona el cache
Cada vez que haces una peticion, el cliente:
1. Busca en la base de datos SQLite si ya tiene esa respuesta
2. Si la tiene y no ha expirado (1 hora por defecto), la devuelve directo
3. Si no la tiene, hace la peticion HTTP real y guarda el resultado

Esto significa que la primera vez sera lento, pero las siguientes seran instantaneas.

### Usar los modelos
No trabajes directamente con los diccionarios de la API. Usa las funciones de `models.py`:

```python
from api_client import PokeAPIClient
from models import parse_pokemon, parse_type_info

client = PokeAPIClient()

# Obtener datos y parsear
data = client.get_pokemon("charizard")
pokemon = parse_pokemon(data)

print(pokemon.name)          # "charizard"
print(pokemon.types)         # ["fire", "flying"]
print(pokemon.stats["attack"])  # 84
```

### Streamlit
- Usa `st.columns()` para layouts de multiples columnas
- Usa `st.tabs()` para organizar secciones
- Usa `st.selectbox()` o `st.multiselect()` para filtros
- Usa `st.session_state` para mantener el estado entre interacciones
- Usa `@st.cache_data` para cachear funciones costosas en Streamlit

### Plotly
- `go.Bar` para graficos de barras
- `go.Scatterpolar` para graficos de radar (ideal para comparar stats)
- `go.Figure.add_trace()` para superponer multiples Pokemon en un grafico
