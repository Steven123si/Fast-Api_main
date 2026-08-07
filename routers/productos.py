from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import seguridad

# El router agrupa los endpoints de productos.
router = APIRouter(prefix="/productos", tags=["Productos"])

# Modelo de entrada (sin id: lo asigna el servidor)
class ProductoEntrada(BaseModel):
    nombre: str
    precio: float
    categoria: str

# "Base de datos" en memoria
productos = [
    {"id": 1, "nombre": "Teclado mecanico", "precio": 120000, "categoria": "Perifericos"},
    {"id": 2, "nombre": "Mouse gamer",      "precio": 85000,  "categoria": "Perifericos"},
    {"id": 3, "nombre": "Monitor 24",       "precio": 650000, "categoria": "Pantallas"},
]

# READ - listar todos (PÚBLICO)          GET /productos
@router.get("")
def listar_productos():
    return productos

# READ - obtener uno (PÚBLICO)           GET /productos/{producto_id}
@router.get("/{producto_id}")
def obtener_producto(producto_id: int):
    for producto in productos:
        if producto["id"] == producto_id:
            return producto
    raise HTTPException(status_code=404, detail="Producto no encontrado")

# CREATE - crear (requiere autenticación) POST /productos
@router.post("", status_code=201)
def crear_producto(
    datos: ProductoEntrada,
    usuario: dict = Depends(seguridad.obtener_usuario_actual)
):
    nuevo_id = max((p["id"] for p in productos), default=0) + 1
    nuevo = {
        "id": nuevo_id,
        "nombre": datos.nombre,
        "precio": datos.precio,
        "categoria": datos.categoria
    }
    productos.append(nuevo)
    return {
        "mensaje": "Producto creado",
        "producto": nuevo,
        "creado_por": usuario["username"]
    }

# UPDATE - actualizar (requiere autenticación) PUT /productos/{producto_id}
@router.put("/{producto_id}")
def actualizar_producto(
    producto_id: int,
    datos: ProductoEntrada,
    usuario: dict = Depends(seguridad.obtener_usuario_actual)
):
    for producto in productos:
        if producto["id"] == producto_id:
            producto["nombre"] = datos.nombre
            producto["precio"] = datos.precio
            producto["categoria"] = datos.categoria
            return {
                "mensaje": "Producto actualizado",
                "producto": producto,
                "actualizado_por": usuario["username"]
            }
    raise HTTPException(status_code=404, detail="Producto no encontrado")

# DELETE - eliminar (requiere rol admin) DELETE /productos/{producto_id}
@router.delete("/{producto_id}")
def eliminar_producto(
    producto_id: int,
    admin: dict = Depends(seguridad.requerir_admin)
):
    for producto in productos:
        if producto["id"] == producto_id:
            productos.remove(producto)
            return {
                "mensaje": "Producto eliminado",
                "producto": producto,
                "eliminado_por": admin["username"]
            }
    raise HTTPException(status_code=404, detail="Producto no encontrado")