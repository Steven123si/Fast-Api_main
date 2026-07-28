# API de la Tienda - FastAPI

API REST desarrollada con FastAPI para gestionar productos y categorías de una tienda, organizada en routers separados.

## Requisitos

- Python 3.10+
- FastAPI
- Uvicorn

## Instalación

1. Clona el repositorio:
```bash
   git clone <url-del-repositorio>
   cd tienda-api
```

2. Instala las dependencias:
```bash
   pip install fastapi uvicorn
```

## Ejecución

Para levantar el servidor:

```bash
python -m uvicorn main:app --reload
```

La API queda disponible en:
- Servidor: http://127.0.0.1:8000
- Documentación interactiva (Swagger): http://127.0.0.1:8000/docs

## Estructura del proyecto

Endpoints

# Productos (`/productos`)

| Método | Ruta             | Descripción                  |
|--------|------------------|-------------------------------|
| GET    | /productos       | Listar todos los productos    |
| GET    | /productos/{id}  | Obtener un producto por id    |
| POST   | /productos       | Crear un nuevo producto        |
| PUT    | /productos/{id}  | Actualizar un producto         |
| DELETE | /productos/{id}  | Eliminar un producto           |

# Categorías (`/categorias`)

| Método | Ruta              | Descripción                    |
|--------|-------------------|----------------------------------|
| GET    | /categorias       | Listar todas las categorías      |
| GET    | /categorias/{id}  | Obtener una categoría por id     |
| POST   | /categorias       | Crear una nueva categoría         |
| PUT    | /categorias/{id}  | Actualizar una categoría          |
| DELETE | /categorias/{id}  | Eliminar una categoría            |

## Pruebas

Todos los endpoints se probaron manualmente desde `/docs` usando la opción "Try it out", incluyendo:

- Casos exitosos (200/201) para cada operación
- Error 404 al consultar, actualizar o eliminar un id inexistente
- Error 422 al enviar datos inválidos o incompletos en POST/PUT

## Autor

Steven - SENA, ficha 3169892, programa Análisis y Desarrollo de Software (ADSO)