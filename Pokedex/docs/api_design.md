# Diseño de la app

En este archivo se encuentran las decisiones de diseño, y la planificacion previa a la escritura de codigo.

## Objetivo general de la app
Permitir consultar informacion de un Pokemon y entregar los datos de forma estructurada, rapida y con buen diseño

## Objetivos especificos

- Presentar una interfaz util, navegable e intuitiva.
- Permitir la busqueda por nombre o ID del Pokemon.
- Mostrar detalles del Pokemon: tipo, descripcion, interacciones de daño, arbol de evolucion, requisitos de evolucion, stats, habilidades.
- Comparar Pokemones, mostrar diferenecias, ventajas o desventajas entre 2 Pokemones.
- Construir equipos Pokemon, permitir al usuario crear equipos con varios Pokemons, de hasta 6 Pokemons y varios equipos, con sus respectivas interacciones y potencialidades.

## Principios de diseño

La base mas importante sobre la cual se inicia la programacion de esta app es:

### Arquitectura modular por capas
Se establece una arquitectura por capas en donde se presenta:
- Frontend
- Api(Backend)
- Servicios (Backend)
- Cliente/Datos (Backend)
- PokeAPI (API externa)

La misma se convina con una arquitectura por modulos:
- Backend
    - api/
    - cache/
    - clients/
    - core/
    - data/
    - dependencies/
    - models/
    - parsers/
    - services/
    - utils/

- Frontend
    - api/
    - components/
    - pages/

Se ha escogido esta arquitectura porque facilita todos nuestros principios de diseño, como la separacion por responsabilidades, la reutilizacion, la escalabilidad y posibles mejoras a futuro

## Arquitectura REST (Representational State Transfer)
Al ser una app que usa APIs esta arquitectura definira como el exterior se comunica con nuestra app, mediante esta arquitectura podemos manejar las URLs, los metodos (GET, POST), esto se incorpora dentro tanto del backend como del frontend:
- Backend/api
- Frontend/api

En las dos nos encontramos la carpeta api/, que ademas de ser parte de los modulos, aqui se encuentran las bases para que nuestra app se comunique con la API externa y a su ves, el puente que conecta el Frontend con el Backend.
    
### Separacion de responsabilidades
En correspondencia con nuestra arquitectura por modulos, se generan varias carpetas y archivos, cada uno con unas cuantas lineas de codigo, debido a que tienen una responsabilidad unica clara, esta separacion permite llevar un flujo ordenado de trabajo, asi como hacer una adecuada factorizacion del codigo y disminuir los errores, y mejorar el troubleshooting.

### Escalabilidad
Se muda a una nueva y mejorada arquitectura con la finalidad de escalar en un futuro:
 - Migrar a un nuevo frontend con mas caracteristicas y opciones de diseño de forma mas sencilla.
 - Implementar nuevas funcionalidades para uso del usuario, constructor de equipos, comparador de Pokemones.

 ### Reutilizacion
 Es fundamental establecer un principio en el que se puedan reutilizar varios servicios programados entre:
 - API.
 - Streamlit.
 - Reactapp.
 - Tets.

 
## Endpoints principales

| Metodo | Endpoint | Description |
| ------ | -------- | ----------- |
| GET | /pokemon/{name} | Obtiene un Pokemon |
| GET | /pokemon/id/{id}| Obtiene un Pokemon por ID |
| GET | /pokemon/filter?<tipo de filtro deseado>: <ul><li>generation=1</li><li>type=fire</li><li>min_hp = 50</li><li>min_attack=40</li><li>min_defense=30</li><li>min_base_exp=50</li></ul> | Filtra la busqueda de acuerdo al parametro deseado |
| GET | /pokemon/compare | Compara un Pokemon con otro |
| GET | /pokemon/evolution/{name} | Obtiene la cadena evolutiva |
| GET | /pokemon/team-builder | Constructor de equipos Pokemon |
| GET | /health | Estado de la API |

## Manejo de datos

### Endpoint: GET Pokemon
Request: 
    GET /pokemon/pikachu
Response:
    {
        "id": 25,
        "name": "pikachu",
        "types": ["electric"],
        "height": 4,
        "weight": 60,
        "abilities": ["static],
        "stats": {
            "hp": 35,
            "attack": 55,
            "defense": 40,
            "speed": 90
        },
        "sprite": "https://..."
    }

### Endpoint: GET Filtro de busqueda
Request: 
    GET /pokemon/type/fire
Response:
    {
        "type": "fire",
        "count": "5",
        "results": [
            "charizard",
            "arcanine",
            "flareon"
        ]
    }

### Endpoint: GET Evolucion
Request:
    GET pokemon/evolution/charmander
Response: 
    {
        "base": "charmander",
        "evolutions": [
            "charmaleon",
            "charizard"
        ]
    }

### Endpoint: GET Comparador
Request: 
    GET /pokemon/compare?first=pikachu&second=raichu
Response:
    {
        "first": {
            "name": "pikachu",
            "total_stats": 320
        },
        "second": {
            "name": "raichu",
            "total_stats": 485
        }
    }

### Endpoint: GET Constructor de equipos
Request:
    GET /pokemon/team-builder?types=fire,water
Response:
    {
        "recommended_team": [
            "charizard",
            "gyarados",
            "venusaur"
        ]
    }


## Manejo de errores

| Código | Significado |
| ------ | ----------- |
| 200 | OK |
| 400 | Bad Request |
| 404 | Pokemon no encontrado |
| 422 | Error de validacion |
| 500 | Error interno |








