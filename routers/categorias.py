import sqlite3
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from database import obtener_conexion
import seguridad

router = APIRouter(prefix="/categorias", tags=["Categorias"])

class CategoriaEntrada(BaseModel):
    nombre: str

# GET /categorias (PÚBLICO) - Retorna todas las categorías
@router.get("")
def listar_categorias():
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT id, nombre FROM categorias")
        filas = cursor.fetchall()
        return [dict(fila) for fila in filas]
    finally:
        conexion.close()

# GET /categorias/{categoria_id} (PÚBLICO) - Obtiene una por ID
@router.get("/{categoria_id}")
def obtener_categoria(categoria_id: int):
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT id, nombre FROM categorias WHERE id = ?", (categoria_id,))
        categoria = cursor.fetchone()
        if not categoria:
            raise HTTPException(status_code=404, detail="Categoria no encontrada")
        return dict(categoria)
    finally:
        conexion.close()

# GET /categorias/{categoria_id}/productos (RETO EXTRA) - JOIN con productos
@router.get("/{categoria_id}/productos")
def obtener_categoria_con_productos(categoria_id: int):
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT 
                c.id AS cat_id, 
                c.nombre AS cat_nombre,
                p.id AS prod_id, 
                p.nombre AS prod_nombre, 
                p.precio AS prod_precio
            FROM categorias c
            LEFT JOIN productos p ON c.id = p.categoria_id
            WHERE c.id = ?
        """, (categoria_id,))
        filas = cursor.fetchall()

        if not filas:
            raise HTTPException(status_code=404, detail="Categoria no encontrada")

        cat_id = filas[0]["cat_id"]
        cat_nombre = filas[0]["cat_nombre"]

        productos = []
        for fila in filas:
            if fila["prod_id"] is not None:
                productos.append({
                    "id": fila["prod_id"],
                    "nombre": fila["prod_nombre"],
                    "precio": fila["prod_precio"]
                })

        return {
            "id": cat_id,
            "nombre": cat_nombre,
            "productos": productos
        }
    finally:
        conexion.close()

# POST /categorias (requiere AUTENTICACIÓN) - Inserta en SQLite
@router.post("", status_code=201)
def crear_categoria(
    datos: CategoriaEntrada, 
    usuario: dict = Depends(seguridad.obtener_usuario_actual)
):
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO categorias (nombre) VALUES (?)", (datos.nombre,))
        conexion.commit()
        nuevo_id = cursor.lastrowid
        return {
            "mensaje": "Categoria creada", 
            "categoria": {"id": nuevo_id, "nombre": datos.nombre},
            "creada_por": usuario.get("correo") or usuario.get("username")
        }
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=400, 
            detail="Ya existe una categoría con ese nombre."
        )
    finally:
        conexion.close()

# PUT /categorias/{categoria_id} (requiere AUTENTICACIÓN) - Actualiza en SQLite
@router.put("/{categoria_id}")
def actualizar_categoria(
    categoria_id: int, 
    datos: CategoriaEntrada, 
    usuario: dict = Depends(seguridad.obtener_usuario_actual)
):
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute(
            "UPDATE categorias SET nombre = ? WHERE id = ?", 
            (datos.nombre, categoria_id)
        )
        conexion.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Categoria no encontrada")

        return {
            "mensaje": "Categoria actualizada", 
            "categoria": {"id": categoria_id, "nombre": datos.nombre},
            "actualizada_por": usuario.get("correo") or usuario.get("username")
        }
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=400, 
            detail="Ya existe otra categoría con este nombre."
        )
    finally:
        conexion.close()

# DELETE /categorias/{categoria_id} (requiere ROL ADMIN) - Verifica FKs antes de borrar
@router.delete("/{categoria_id}")
def eliminar_categoria(
    categoria_id: int, 
    admin: dict = Depends(seguridad.requerir_admin)
):
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()

        # Validar si existen productos asociados
        cursor.execute("SELECT COUNT(*) FROM productos WHERE categoria_id = ?", (categoria_id,))
        total_productos = cursor.fetchone()[0]

        if total_productos > 0:
            raise HTTPException(
                status_code=400, 
                detail=f"No se puede eliminar la categoría porque tiene {total_productos} producto(s) asociado(s). Reasigne o elimine los productos primero."
            )

        cursor.execute("DELETE FROM categorias WHERE id = ?", (categoria_id,))
        conexion.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Categoria no encontrada")

        return {
            "mensaje": "Categoria eliminada", 
            "id": categoria_id,
            "eliminada_por": admin.get("correo") or admin.get("username")
        }
    finally:
        conexion.close()