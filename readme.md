```markdown
# API de la Tienda - FastAPI

API REST desarrollada con FastAPI para gestionar productos y categorías de una tienda, organizada en routers separados e integrada con autenticación JWT y control de acceso basado en roles (RBAC).

## Requisitos

- Python 3.10+
- FastAPI
- Uvicorn

## Instalación

1. Clona el repositorio:
```bash
git clone <url-del-repositorio>
cd Fast-Api-2

```

2. (Recomendado) Crea y activa un entorno virtual:

```bash
# En Linux / macOS / WSL:
python3 -m venv venv
source venv/bin/activate

# En Windows (CMD / PowerShell):
python -m venv venv
venv\Scripts\activate

```

3. Instala las dependencias:

```bash
pip install fastapi uvicorn

```

> *Nota: Si la terminal no reconoce el comando `pip`, ejecuta `python -m pip install fastapi uvicorn` o `py -m pip install fastapi uvicorn`.*

## Ejecución

Para levantar el servidor:

```bash
python -m uvicorn main:app --reload

```

La API queda disponible en:

* Servidor: http://127.0.0.1:8000
* Documentación interactiva (Swagger): http://127.0.0.1:8000/docs

## Seguridad y Control de Acceso

La aplicación implementa protección de rutas mediante **JWT (JSON Web Tokens)** y middleware de autorización mediante dependencias (`Depends`):

* **Acceso Público:** Lectura de información (`GET`).
* **Requiere Autenticación:** Creación y edición de registros (`POST`, `PUT`).
* **Requiere Rol Administrador:** Eliminación de registros (`DELETE`).

---

## Endpoints

### Autenticación (`/token`)

| Método | Ruta | Descripción | Acceso |
| --- | --- | --- | --- |
| POST | /token | Iniciar sesión y obtener token de acceso JWT | Público |

### Productos (`/productos`)

| Método | Ruta | Descripción | Acceso |
| --- | --- | --- | --- |
| GET | /productos | Listar todos los productos | Público |
| GET | /productos/{id} | Obtener un producto por id | Público |
| POST | /productos | Crear un nuevo producto | Autenticado |
| PUT | /productos/{id} | Actualizar un producto | Autenticado |
| DELETE | /productos/{id} | Eliminar un producto | Rol Admin |

### Categorías (`/categorias`)

| Método | Ruta | Descripción | Acceso |
| --- | --- | --- | --- |
| GET | /categorias | Listar todas las categorías | Público |
| GET | /categorias/{id} | Obtener una categoría por id | Público |
| POST | /categorias | Crear una nueva categoría | Autenticado |
| PUT | /categorias/{id} | Actualizar una categoría | Autenticado |
| DELETE | /categorias/{id} | Eliminar una categoría | Rol Admin |

---

## Pruebas

Todos los endpoints se probaron manualmente desde Swagger UI (`/docs`) validando los flujos de seguridad:

* **Sin Token (401 Unauthorized):** Verificado al intentar operaciones `POST`, `PUT` o `DELETE` sin estar autenticado.
* **Usuario Estándar:** Verificada la creación y actualización exitosa (`201/200`), así como la restricción de borrado (`403 Forbidden`).
* **Usuario Administrador:** Verificada la eliminación exitosa de recursos (`200 OK`).
* **Manejo de errores comunes:** Respuestas `404 Not Found` para IDs inexistentes y `422 Unprocessable Entity` para esquemas de datos inválidos.

## Autor

Steven - SENA, ficha 3169892, programa Análisis y Desarrollo de Software (ADSO)

```

```