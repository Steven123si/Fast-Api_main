import sqlite3
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
import seguridad
from database import obtener_conexion

router = APIRouter(prefix="/auth", tags=["Autenticacion"])

# Modelo de entrada para el registro
class UsuarioRegistro(BaseModel):
    correo: EmailStr
    password: str

# 1. REGISTRO DE USUARIOS (NUEVO)
@router.post("/registro", status_code=201)
def registrar_usuario(datos: UsuarioRegistro):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    password_encriptada = seguridad.hashear_password(datos.password)
    
    try:
        cursor.execute(
            "INSERT INTO usuarios (correo, password, rol) VALUES (?, ?, 'cliente')",
            (datos.correo, password_encriptada)
        )
        conexion.commit()
        nuevo_id = cursor.lastrowid
    except sqlite3.IntegrityError:
        # Se activa si el correo ya existe por la restricción UNIQUE de la tabla
        conexion.close()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo ya se encuentra registrado"
        )
        
    conexion.close()
    return {
        "mensaje": "Usuario registrado exitosamente",
        "usuario": {"id": nuevo_id, "correo": datos.correo, "rol": "cliente"}
    }

# 2. LOGIN (Actualizado con el campo correo)
@router.post("/login")
def login(datos: OAuth2PasswordRequestForm = Depends()):
    # datos.username recibe el correo ingresado en /docs
    usuario = seguridad.buscar_usuario(datos.username)
    
    if usuario is None or not seguridad.verificar_password(datos.password, usuario["password"]):
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
        
    token = seguridad.crear_token(usuario["correo"])
    return {"access_token": token, "token_type": "bearer"}

# 3. QUIEN SOY (Endpoint protegido)
@router.get("/yo")
def quien_soy(usuario: dict = Depends(seguridad.obtener_usuario_actual)):
    return {
        "id": usuario["id"],
        "correo": usuario["correo"],
        "rol": usuario["rol"]
    }