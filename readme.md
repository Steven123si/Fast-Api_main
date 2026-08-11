# API de la Tienda - FastAPI & SQLite

API REST desarrollada con **FastAPI** y **SQLite** para gestionar productos y categorías de una tienda, organizada en routers separados e integrada con autenticación **JWT** y control de acceso basado en roles (RBAC).

## Requisitos

- Python 3.10+
- Git

## Instalación

1. Clona el repositorio e ingresa al directorio del proyecto:
```bash
git clone <url-del-repositorio>
cd Fast-Api-2
```

2. Crea y activa un entorno virtual:

- Linux / macOS / WSL:
```bash
python3 -m venv venv
source venv/bin/activate
```

- Windows (CMD / PowerShell):
```powershell
python -m venv venv
venv\Scripts\activate
```

3. Instala las dependencias necesarias:
```bash
pip install fastapi uvicorn
pip install python-multipart
pip install bcrypt
python -m pip install PyJWT
pip install "passlib[bcrypt]"
pip install email-validator
```

4. Ejecuta el script para poblar y estructurar la base de datos:
```bash
python SQLK/taller_sql.py
```

## Ejecución

Para iniciar el servidor de desarrollo con recarga automática:
```bash
python -m uvicorn main:app --reload
```

Acceso al servicio:
- Servidor base: http://127.0.0.1:8000
- Documentación interactiva (Swagger UI): http://127.0.0.1:8000/docs
- Documentación alternativa (ReDoc): http://127.0.0.1:8000/redoc

## Usuarios de Ejemplo y Roles

Para probar los endpoints protegidos desde Swagger UI (`/docs`), obtén un token desde `/token` usando una de las siguientes cuentas:

| Correo / Usuario | Contraseña | Rol | Permisos |
| :--- | :--- | :--- | :--- |
| `admin@tienda.com` | `admin123` | **admin** | Acceso total (`GET`, `POST`, `PUT`, `DELETE`) |
| `ana@tienda.com` | `ana123` | **cliente** | Lectura y Escritura (`GET`, `POST`, `PUT`) |

## Endpoints de la API

### Autenticación (`/token`)

| Método | Ruta | Descripción | Acceso |
| :--- | :--- | :--- | :--- |
| POST | `/token` | Iniciar sesión y recibir Token JWT | Público |

### Productos (`/productos`)

| Método | Ruta | Descripción | Acceso |
| :--- | :--- | :--- | :--- |
| GET | `/productos` | Listar todos los productos | Público |
| GET | `/productos/{id}` | Obtener un producto por ID | Público |
| POST | `/productos` | Crear un nuevo producto | Autenticado |
| PUT | `/productos/{id}` | Actualizar un producto | Autenticado |
| DELETE | `/productos/{id}` | Eliminar un producto | Rol Admin |

### Categorías (`/categorias`)

| Método | Ruta | Descripción | Acceso |
| :--- | :--- | :--- | :--- |
| GET | `/categorias` | Listar todas las categorías | Público |
| GET | `/categorias/{id}` | Obtener una categoría por ID | Público |
| GET | `/categorias/{id}/productos` | **Reto Extra:** Categoría y lista de sus productos (`JOIN`) | Público |
| POST | `/categorias` | Crear categoría (Nombre único) | Autenticado |
| PUT | `/categorias/{id}` | Actualizar categoría | Autenticado |
| DELETE | `/categorias/{id}` | Eliminar categoría (Verifica integridad relacional) | Rol Admin |

## Criterios de Calidad

- **Seguridad SQL:** Sentencias preparadas con parámetros `?` en todas las consultas para evitar inyección SQL.
- **Manejo de Conexiones:** Cierre garantizado dentro de bloques `finally: conexion.close()` y confirmación de transacciones con `commit()`.
- **Integridad Relacional:** La eliminación de categorías verifica primero que no existan productos vinculados; en caso de haberlos, responde con HTTP 400.
- **Respuestas Estándar:** Manejo explícito de códigos HTTP 200, 201, 400, 401, 403 y 404.

## Exclusiones del Repositorio (.gitignore)

Se ignoran del control de versiones:
- Entorno virtual (`venv/`)
- Base de datos SQLite (`tienda.db`)
- Archivos temporales de Python (`__pycache__/`)

## Autor

**Steven**  
SENA - Centro de Tecnología de la Manufactura Avanzada (CTMA)  
Programa: Análisis y Desarrollo de Software (ADSO) | Ficha: 3169892