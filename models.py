# models.py
import sqlite3

def init_db():
    """Inicializa la base de datos si no existe."""
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS anuncios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        desc TEXT NOT NULL
    )
    ''')
    
    conn.commit()
    conn.close()

def get_users():
    """Obtiene todos los usuarios de la base de datos."""
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

def add_user(username, email, password):
    """Añade un nuevo usuario a la base de datos."""
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username='" + username + "'")
    users=cursor.fetchall()
    if len(users) == 0:
       cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
    cursor.execute("SELECT * FROM anuncios")
    anuncios=cursor.fetchall()
    print (anuncios)
    if len(anuncios) == 0:
       print (f"Los crea")
       cursor.execute("INSERT INTO anuncios (desc) VALUES ('Fotos')")
       cursor.execute("INSERT INTO anuncios (desc) VALUES ('Software')")
       cursor.execute("INSERT INTO anuncios (desc) VALUES ('Calzados')")
    
    conn.commit()
    conn.close()

