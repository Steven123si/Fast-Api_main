import sqlite3
import bcrypt

DB_NAME = "tienda.db"

def obtener_conexion():
    """
    Abre la conexión con SQLite.
    check_same_thread=False permite que FastAPI atienda peticiones en hilos distintos.
    row_factory = sqlite3.Row permite acceder a columnas por nombre y dict(fila).
    """
    conexion = sqlite3.connect(DB_NAME, check_same_thread=False)
    conexion.row_factory = sqlite3.Row
    return conexion

def crear_tablas():
    """Crea las tablas en la base de datos si no existen."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    # Habilitar soporte de Llaves Foráneas en SQLite
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Tabla Categorías
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE
    );
    """)

    # Tabla Productos con Llave Foránea a Categorías
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        precio REAL NOT NULL,
        categoria_id INTEGER NOT NULL,
        FOREIGN KEY (categoria_id) REFERENCES categorias (id) ON DELETE CASCADE
    );
    """)

    # Tabla Usuarios
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        correo TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        rol TEXT NOT NULL DEFAULT 'cliente'
    );
    """)

    conexion.commit()
    conexion.close()

def sembrar_datos():
    """Inserta datos de prueba únicamente si la base de datos está vacía."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # Verificar si ya existen categorías
    cursor.execute("SELECT COUNT(*) FROM categorias")
    if cursor.fetchone()[0] == 0:
        # Categorías
        cursor.execute("INSERT INTO categorias (nombre) VALUES ('Electrónica')")
        cursor.execute("INSERT INTO categorias (nombre) VALUES ('Ropa')")
        
        # Productos
        cursor.execute("INSERT INTO productos (nombre, precio, categoria_id) VALUES ('Laptop', 1200.0, 1)")
        cursor.execute("INSERT INTO productos (nombre, precio, categoria_id) VALUES ('Camiseta', 25.0, 2)")

        # Usuarios (Hasheado directo con bcrypt)
        hashed_password = bcrypt.hashpw("admin123".encode(), bcrypt.gensalt()).decode()
        cursor.execute(
            "INSERT INTO usuarios (correo, password, rol) VALUES ('admin@tienda.com', ?, 'admin')", 
            (hashed_password,)
        )

        conexion.commit()
        print("🌱 Datos iniciales sembrados con éxito.")

    conexion.close()