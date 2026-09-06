from fastapi import FastAPI, status
from contextlib import asynccontextmanager
from config.db import crear_db_y_tablas
from routers.categoria_router import router as categorias_router
from routers.producto_router import router as productos_router
from routers.rol_router import router as rol_router
from routers.usuario_router import router as usuario_router
from oauth.oauth import router as oauth_router
import models as models


@asynccontextmanager
async def lifespan(app: FastAPI):
    crear_db_y_tablas()
    yield


app = FastAPI(lifespan=lifespan)
app.title = "API Tienda la Cachaca"
app.version = "0.0.1"


@app.get("/",  summary="Comprobando estado de api", status_code=status.HTTP_200_OK)
async def home():
    return {"message": "ok"}

# el parámetro tags sirve para agrupar las rutas en la documentation de fastapi
app.include_router(categorias_router, tags=["categorias"])
app.include_router(productos_router, tags=["productos"])
app.include_router(rol_router, tags=["roles"])
app.include_router(usuario_router, tags=["usuarios"])
app.include_router(oauth_router, tags=["oauth"])
