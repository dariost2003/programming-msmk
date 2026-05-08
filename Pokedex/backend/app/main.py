from fastapi import FastAPI

from app.api.routes import router
from app.core.config import Settings

app = FastAPI(
    tittle=Settings.APP_NAME,
    version=Settings.APP_VERSION,
)

app.include_router(router)

@app.get('/health')
def health():
    return {'status': 'ok'}