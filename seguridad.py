from datetime import datetime, timedelta, timezone
import bcrypt
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from database import obtener_conexion

# Configuración
SECRET_KEY = "clave-super-secreta-de-mas-de-32-caracteres-cambieme"
ALGORITMO = "HS256"
MINUTOS_EXPIRACION = 30

# Hashing de contraseñas con bcrypt
def hashear_password(password: str) -> str:
    hasheado = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hasheado.decode()

def verificar_password(plano: str, hasheado: str) -> bool:
    return bcrypt.checkpw(plano.encode(), hasheado.encode())

# Buscar usuario en la base de datos SQLite por correo
def buscar_usuario(correo: str):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE correo = ?", (correo,))
    fila = cursor.fetchone()
    conexion.close()
    
    if fila:
        return dict(fila)
    return None

# Crear token JWT con la fecha de expiración
def crear_token(correo: str) -> str:
    expira = datetime.now(timezone.utc) + timedelta(minutes=MINUTOS_EXPIRACION)
    return jwt.encode({"sub": correo, "exp": expira}, SECRET_KEY, algorithm=ALGORITMO)

# Le dice a FastAPI dónde se obtiene el token (activa Authorize en /docs)
oauth2_esquema = OAuth2PasswordBearer(tokenUrl="auth/login")

# Dependencia: valida el token JWT y consulta al usuario en la BD
def obtener_usuario_actual(token: str = Depends(oauth2_esquema)):
    error = HTTPException(
        status_code=401, 
        detail="Token inválido",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        datos = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITMO])
        correo = datos.get("sub")
        if correo is None:
            raise error
    except jwt.PyJWTError:
        raise error
    
    usuario = buscar_usuario(correo)
    if usuario is None:
        raise error
        
    return usuario

# Dependencia: exige rol admin
def requerir_admin(usuario: dict = Depends(obtener_usuario_actual)):
    if usuario.get("rol") != "admin":
        raise HTTPException(status_code=403, detail="Requiere rol de administrador")
    return usuario