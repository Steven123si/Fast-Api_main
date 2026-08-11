from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import crear_tablas, sembrar_datos
from routers import productos, categorias, auth

# 1. Definimos la función lifespan para inicializar la base de datos al arrancar
@asynccontextmanager
async def lifespan(app: FastAPI):
    crear_tablas()   # Crea las tablas si no existen
    sembrar_datos()  # Inserta datos iniciales de prueba si está vacía
    yield

# 2. Instanciamos la aplicación pasando el parámetro lifespan
app = FastAPI(title="API de la Tienda", lifespan=lifespan)

# 3. Conectamos los routers
app.include_router(auth.router)
app.include_router(productos.router)
app.include_router(categorias.router)

# 4. Endpoint de inicio
@app.get("/", tags=["Inicio"])
def inicio():
    return {"mensaje": "API de la Tienda funcionando. Visita /docs"}