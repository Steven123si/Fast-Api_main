import sqlite3

# ---------------------------------------------------------
# 1. Conectarse y crear la tabla
# ---------------------------------------------------------
conexion = sqlite3.connect("taller.db")
cursor = conexion.cursor()

# Creamos la tabla si no existe
cursor.execute("""
CREATE TABLE IF NOT EXISTS estudiantes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    edad INTEGER,
    promedio REAL
)
""")
conexion.commit()
print("=== Paso 1: Tabla 'estudiantes' creada ===")


# ---------------------------------------------------------
# 2. Insertar datos
# ---------------------------------------------------------
# Un solo registro con execute()
cursor.execute(
    "INSERT INTO estudiantes (nombre, edad, promedio) VALUES (?, ?, ?)",
    ("Ana Maria", 22, 4.5)
)

# Varios registros a la vez con executemany()
varios_estudiantes = [
    ("Carlos Perez", 19, 3.8),
    ("Sofia Lopez", 24, 4.9),
    ("David Gomez", 21, 3.2),
    ("Laura Torres", 18, 4.1)
]
cursor.executemany(
    "INSERT INTO estudiantes (nombre, edad, promedio) VALUES (?, ?, ?)",
    varios_estudiantes
)

# Guardar los cambios permanentemente
conexion.commit()
print("=== Paso 2: Datos insertados y guardados con commit() ===")


# ---------------------------------------------------------
# 3. Consultar datos
# ---------------------------------------------------------
print("\n=== Paso 3: Consultas ===")

# Todos los registros
cursor.execute("SELECT * FROM estudiantes")
print("Todos los estudiantes (fetchall):")
print(cursor.fetchall())

# Filtro: edad mayor a 20
cursor.execute("SELECT * FROM estudiantes WHERE edad > 20")
print("\nMayores de 20 años:")
print(cursor.fetchall())

# Orden y Límite: Top 3 mejores promedios
cursor.execute("SELECT * FROM estudiantes ORDER BY promedio DESC LIMIT 3")
print("\nTop 3 mejores promedios:")
print(cursor.fetchall())

# Comparación: fetchone() vs fetchall()
cursor.execute("SELECT * FROM estudiantes ORDER BY id ASC")
print("\nProbando fetchone() (trae solo la primera fila):")
print(cursor.fetchone())
print("Probando fetchall() tras fetchone() (trae las filas restantes):")
print(cursor.fetchall())


# ---------------------------------------------------------
# 4. Actualizar y Eliminar
# ---------------------------------------------------------
print("\n=== Paso 4: Actualizar y Eliminar ===")

# Actualizar el promedio del estudiante con ID 1
cursor.execute("UPDATE estudiantes SET promedio = 4.8 WHERE id = ?", (1,))
print("Filas actualizadas (rowcount):", cursor.rowcount)

# Eliminar el estudiante con ID 4
cursor.execute("DELETE FROM estudiantes WHERE id = ?", (4,))
print("Filas eliminadas (rowcount):", cursor.rowcount)

# Guardar cambios
conexion.commit()


# ---------------------------------------------------------
# 5. Leer por nombre de columna (sqlite3.Row)
# ---------------------------------------------------------
print("\n=== Paso 5: Uso de sqlite3.Row ===")

# Cambiamos la fábrica de filas para acceder como diccionario
conexion.row_factory = sqlite3.Row
cursor = conexion.cursor()

cursor.execute("SELECT * FROM estudiantes")
filas = cursor.fetchall()

for fila in filas:
    # Acceso por nombre de columna
    print(f"ID: {fila['id']} | Nombre: {fila['nombre']} | Promedio: {fila['promedio']}")
    # Conversión a diccionario real de Python
    print("  Como dict:", dict(fila))

# Cerramos la conexión al finalizar
conexion.close()