from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.core.config import settings


app=FastAPI(
    title= settings.APP_NAME,
    version= settings.APP_VERSION,
    description='Proffessional Pokemon API Backend',
)

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins= settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Registro de rutas
app.include_router(router)

# Verifica el estado del backend
@app.get('/health', tags=['Health'])
async def healthcheck() -> dict[str, str]:
    return {
        'status': 'ok',
        'app': settings.APP_NAME,
        'version': settings.APP_VERSION
    }

# Se inicializa el servidor
@app.on_event('startup')
async def startup_event() -> None:

    # Evento que se ejecuta al iniciar la aplicación
    print(f'{settings.APP_NAME} v{settings.APP_VERSION} inicializado correctamente')
    