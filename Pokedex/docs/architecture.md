# Arquitectua proyecto - Pokedex

## Objetivo general

Este proyecto se centra en crear una Pokedex, aplicacion web modular, escalable, y sostenible que permita la busqueda de datos Pokemon en base a PokeAPI, una API publica que recoge informacion general y especifica de todos los Pokemones.

La arquitectura y diseño fueron cambiados en su raiz y esencia para realizar una separacion logica, de responsabilidades, establecer una arquitectura por capas, que permita un manejo adecuado de errores, nuevas funcionalidades y escalabilidad en cache, base de datos y frontend

## Diagrama de arquitectura

Flujo del aplicativo web

FRONTEND/BACKEND
1. A[Usuario] ── Interactua con ──> B[Frontend-Streamlit] 
2. B[Frontend-Streamlit] ── llama a ──> C[Backend-FastAPI]
3. C[Backend-FastAPI] ── mira en ──> D[Routes]
4. D[Routes] ── dirige a ──> E[Services]
5. E[Services] ── usa ──> F[PokeAPI-Client]
        ├──E[Services] ── devuelve info .json a ──> G[Parsers]
        ├──E[Services] ── pasa info ──> H[Cache-Manager]
        │                                └──> H[Cache-Manager] ── guarda datos ──> I[Cache] 
        └──E[Services] ── pasa info ──> J[Generador-indice-pokemon]
    

7. G[Parsers] ── pasa datos estructurados a ──> K[Models]
6. K[Models] ── devuelve datos ──> B[Frontend-Streamlit]

Estructura principal
    pokedex/
        │
        ├──backend/
        │
        ├──frontend/
        │
        ├──docs/
        │
        ├──README.md
        │
        └──.gitignore


- Backend/: el backend se construyo mediante Fastapi y con una arquitectura modular por capas
        │
        └──app/
            ├──main.py:
            │
            │       **RESPONSABILIDADES:** Orquestador.
            │           - Iniciar aplicacion.
            │           - Registrar routers, conecta las rutas en un archivo separado.
            │           - Configura middlewares (CORSMiddleware).
            │           - Configura un endpoint /health para verificar que el sistema esta en funcionamiento.
            │           - Levanta el servidor (inicalizar par empezar con las peticiones).
            │
            │
            ├──api/   
            │    └──routes.py:
            │ 
            │       **RESPONSABILIDADES:** Controlador de la entrada a la Pokedex.
            │           - Define los endpoints de API: expone la Pokedex al frontend y defino URLs de acceso.
            │           - Validar parametros: Valida inputs, y define filtros de consulta.
            │           - Llamar a services: delega la logica a los diferentes services.
            │           - Retomar respuestas JSON.
            │           - Maneja los errores HTTP: levanta errores internos y mantiene a la app en funcionamiento.
            │
            │
            ├──clients/
            │     └──pokeapi_client.py: 
            │
            │       **RESPONSABILIDADES:** Llamadas inteligentes a API.
            │            - Se comunica con la PokeAPI (publica externa): hace las HTTP request, obtiene los datos │pokemon.
            │           - Rate limiting: establece un limite de peticiones.
            │           - Evitar llamadas repetidas.
            │           - Normaliza inputs: Errores en mayusuclas o minusculas, queries.
            │           - Abstraccion de endpoints y metodos semanticos a los diferentes dominios Pokemon.
            │
            │
            ├──services/
            │      ├──pokemon_service.py:    
            │      │
            │      │  **RESPONSABILIDADES:** Que puede hacer mi app (tipos, evoluciones, stats, sprites, etc)
            │      │      - Maneja las llamadas a PokeAPIClient: pide los datos.
            │      │      - Define diferentes usos y detalles de Pokemones: establece que datos o acciones podemos realizar con nuestra Pokedex.
            │      │     
            │      │ 
            │      ├──evolution_service.py: 
            │      │
            │      │  **RESNPONSABILIDAD**: un servicio que transforma datos en un arbol. 
            │      │        - Pide la cadena evolutiva de un Pokemon desde PokeAPI: resuelve URLs encadenadas.
            │      │        - Construye el arbol de evoluciones.
            │      │        - Limpia y ordena los datos de una evolucion.     
            │      │        
            │      │
            │      ├──filter_service.py:
            │      │
            │      │  **RESPONSABILIDAD:** Un repositorio en la memoria local.
            │      │        - Cargar el dataset local.
            │      │        - Aplica los filtros de busqueda configurados.
            │      │        - Optimiza la consulta para los filtros, evitando hacer varios llamados a la API, haciendo un dataset con datos basicos.
            │      │
            │      │
            │      └──type_service.py:        
            │       
            │         **RESPONSABILIDAD:** Logica de dominio Pokemon tipos.
            │               - Obtiene datos de tipos desde client.
            │               - Muestra la dinamica de las interacciones de daño recibido entre Pokemones.
            │      
            │      
            ├──parsers/
            │      ├──pokemon_parser.py:    
            │      │
            │      │  **RESPONSABILIDAD**: primera capa de parser 
            │      │      - Adapta los JSON externos en un modelo interno configurado.
            │      │      - Limpia y normaliza datos.
            │      │      - Selecciona la informacion relevante. 
            │      │      - Encapsula los datos externos para entregar una estructura unitaria a la app.  
            │      │     
            │      │ 
            │      ├──evolution_parser.py: 
            │      │
            │      │  **RESNPONSABILIDAD**: entrega un arbol limpio.
            │      │        - Parsear JSON, navega estructuras anidadas.
            │      │        - Limpia info irrelevante.
            │      │        - Crea una estructura apropiada para el frontend.     
            │      │
            │      │
            │      └──type_parser.py:     
            │       
            │         **RESPONSABILIDAD:** traductor de los sistemas de tipos de Pokemon a nuestro modelo.
            │               - Transforma datos externos a un diseño interno.
            │               - Toma las relaciones de daño.
            │               - Simplifica datos y encapsula info externa.
            │
            │
            ├──models/  
            │      └──pokemon.py:     
            │       
            │         **RESPONSABILIDAD:** lenguaje interno de nuestra Pokedex.
            │               - Define como se vera un Pokemon en nuestra app.
            │               - Representa varios dominios Pokemon(datos resumidos, datos completos, relaciones de tipos, nodo evolutivo).
            │               - Estandariza los datos, evita inconsistencias.
            │               - Separa el dominio de JSON externo, nuestra app ya no depende de datos JSON de la API externa, sino de nuestro models.
            │
            │
            ├──cache/  
            │      └──cache_manager.py:     
            │       
            │         **RESPONSABILIDAD:** adapta nuestra infraestructura de datos.
            │               - Inicializa infraestructura del cache, es decir, si no hay datos, crea la base de datos y define el esquema cache.
            │               - Guarda datos en la cache.
            │               - Obtiene datos desde la cache.
            │               - Manejo del Time to Live (ttl).
            │
            │
            ├──core/
            │      ├──config.py:    
            │      │
            │      │  **RESPONSABILIDAD**: centro de la configuracion de la app. 
            │      │      - Define configuracion global: metadatos, identificadores globales.
            │      │      - Configura nuestra PokeAPI, como se estructura, dependencias externas.
            │      │      - Configura el desempeño de la app, comportamiento del sistema. 
            │      │      - Define storage local, configura CORS.
            │      │      - Configuracion externa.          
            │      │
            │      │
            │      └──constants.py:     
            │       
            │         **RESPONSABILIDAD:** reglas fijas de nuestro sistema.
            │               - Constantes de integracion, define endpoints, centraliza dependencias.
            │               - Contiene las reglas fijas de performance.
            │               - Reglas: idiomas aceptados.
            │
            │
            ├──data/
            │     ├──seeds/  
            │     │       └──generate_pokemon_index.py:    
            │     │
            │     │  **RESPONSABILIDAD**: script ETL (Extraer, Transformar y Cargar(Load)). 
            │     │      - Extrae un gran volumen de datos de la API externa.
            │     │      - Itera y extrae datos necesarios.
            │     │      - Normaliza los datos. 
            │     │      - Crea un dataset local.
            │     │      - Manejo de errores por intentos y rate control.          
            │     │
            │     │
            │     └──datos_basicos_filtro:    
            │       
            │         **RESPONSABILIDAD:** dataset local.
            │               - Contiene datos Pokemones de acuerdo a los filtros de nuestra app.
            │               - Brinda los datos de forma resumida y modelada para presentar los datos de forma rapida cuando se coloque un filtro de busqueda.
            │ 
            │
            ├──utils/
            │      ├──colors.py: 
            │      │
            │      │  **RESPONSABILIDAD**: paleta de colores. 
            │      │      - Mapea los tipos de Pokemon y los empareja con un color.
            │      │      - Estandariza los colores en nuestro frontend.
            │      │      - Diccionario global de colores.   
            │      │     
            │      │ 
            │      ├──stats.py: 
            │      │
            │      │    **RESNPONSABILIDAD:** reglas del combate Pokemon.
            │      │        - Define las reglas de combate.
            │      │        - Calcula la efectividad de los tipos.
            │      │        - Combina los efectos de multiples tipos y clasifica los resultados.     
            │      │
            │      │
            │      └──formatters.py:.    
            │       
            │         **RESPONSABILIDADES:**
            │               - .
            │               - .
            │               - .   
            │
            │           
            └──dependencies/  
                   └──dependencias.py:   
                    
                      **RESPONSABILIDAD** 
                            - Crea infraestructura base.
                            - Conecta el cliente con la cache.
                            - Ensambla la logica de la app e inyecta infraestructura en services.
                            - Centraliza instancias globales.

             
- Frontend/: aqui se presenta la arquitectura de nuestro frontend, esta sera nuestra capa de presentacion al cliente, el que orquesta la interfaz de usuario.
        │
        └──streamlit/
                   ├──streamlit_app.py:
                   │
                   │       **RESPONSABILIDADES:** 
                   │           - Funciona de ancla o punto principal de nuestro frontend.
                   │
                   │
                   ├──api/   
                   │    └──backend_client.py: 
                   │ 
                   │       **RESPONSABILIDADES**: es el http client del frontend.
                   │           - Conecta Streamlit con nuestra API interna en el backend.
                   │           - Encapsula HTTP requests.
                   │           - Abstrae endpoints.
                   │
                   │
                   ├──clients/
                   │     └──pokeapi_client.py: 
                   │
                   │       **RESPONSABILIDAD**: Llamadas inteligentes a API.
                   │            - Se comunica con la PokeAPI (publica externa): hace las HTTP request, obtiene los datos │pokemon.
                   │           - Rate limiting: establece un limite de peticiones.
                   │           - Evitar llamadas repetidas.
                   │           - Normaliza inputs: Errores en mayusuclas o minusculas, queries.
                   │           - Abstraccion de endpoints y metodos semanticos a los diferentes dominios Pokemon.
                   │
                   │
                   ├──components/
                   │      ├──combat_effectiveness.py: 
                   │      │
                   │      │  **RESPONSABILIDAD**: daño recibido en combate
                   │      │      - Representa en la UI las interacciones de resistencia y debilidades de los Pokemones.
                   │      │     
                   │      │ 
                   │      ├──evolution_chain.py: 
                   │      │
                   │      │  **RESNPONSABILIDAD**: presenta la usuario el arbol de evolucion con un diseño atractivo.
                   │      │        - Representa en la UI el arbol de evoluciones de un Pokemon.
                   │      │        - Incluye dentro de la representacion los requisitos para su evolucion.
                   │      │        
                   │      │
                   │      ├──pokemon_card.py: 
                   │      │
                   │      │  **RESPONSABILIDAD:** carta coleccionable.
                   │      │        - Renderiza una carta, representacion visual del Pokemon.
                   │      │
                   │      │
                   │      ├──radar_chart.py: 
                   │      │
                   │      │  **RESPONSABILIDAD** 
                   │      │        - Representa los stats de un Pokemon en un grafico tipo radar.
                   │      │
                   │      │
                   │      └──type_badges.py:
                   │       
                   │         **RESPONSABILIDADES:** 
                   │               - Renderiza una insignia de acuerdo al tipo del Pokemon seleccionado.
                   │               
                   │      
                   │      
                   └──pages/
                          ├──compare.py: **EN DESARROLLO**   
                          │
                          │  **RESPONSABILIDADES:** Pokemon vs Pokemon 
                          │      - Compara las stats.
                          │      - Muestra las diferencias entre Pokemones.
                          │     
                          │ 
                          ├──home.py: 
                          │
                          │  **RESNPONSABILIDADES:** la pagina de presentacion de nuestra app.
                          │        - Pagina inicial de interacicon del usuario.
                          │        - Contiene las barras y filtros de busqueda.
                          │        - Es la pagina a traves de la cual se navega en nuestra app.
                          │     
                          │ 
                          ├──pokemon_detail.py: es el archivo que coordina las llamadas al backend.
                          │
                          │  **RESNPONSABILIDADES:**
                          │        - Ensambla la interfaz del usario a detalle.
                          │
                          │
                          └──team_builder.py: **EN DESAROLLO** 
                           
                             **RESPONSABILIDADES:** construye equipos de acuerdo a estadisticas y preferencias.
                                   - Establece una logica en la UI de seleccion de Pokemones.
     
                    
                   
                   
# Tecnologias que usa la app

- Python ---> El lenguaje principal de programacion de la app.
- Fastapi ---> Backend de nuestra API.
- Streamlit ---> Frontend actual.
- Reactapp ---> Frontend fase 6.
- PokeAPI ---> Fuente de datos externa.
- JSON ---> Datos auxiliares.
- Uvicorn ---> Servidor ASGI.

# Flujo de datos

1. Usuario realiza una busqueda en la interfaz de usuario (frontend).
2. Streamlit llama al backend, a nuestra FastAPI.
3. FastAPI recibe la peticion mediante routes.py.
4. Routes.py llama al Services correspondiente.
5. Services consulta inicialmente el cache.
6. Si no existe la informacion en el cache ---> se hace el llamado a la API externa.
7. Se recibe la respuesta y se parsean los datos.
8. Los datos parseados se transforman en un Models interno.
9. Se almacenan los datos en el cache.
10. Se envia la respuesta a frontend.
11. Frontend muestra los datos de acuerdo al diseño escrito.
12. Usuario ve la respuesta de su busqueda en UI.

