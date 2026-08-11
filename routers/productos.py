from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import seguridad
from database import obtener_conexion

router = APIRouter(prefix="/productos", tags=["Productos"])

# Modelo de entrada: ahora recibe categoria_id (llave foránea)
class ProductoEntrada(BaseModel):
    nombre: str
    precio: float
    categoria_id: int


# READ - listar todos (PÚBLICO)
@router.get("")
def listar_productos():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    cursor.execute("SELECT * FROM productos")
    filas = cursor.fetchall()
    
    conexion.close()
    return [dict(fila) for fila in filas]


# READ - obtener uno por ID (PÚBLICO)
@router.get("/{producto_id}")
def obtener_producto(producto_id: int):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    cursor.execute("SELECT * FROM productos WHERE id = ?", (producto_id,))
    fila = cursor.fetchone()
    
    conexion.close()
    
    if fila is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
        
    return dict(fila)


# CREATE - crear producto (requiere autenticación)
@router.post("", status_code=201)
def crear_producto(
    datos: ProductoEntrada,
    usuario: dict = Depends(seguridad.obtener_usuario_actual)
):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    # 1. Validar integridad de negocio: verificar si la categoría existe
    cursor.execute("SELECT id FROM categorias WHERE id = ?", (datos.categoria_id,))
    if cursor.fetchone() is None:
        conexion.close()
        raise HTTPException(status_code=400, detail="La categoría especificada no existe")
    
    # 2. Insertar el producto
    cursor.execute(
        "INSERT INTO productos (nombre, precio, categoria_id) VALUES (?, ?, ?)",
        (datos.nombre, datos.precio, datos.categoria_id)
    )
    conexion.commit()
    
    nuevo_id = cursor.lastrowid
    conexion.close()
    
    return {
        "mensaje": "Producto creado",
        "producto": {
            "id": nuevo_id,
            "nombre": datos.nombre,
            "precio": datos.precio,
            "categoria_id": datos.categoria_id
        },
        "creado_por": usuario.get("correo") or usuario.get("username")
    }


# UPDATE - actualizar producto (requiere autenticación)
@router.put("/{producto_id}")
def actualizar_producto(
    producto_id: int,
    datos: ProductoEntrada,
    usuario: dict = Depends(seguridad.obtener_usuario_actual)
):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    # 1. Validar integridad de negocio: verificar si la categoría existe
    cursor.execute("SELECT id FROM categorias WHERE id = ?", (datos.categoria_id,))
    if cursor.fetchone() is None:
        conexion.close()
        raise HTTPException(status_code=400, detail="La categoría especificada no existe")
    
    # 2. Actualizar el registro
    cursor.execute(
        "UPDATE productos SET nombre = ?, precio = ?, categoria_id = ? WHERE id = ?",
        (datos.nombre, datos.precio, datos.categoria_id, producto_id)
    )
    
    # Si rowcount vale 0, el ID no existía
    if cursor.rowcount == 0:
        conexion.close()
        raise HTTPException(status_code=404, detail="Producto no encontrado")
        
    conexion.commit()
    conexion.close()
    
    return {
        "mensaje": "Producto actualizado",
        "producto": {
            "id": producto_id,
            "nombre": datos.nombre,
            "precio": datos.precio,
            "categoria_id": datos.categoria_id
        },
        "actualizado_por": usuario.get("correo") or usuario.get("username")
    }


# DELETE - eliminar producto (requiere rol admin)
@router.delete("/{producto_id}")
def eliminar_producto(
    producto_id: int,
    admin: dict = Depends(seguridad.requerir_admin)
):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    cursor.execute("DELETE FROM productos WHERE id = ?", (producto_id,))
    
    # Si rowcount vale 0, el ID no existía
    if cursor.rowcount == 0:
        conexion.close()
        raise HTTPException(status_code=404, detail="Producto no encontrado")
        
    conexion.commit()
    conexion.close()
    
    return {
        "mensaje": "Producto eliminado",
        "id": producto_id,
        "eliminado_por": admin.get("correo") or admin.get("username")
    }