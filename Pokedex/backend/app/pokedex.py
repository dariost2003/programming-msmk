from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.core.config import Settings

app=FastAPI(
    tittle=Settings.APP_NAME,
    version=Settings.APP_VERSION,
    description='Proffessional Pokemon API Backend',
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=Settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

#Routers

app.include_router(router)

@app.get('/health')
async def healthcheck():
    return {
        'status': 'ok',
        'app': Settings.APP_NAME,
        'version': Settings.APP_VERSION
    }