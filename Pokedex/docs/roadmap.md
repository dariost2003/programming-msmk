
# Roadmap

## Fase 1

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

        1. version 1.0 non functional
            Commits: 6797c1b - a07c81s
        2. version 1.0.1 functional version
            Commits: d744501 - 5f2f2f6
        3.  version 1.0.2 functional version
            Commits: 704b870 - 0a7bf43
        4. version 1.1.0 functional version
            Commits: 625afa0 - 0d14b9b
        5. version 1.2.0 functional version
            Commits: e89ecf - 22c6b01
        6. version 1.3.0 functional version
            Commits: e508999 - 7ab5c86

## Fase 2

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

        1. version 2.0.0 functional version
            Commits: d7937be
        2. version 2.1.0 functional version
            Commits: 58f2113

## Fase 3

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
        1. version 3.0.0 functional version
            Commits: 644c837
        2. version 3.1.0 functional version
            Commits: b3f4777
        3. version 3.1.1 functional version
            Commits: bed690d

## Fase 4

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
        │   │   ├── dependencias/
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
        │   │       │   └── type_badges.py
        │   │       └── pages/
        │   │           ├──  compare.py
        │   │           ├──  home.py
        │   │           ├──  pokemon_detail.py
        │   │           └── team_builder.py
        │   │
        │   └── react-app/
        │       ├── src/
        │       └── package.json
        │
        ├── .gitignore
        ├── docs/
        │     ├── architecture.md
        │     ├── pseudocode.md
        │     ├── roadmap.md
        │     └── api_design.md
        │
        ├── README.md
        └── docker-compose.yml

        Por cambios de docente se muda de repositorio, no se registran commits de nueva arquitectura y diseño

            1. version 1.0.0 no funcional
                Se crean carpetas y arquitectura en vs code, se empieza a mudar y cambiar archivos antiguos a archivos nuevos y escribir nuevo codigo
            2. version 1.0.1 no funcional
                Commits: primer commit registrado con nueva arquitectura
                
                 