from fastapi import FastAPI
from routers import productos, categorias, auth

# 1. Primero instanciamos la aplicación
app = FastAPI(title="API de la Tienda")

# 2. Conectamos los routers
app.include_router(auth.router)
app.include_router(productos.router)
app.include_router(categorias.router)

# 3. Endpoint de inicio
@app.get("/", tags=["Inicio"])
def inicio():
    return {"mensaje": "API de la Tienda funcionando. Visita /docs"}