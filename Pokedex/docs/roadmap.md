
# Roadmap - Pokedex

## Objetivo general de la app
Permitir consultar informacion de un Pokemon y entregar los datos de forma estructurada, rapida y con buen diseño

## Objetivos especificos

- Presentar una interfaz util, navegable e intuitiva.
- Permitir la busqueda por nombre o ID del Pokemon.
- Mostrar detalles del Pokemon: tipo, Descripción, interacciones de daño, arbol de evolucion, requisitos de evolucion, stats, habilidades.
- Comparar Pokemones, mostrar diferenecias, ventajas o desventajas entre 2 Pokemones.
- Construir equipos Pokemon, permitir al usuario crear equipos con varios Pokemons, de hasta 6 Pokemons y varios equipos, con sus respectivas interacciones y potencialidades.


# Fase 1 (MVP: producto minimo viable 24/04/2026 - 04/05/2026)

 - Pokedex version 1

    python-class-2/
        │
        ├── ejercicio-1-sensores/
        ├── ejercicio-2-juego/
        ├── ejercicio-3-ciberseguridad/
        ├── ejercicio-5-canvas/
        └── ejercicio-4-pokeapi
                │
                ├── CRITERIOS.md
                ├── README.md
                ├── api_client.py
                ├── app_ejemplo.py
                ├── cache.py
                ├── models.py
                ├── pokedex.py
                └── requirements.txt

## Funcionalidades:
- Barra de busqueda basica de Pokemon
- Cache basico
- Vista a detalle inicial/simple Pokemon
- Conexion a PokeAPI externa


# Fase 2 (Nuevas funcionalidades adaptadas 05/05/2026)

 - Pokedex version 2

    python-class-2/
        │
        ├── ejercicio-1-sensores/
        ├── ejercicio-2-juego/
        ├── ejercicio-3-ciberseguridad/
        ├── ejercicio-5-canvas/
        └── ejercicio-4-pokeapi
                │
                ├── CRITERIOS.md
                ├── README.md
                ├── api_client.py
                ├── app_ejemplo.py
                ├── cache.py
                ├── datos_basicos_filtro.json
                ├── models.py
                ├── pokedex.py
                ├── pokemon_filter_seed.py
                └── requirements.txt

## Nuevas funcionalidades:
- Filtros de busqueda.
- Mejora eficiencia en busqueda.
- Scripts para generar dataset propio.
- Mejoras de diseño de UI.


# Fase 3 (Nuevas funcionalidades adaptadas 06/05/2026)

 - Pokedex version 3

    python-class-2/
        │
        ├── ejercicio-1-sensores/
        ├── ejercicio-2-juego/
        ├── ejercicio-3-ciberseguridad/
        ├── ejercicio-5-canvas/
        └── ejercicio-4-pokeapi
                │
                ├── CRITERIOS.md
                ├── README.md
                ├── api_client.py
                ├── app_ejemplo.py
                ├── cache.py
                ├── datos_basicos_filtro.json
                ├── models.py
                ├── pokedex.py
                ├── pokemon_filter_seed.py
                └── requirements.txt
       
## Nuevas funcionalidades:
- Cadena evolutiva añadida.
- Relaciones de daño por tipo.
- Flavor text.
- Correccion de bugs.
- Se optimiza la logica de busqueda.
- Mejoras de diseño.


# Fase 4 (Nueva arquitectura/diseño, cambio general/total, 08/05/2026- actual)

    Hasta el momento se presenta una aplicacion web funcional, esteticamente llamativa, sin embargo por motivos de orden y diseño se decide mudar de arquitectura y diseño por el siguiente:

    pokedex/
        │
        ├── backend/
        │   │
        │   ├── app/
        │   │   │
        │   │   ├── main.py
        │   │   │
        │   │   ├── api/
        │   │   │   └── routes.py
        │   │   │
        │   │   ├── clients/
        │   │   │   └── pokeapi_client.py
        │   │   │
        │   │   ├── services/
        │   │   │   ├── pokemon_service.py
        │   │   │   ├── evolution_service.py
        │   │   │   ├── type_service.py
        │   │   │   └── filter_service.py
        │   │   │
        │   │   ├── parsers/
        │   │   │   ├── pokemon_parser.py
        │   │   │   ├── evolution_parser.py
        │   │   │   └── type_parser.py
        │   │   │
        │   │   ├── models/
        │   │   │   └── pokemon.py
        │   │   │
        │   │   ├── cache/
        │   │   │   └── cache_manager.py
        │   │   │
        │   │   ├── core/
        │   │   │   ├── config.py
        │   │   │   └── constants.py
        │   │   │
        │   │   ├── data/
        │   │   │   ├── datos_basicos_filtro.json
        │   │   │   └── seeds/
        │   │   │       └── generate_pokemon_index.py
        │   │   │
        │   │   ├── utils/
        │   │   │   ├── colors.py
        │   │   │   ├── stats.py
        │   │   │   └── formatters.py
        │   │   │
        │   │   ├── dependencies/
        │   │   │   └──dependencias.py
        │   │   │                                 
        │   │   └── requirements.txt
        │   │
        │   └── venv/
        │
        ├── frontend/
        │   │
        │   ├── streamlit/
        │   │       ├── streamlit_app.py
        │   │       │   
        │   │       ├── api/
        │   │       │   └── backend_client.py    
        │   │       │
        │   │       ├── components/
        │   │       │   ├──  combat_effectiveness.py
        │   │       │   ├──  evolution_chain.py
        │   │       │   ├──  combat_card.py
        │   │       │   ├──  radar_chart.py
        │   │       │   └──  type_badges.py
        │   │       └── pages/
        │   │           ├──  compare.py
        │   │           ├──  home.py
        │   │           ├──  pokemon_detail.py
        │   │           └── team_builder.py
        │   │
        │   └── react-app/ (mudar en proximas etapas)
        │       ├── src/
        │       └── package.json 
        │
        │
        ├── docs/
        │     ├── architecture.md
        │     ├── pseudocode.md
        │     ├── roadmap.md
        │     ├── readme.md
        │     └── api_design.md
        └── .gitignore
        
        
    
        Por cambios de docente se muda de repositorio, no se registran commits de nueva arquitectura y diseño

## Cambios Principales:
- Migracion total a nueva arquitectura modular por capas.
- Separacion frontend/backend.
- Implementación de FastAPI.
- Varios servicios.
- Parsers independientes.
- Reutilizacion de componentes.
- Organizacion y diseño con vistas a escalar a otras apps de UI, storage, uso de servidores en nube.

   
    
# Fase 5 (Comparador de pokemones, constructor de equipos, corto plazo 10 dias)

## Funcionalidades previstas:
### Comparador de Pokemon
- Compara stats.
- Compara tipos.
- Compara graficos de radar.

### Constructor de equipos
- Permite añadir Pokemones a un equipo.
- Da sugerencias de Pokemones para el equipo de acuerdo a debilidades y tipos.

### Mejoras en la interfaz de usuario
- Animaciones basicas.
- Diseño adaptativo a diferentes pantallas.
- Mejoras en las tarjetas Pokemon.

### Dockerizacion
- Crear nuestro Dockfile Backend.
- Y construir el Docker Compose (carpeta ya creada).

### Cache Mejorado
- TTL cache
- Invalidacion simple


# Fase 6 (Migrar a React, mediano plazo)

## Nuevas funcionalidades previstas:
- React + Vite.
- Axios API Client.
- Migrar a SPA con React Router. 
- Componentizacion avanzada en React.
- Estado Global


## Ideas Futuras
- Sistema de favoritos.
- Base de datos con login de usuarios.
- Simulador de Combate.
- Implementación de IA, para recomendaciones y preguntas.





















