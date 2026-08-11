# API de la Tienda - FastAPI & SQLite

API REST desarrollada con **FastAPI** y **SQLite** para gestionar productos y categorías de una tienda online, organizada en routers independientes (`APIRouter`) e integrada con autenticación mediante tokens **JWT** y control de acceso basado en roles (RBAC).

## Requisitos Previos

- Python 3.10 o superior
- Pip (gestor de paquetes de Python)
- Git

## Instalación

1. **Clona el repositorio e ingresa al directorio del proyecto:**
   ```bash
   git clone <url-del-repositorio>
   cd Fast-Api-2
   ```

2. **Instala las dependencias requeridas:**
```bash
   pip install fastapi uvicorn
   pip install python-multipart
   pip install bcrypt
   pip install PyJWT
   pip install "passlib[bcrypt]"
   pip install email-validator
```

3. **Poblar y estructurar la base de datos:**
   ```bash
   python SQLK/taller_sql.py
   ```

## Ejecución del Servidor

Para iniciar el servidor local en modo desarrollo con recarga automática:

```bash
python -m uvicorn main:app --reload
```

Acceso al servicio:
- **Servidor Base:** http://127.0.0.1:8000
- **Documentación Interactiva (Swagger UI):** http://127.0.0.1:8000/docs
- **Documentación Alternativa (ReDoc):** http://127.0.0.1:8000/redoc

## Usuario de Ejemplo (Autenticación)

Para interactuar con los endpoints protegidos desde Swagger UI (`/docs`), obtén un token enviando credenciales a `/token` con la siguiente cuenta de prueba:

| Correo / Usuario | Contraseña | Rol | Permisos |
| :--- | :--- | :--- | :--- |
| `admin@tienda.com` | `admin123` | **admin** | Acceso total (`GET`, `POST`, `PUT`, `DELETE`) |

## Endpoints de la API

### Autenticación (`/token`)

| Método | Ruta | Descripción | Acceso |
| :--- | :--- | :--- | :--- |
| `POST` | `/token` | Iniciar sesión y recibir Token JWT | Público |

### Productos (`/productos`)

| Método | Ruta | Descripción | Acceso |
| :--- | :--- | :--- | :--- |
| `GET` | `/productos` | Listar todos los productos | Público |
| `GET` | `/productos/{id}` | Obtener un producto por ID | Público |
| `POST` | `/productos` | Crear un nuevo producto | Autenticado |
| `PUT` | `/productos/{id}` | Actualizar un producto | Autenticado |
| `DELETE` | `/productos/{id}` | Eliminar un producto | Exclusivo Admin |

### Categorías (`/categorias`)

| Método | Ruta | Descripción | Acceso |
| :--- | :--- | :--- | :--- |
| `GET` | `/categorias` | Listar todas las categorías | Público |
| `GET` | `/categorias/{id}` | Obtener una categoría por ID | Público |
| `GET` | `/categorias/{id}/productos` | Obtener categoría y la lista de sus productos (`JOIN`) | Público |
| `POST` | `/categorias` | Crear categoría (Restricción `UNIQUE` en nombre) | Autenticado |
| `PUT` | `/categorias/{id}` | Actualizar categoría | Autenticado |
| `DELETE` | `/categorias/{id}` | Eliminar categoría (Protección de integridad relacional) | Exclusivo Admin |

## Criterios de Calidad y Seguridad

- **Seguridad contra Inyección SQL:** Todas las consultas utilizan sentencias preparadas con parámetros posicionados `?`.
- **Manejo de Recursos y Conexiones:** Cierre garantizado mediante bloques `finally: conexion.close()` y confirmación explícita con `commit()`.
- **Integridad Relacional:** La eliminación de categorías verifica la ausencia de productos asociados; de lo contrario, responde con HTTP 400.
- **Manejo de Errores e Indicadores HTTP:** Implementación de respuestas estándar `200 OK`, `201 Created`, `400 Bad Request`, `401 Unauthorized`, `403 Forbidden` y `404 Not Found`.

## Exclusiones del Repositorio (.gitignore)

Se ignoran del control de versiones los archivos volátiles y locales:
- Base de datos SQLite (`tienda.db`)
- Archivos temporales y de caché (`__pycache__/`, `*.pyc`)
- Configuración de editor local (`.vscode/`, `.idea/`)

## Autor

**Steven**  
SENA - Centro de Tecnología de la Manufactura Avanzada (CTMA)  
Programa: Análisis y Desarrollo de Software (ADSO) | Ficha: 3169892
