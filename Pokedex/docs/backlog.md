# Backlog

## Prioridades usadas para el backlog: 
    
- Alta: Fundamental para el funcionamiento de la app.
- Media: Mejora importante de la app.
- Futuro: Funcionalidades para futuras fases.

## Estados de las actividades en el backlog:

- Completado: Actividad terminada.
- En curso: Se encuentra en desarrollo.
- Pendiente: En espera, falta desarrollar.
- Futuro: Proximas funcionalidades, a largo plazo.

### DOD (Definition of Done): Definición de completado:
Una actividad se considera completada cuando:
- El código funciona correctamente.
- Cumple criterios de aceptación.
- No se generan errores.
- Se integra con la nueva arquitectura.
- Se prueba manualmente.
- Mantiene el estilo modular por capas del proyecto.

# EPICA 1 - ARQUITECTURA BASE

## Objetivo
Construir una base de arquitectura que divida responsabilidades frontend/backend y la arquitectura basica modular por capas.

## Historia 1.1 - Crear una arquitectura modular por capas para el backend y frontend

### Prioridad: ALTA.
### Estado: COMPLETADO.

#### Descripción
Como estudiante de primer año, busco una arquitectura modular por capas para que el proyecto pueda ser desarrollado de forma ordenada, que tenga posibilidad de escalar y que se pueda mantener.

### Criterios de aceptación
- [x] Crear carpeta backend/app.
- [x] Crear modulos:
    - api.
    - cache.
    - clients.
    - core.
    - data.
    - dependencies.
    - models.
    - parsers.
    - services.
    - utils.

## Historia 1.2 - Configurar FastAPI

### Prioridad: ALTA.
### Estado: COMPLETADO.

#### Descripción
Como desarrollador necesito un backend FastAPI funcional para nuestros endpoints REST.

### Criterios de aceptación
- [x] main.py inicializa FastAPI.
- [x] Se ha creado el endpoint /health.
- [x] Routers registrados correctamente.
- [x] Uvicorn levanta el servidor.

## Historia 1.3 - Configurar frontend en Streamlit

### Prioridad: ALTA.
### Estado: COMPLETADO.

#### Descripción
Como ususario, me gustaria una interfaz visual y con buen diseño para interactuar con la app.

### Criterios de acpetacion
- [x] Existe streamlit_app.py.
- [x] Frontend se conecta con el backend.
- [x] Navegacion funciona entre paginas.

## Historia 1.4 - Configurar CORS y configuracion global

### Prioridad: ALTA.
### Estado: COMPLETADO.

#### Descripción
Como desarrollador, me gustaria una app con principios de seguridad y un archivo donde se puedan recoger los principios de configuracion de la app, que despues puedan ser modificados facilmente, sin tocr el codigo.

### Criterios de aceptación
- [x] Middleware CORS configurado.
- [x] Configuracion centralizada en un archivo config.py.
- [x] Variables que se puedan reutilizar en la app.


# EPICA 2 - Cache y rendimiento

## Objetivo
Mejorar la velocidad, disminuir llamadas, y mejorar infraestructura para escalabilidad.

## Historia 2.1 - Implementar cache persistente SQLite

### Prioridad: ALTA.
### Estado: COMPLETADO.

#### Descripción
Como desarrollador es fundamental para esta app usar almacenamiento para disminuir las llamdas repetidas.

### Criterios de aceptación
- [x] Cache persistente funcional.
- [x] SQLite integrado.
- [x] Lectura y escritura en el cache opoerativo.
- [x] Cache integrado con services.

## Historia 2.2 - Implementar TTL cache

### Prioridad: ALTA.
### Estado: COMPLETADO.

#### Descripción
Es fundamental implementar el TTL en el cache para borrar datos antiguos, y evitar inconsistencias.

### Criterios de aceptación
- [x] Cada registro tiene su timestamp (fecha y hora).
- [x] El cache expira automaticamente.
- [x] Datos vencidos se refrescan.


## Historia 2.3 - Optimizar estrategia cache-first

### Prioridad: ALTA.
### Estado: COMPLETADO.

#### Descripción
Como desarrollador, es fundamental que nuestra app consulta primero a la cache.

### Criterios de aceptación
- [x] Se consulta primero el cache antes de hacer una request a la API externa.
- [x] Disminuye la cantidad de requests.


# EPICA 3 - Integracion con la PokeAPI

## Objetivo
Pedir la informacion de los diferentes Pokemones a la API externa.

## Historia 3.1 - Iniciar el cliente PokeAPI

### Prioridad: ALTA.
### Estado: COMPLETADO.

#### Descripción
Para tener un adecuado backend se necesita un cliente HTTP para hacer requests a la PokeAPI externa.

### Criterios de aceptación
- [x] Crear pokeapi_client.py.
- [x] Maneja requests HTTP.
- [x] Normaliza identificadores.
- [x] Manejo de errores.

## Historia 3.2 - Usar rate limiting basico

### Prioridad: MEDIA.
### Estado: COMPLETADO.

#### Descripción
Como desarrollador, es util conocer e implementar herramientas para el manejo de peticiones en apps que utilizan APIs.

### Criterios de aceptación
- [x] Limitacion de frecuencia de llamadas a la API.
- [x] Se evitan llamadas repetidas a la API.

## Historia 3.3 - Manejo de errores externos

### Prioridad: ALTA.
### Estado: COMPLETADO.

#### Descripción
Es necesario implementar el manejo de errores para evitar que crashee la app.

### Criterios de aceptación
- [x] Errores HTTP manejados.
- [x] Timeout controlado.
- [x] Mensajes consistentes en el frontend.


# EPICA 4 - Gestion y solicitud de informacion de los Pokemones

## Objetivo
Consultar la informacion de un Pokemon

## Historia 4.1 - Busqueda de Pokemon por nombre o ID

### Prioridad: ALTA.
### Estado: COMPLETADO.

#### Descripción
Como usuario lo minimo que espero de una Pokedex es que me permita buscar un Pokemon por nombre o ID, mediante el endpoint.

#### Endpoint
GET /pokemon/{identifier}

### Criterios de aceptación
- [x] Devuelve los datos completos de un Pokemon.
- [x] Se muestra al sprite del Pokemon.
- [x] Incluye datos de estadisticas, habilidades y tipo del Pokemon.
- [x] Se permite la busqueda de forma correcta tanto por ID como por el nombre del Pokemon.

## Historia 4.2 - Parsear datos externos

### Prioridad: ALTA.
### Estado: COMPLETADO.

#### Descripción 
Para un buen manejo de los datos en una app modular por capas, es necesario transformar datos crudos tipo JSON a un modelo de lenguaje interno.

### Criterios de aceptación
- [x] Crear pokemon_parser.py, type_parser.py 
- [x] JSON externo no llega al frontend.
- [x] Se usan estos datos parseados en la logica interna.

## Historia 4.3 - Mostrar el detalle completo del Pokemon

### Prioridad: ALTA.
### Estado: COMPLETADO.

#### Descripción
Como parte de una app completa, es fundamental incluir un detalle de caracteristicas del Pokemon.

### Criterios de aceptación
- [x] Se muestra el detalle completo del Pokemon.
- [x] Se renderiza el tipo, stats, habilidades, sprite, peso, altura.

# EPICA 5 - Filtros de busqueda

## Objetivo
Permitir busqueda avanzada por filtros.

## Historia 5.1 - Crear dataset local

### Prioridad: ALTA.
### Estado: COMPLETADO.

#### Descripción
Como desarrollador, para optimizar la busqueda por filtros es necesario crear un pequeño dataset para extraer y obtener los datos de forma sencilla, rapida y que permita mostrar en la UI los diversos resultados derivados de la busqueda mediante filtros.

### Criterios de aceptación 
- [x] Crear un script ETL funcional, archivo llamado generate_pokemon_index.py
- [x] Archivo datos_basicos_filtro.json generado automaticamente.

## Historia 5.2 - Filtro de Pokemon por tipos y generación

### Prioridad: ALTA.
### Estado: COMPLETADO.

#### Descripción
Como usuario me gustaria buscar a Pokemones de acuerdo a un filtro que me permita buscar por tipos y la generación.

#### Endpoint
GET /pokemon/filter?type=fire

### Criterios de aceptación
- [x] Crear Endpoint. 
- [x] Sidebar funcional en Streamlit.
- [x] Datos se visualizan en galería.

## Historia 5.3 - Filtro por stats

### Prioridad: MEDIA.
### Estado: COMPLETADO.

#### Description
Como ususario me gustaria poder buscar Pokemones por diferentes stats de los mismos.

### Criterios de aceptación
- [x] Se puede filtrar por HP.
- [x] Se puede filtrar por ataque.
- [x] Se puede filtrar por defensa.
- [x] Se puede filtrar por experiencia base

## Historia 5.4 - Filtros utilizan el dataset, sin llamar a una API externa

### Prioridad: ALTA.
### Estado: COMPLETADO.

#### Descripción
Como desarrollador, es fundamental que se utilice la herramienta creada, tanto como para rapidez, como para fluidez de la app.

### Criterios de aceptación
- [x] Sistema de filtros usa el Dataset local.
- [x] No se realizan requests a la API externa.


# EPICA 6 - Sistema de evoluciones

## Objetivo
Se representa y muestra de forma visual la cadena evolutiva de un Pokemon

## Historia 6.1 - Datos de la cadena evolutiva

### Prioridad: MEDIA.
### Estado: COMPLETADO.

#### Descripción
Como paso inicial en la construccion de un arbol evolutivo, es necesario iniciar obteniendo los datos basicos de una cadena evolutiva, mediante el endpoint:
- GET /pokemon/evolution/{identifier}

### Criterios de aceptación
- [x] Se obtienen los datos completos de una cadena evolutiva.
- [x] Se resuelven URLs encadenadas

## Historia 6.2 - Crear archivo que parsee datos evolutivos

### Prioridad: MEDIA.
### Estado: COMPLETADO.

#### Descripción
Al igual que con los datos de un Pokemon, es necesario para una cadena evolutiva crear un archivo que parsee los datos de esta cadena evolutiva.

### Criterios de aceptación
- [x] Navega y extrae datos de un JSON anidado.
- [x] Se construye un arbol con datos limpios.

## Historia 6.3 - Mostrar el arbol evolutivo en la interfaz de usuario

### Prioridad: ALTA.
### Estado: COMPLETADO.

#### Descripción
Como usuario me gustaria ver en pantalla un arbol que muestra la evolucion.

### Criterios de aceptación
- [x] Diseño visual funcional.
- [x] Se muestra el arbol evolutivo en orden, con sus respectivos sprites.

## Historia 6.4 - Mostrar requisitos de evolucion

### Prioridad: MEDIA.
### Estado: COMPLETADO.

#### Descripción
Asi como el arbol evolutivo, como usuario me gustaria que dentro de este se incluyan los requisitos para avanar a dicha evolucion.

### Criterios de aceptación 
- [x] Muestra el nivel requerido.
- [x] Muestra los objetos necesarios.
- [x] Se muestran metodos alternativos (Intercambio, Felicidad, Clima).

# EPICA 7 - Sistema de tipos e interacciones en combate

## Objetivo
Representar la logica de las interacciones en un combate Pokemon de acuerdo al tipo de Pokemon.

## Historia 7.1 - Calcular las relaciones de daño

### Prioridad: MEDIA.
### ESTADO: COMPLETADO.

#### Descripción
Como desarrollador, si quiero mostrar la usuario las relaciones de daño, estas tienen que ser incialmente calculadas.

### Criterios de aceptación
- [x] Crea archivo stats.py
- [x] Calculo de debilidades.
- [x] Calculo de resistencias.
- [x] Calculo de inmunidad.

## Historia 7.2 - Instaurar la logica de la efectividad del daño

### Prioridad: MEDIA.
### ESTADO: COMPLETADO.

#### Descripción
Como desarollador, para lograr implementarlo en el diseño final, es necesario crear la logica de la efectividad del daño que recibe un Pokemon, ya que existen Pokemones que son de varios tipos o reciben daño de Pokemon con varios tipos, esta logica del daño final tiene que ser calculada.

### Criterios de aceptación
- [x] Multiplicadores de daño recibido correctos x4, x2, x0.5, x0.25, x0.0.
- [x] Se calcula correctamente para un Pokemon con mas de un tipo.

## Historia 7.3 - Mostrar relaciones de daño en la UI

### Prioridad: ALTA.
### Estado: COMPLETADO.

#### Descripción
Como ususario considero un gran plus, que se muestre en la Pokedex las relaciones de daño entre Pokemones.

### Criterios de aceptación
- [x] UI clara y con adecuado diseño.
- [x] Los tipos se diferencian por colores.
- [x] Se muestran las relaciones de daño de acuerdo al tipo.

# EPICA 8 - Comparador de Pokemones

## Objetivo
Comparar estadisticas, tipos, ventajas y desventajas Pokemon.

## Historia 8.1 - Crear Endpoint comparador

### Prioridad: MEDIA.
### Estado: PENDIENTE.

#### Descripción
Como desarrollador, para poder crear una funcion que compare un Pokemon con otro, es necesario crear el ENDPOINT para buscar.

#### Endpoint
GET /pokemon/compare.

### Criterios de aceptación
- [] Crear Endpoint.

## Historia 8.2 - Se comparan stats

### Prioridad: MEDIA.
### Estado: PENDIENTE.

##### Descripción
Como usuario me gustaria que se puedan comparar las estadisticas de un Pokemon con otro.

### Criterios de aceptación
- [] Se observan diferencias visibles entre un Pokemon y otro.
- [] Se calculan los totales de estadisticas.

## Historia 8.3 - Se comparan tipos

### Prioridad: MEDIA.
### Estado: PENDIENTE.

#### Descripción
Como usuario me gustaria que se puedan comparar los tipos de un Pokemon con otro.

### Criterios de aceptación
- [] Se muestran las ventajas/desventajas entre un Pokemon y otro.

## Hsitoria 8.4 - Se comparan los graficos de radar

### Prioridad: MEDIA.
### Estado: PENDIENTE.

#### Descripción
Como usuario, se veria bien en la UI que se comparen los graficos de radar.

### Criterios de aceptación
- [] Se presenta un grafico comparativo.

# EPICA 9 - Constructor de equipos 

## Objetivo
Crear una funcion que permita crear equipos Pokemon.

## Historia 9.1 - Crear seleccion de equipo

### Prioridad: FUTURO.
### Estado: PENDIENTE.

#### Descripción
Es necesario iniciar con permitir crear el equipo.

### Criterios de aceptación
- [] Se permite seleccionar hasta 6 Pokemones.
- [] Se pueden agregar o quitar los elementos del equipo.

## Historia 9.2 - Análisis de debilidades del equipo

### Prioridad: FUTURO.
### Estado: PENDIENTE.

#### Descripción
El núcleo de crear un constructor de equipos es que se pueda análizar las potencialidades entre los diversos componentes del equipo.

### Criterios de aceptación
- [] Detecta vulnerabilidades.
- [] Calcula coberturas por sus tipos.

## Historia 9.3 - Recomendacion de Pokemon complementario

### Prioridad: FUTURO.
### Estado: PENDIENTE.

#### Descripción
Como usuario, es una herramienta útil en la construccion de un equipo.

### Criterios de aceptación
- [] Sugiere un Pokemon útil de acuerdo a la seleccion del usuario.
- [] Reduce las debilidades del equipo.



# EPICA 10 - Frontend y UI

## Objetivo
Mejorar la experiencia del usuario y otorga una mejor navegación durante la app.

## Historia 10.1 - Crear tarjetas Pokemon

### Prioridad: MEDIA.
### Estado: COMPLETADO.

#### Descripción
Como usuario, mejoraria la experiancia si podria ver el Pokemon desplegado como una carta.

### Criterios de aceptación
- [x] Se crea una carta para presentar el Pokemon.
- [x] Se incluye en la carte Pokemon el name, HP, sprite, attack, defense, sp. attack y sp. defense
- [x] Se muestra una carta que corresponde sus colores con el tipo.

## Historia 10.2 - Implementar el grafico de radar

### Prioridad: MEDIA.
### Estado: COMPLETADO.

#### Descripción
Como parte de la experiencia del usuario es un plus representar las estadisticas del Pokemon en un grafico de radar.

### Criterios de aceptación 
- [x] Se muestra un grafico de radar que se cosntruye con las estadisticas del Pokemon.
- [x] El grafico de radar se representa con los colores del tipo de Pokemon.

## Historia 10.3 - Añadir animaciones

### Prioridad: MEDIA.
### Estado: PENDIENTE.

#### Descripción
Las animaciones suman un plus en la experiencia del usuario.

### Criterios de aceptación
- [] Se implementan animaciones en los graficos y sprites de la app.


# EPICA 11 - Migración a React

## Objetivo
Migrar el frontend desde Streamlit a React+ TypeScript.

## Historia 11.1 - Configurar React 

### Prioridad: FUTURO.
### Estado: PENDIENTE.

#### Descripción
Se necesita una base moderna en React para construir un frontend más escalable y moderno.

### Criterios de aceptación
- [] Proyecto React iniciado.
- [] TypeScript configurado.
- [] Estructura básica de carpetas.
- [] Aplicacion inicia.


## Historia 11.3 - Migrar las páginas principales

### Prioridad: FUTURO.
### Estado: PENDIENTE.

#### Descripción
Migrar las funcionalidades a React

### Criterios de aceptación
- [] Página Home migrada.
- [] Página Pokemon Detail migrada. 
- [] Página Compare migrada.
- [] Página Team Builder migrada.
- [] Se puede navegar por la página.

## Historia 11.4 - Implementar React Router

### Prioridad: FUTURO.
### Estado: PENDIENTE.

#### Descripción
Es necesario para una navegación fluída entre páginas.

### Criterios de aceptación
- [] Instalar React Router.
- [] Configurar rutas.
- [] Navegación SPA funcional.
- [] Manejar rutas inválidas.

# EPICA 12 - Calidad y escalabilidad

## Objetivo
Configurar la app para aplicar aumentar funcionalidades y mejorar la calidad del producto.

## Historia 12.1 - Implementar tests unitarios

### Prioridad: FUTURO.
### Estado: PENDIENTE.

#### Descripción
Se necesitan pruebas unitarias para valorar la lógica individual.

### Criterios de aplicación
- [] Test para services.
- [] Tests para parsers.
- [] Tests ejecutables automaticamente.



## Historia 12.2 - Implementar tests de integración

### Prioridad: FUTURO.
### Estado: PENDIENTE.

#### Descripción
Necesario para validar el funcionamiento entre módulos y endpoints.

### Criterios de aceptación
- [] Tests para endpoints.
- [] Tests para flujo entre frontend-backend.
- [] Respuestas HTTP adecuadas.
- [] Uso de entorno de pruebas.

