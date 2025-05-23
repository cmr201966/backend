# app.py
#from flask import Flask
from flask import Flask, request, jsonify
import jwt
import datetime
from werkzeug.security import check_password_hash
from flask_restful import Api, Resource
from resources import UserList
from models import init_db
from models import add_user
from models import get_users
from flask_cors import CORS
import os
from dotenv import load_dotenv
import pyodbc

# Crear la aplicación Flask
app = Flask(__name__)

# Cargar variables desde .env
load_dotenv()
# Asignar la clave secreta desde la variable de entorno
app.config['SECRET_KEY'] = os.getenv('VUE_SECRET_KEY')

CORS(app)  


# Crear la API
api = Api(app)

# Inicializar la base de datos
init_db()
add_user("cmr", "cmr201966@gmail.com", "*1235*")
datos=get_users()
print (datos)

# Añadir los recursos (endpoints)
api.add_resource(UserList, '/users')

@app.route('/')
def hello_world():
    return 'Server python con flask...'

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()  # Obtener datos JSON enviados desde el frontend
    username = data.get('username')
    password = data.get('password')
    
    # Verificar usuario y contraseña
    if verify_user_password(username, password):
        token = jwt.encode(
            {'user_id': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)},  # Expira en 1 hora
            app.config['SECRET_KEY'],
            algorithm='HS256'
        )

        return jsonify({'token': token}), 200        
    else:
        return jsonify({"message": "Credenciales incorrectas"}), 401

@app.route('/anuncios', methods=['GET'])
def get_anuncios():
    import sqlite3
    conn = sqlite3.connect('database.db')   
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM anuncios")
    anuncios=cursor.fetchall()
    return jsonify(anuncios)

# Endpoint para obtener un anuncio por su ID
@app.route('/get_anuncio/<int:id>', methods=['GET'])
def get_anuncio(id):
    import sqlite3
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Ejecuta la consulta para obtener el anuncio por ID
    cursor.execute("SELECT * FROM anuncios WHERE id = ?", (id,))
    anuncio = cursor.fetchone()

    # Si no se encuentra el anuncio
    if not anuncio:
        return jsonify({"message": "Anuncio no encontrado"}), 404

    # Si se encuentra el anuncio, devuelve los datos
    anuncio_data = {
        "descripcion": anuncio[1],
        # Agrega aquí los demás campos del anuncio según tu base de datos
    }

    conn.close()
    return jsonify(anuncio_data), 200

# Ruta para insertar o actualizar anuncio
@app.route('/set_anuncio', methods=['POST'])
def save_anuncio():
    import sqlite3
    # Obtener los datos desde la solicitud
    data = request.get_json()  # Suponiendo que los datos están en formato JSON
    descripcion = data.get('descripcion', '')  # Obtener la descripcion del cuerpo de la solicitud
    id = data.get('id', None)  # Obtener el ID si es un update
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    if id is None:  # Si no hay ID, es una inserción (nuevo anuncio)
        cursor.execute("INSERT INTO anuncios (desc) VALUES (?)", (descripcion,))
    else:  # Si hay ID, es una actualización del anuncio
        cursor.execute("UPDATE anuncios SET desc = ? WHERE id = ?", (descripcion, id))

    conn.commit()
    conn.close()
    
    return jsonify({"message": "Anuncio guardado correctamente"}), 200


@app.route('/del_anuncio/<int:id>', methods=['DELETE'])
def delete_anuncio(id):
    import sqlite3
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM anuncios WHERE id = ?", (id,))
    conn.commit()
    return jsonify("ok"), 200

def verify_user_password(username, password):
    # Conexión a la base de datos SQLite
    import sqlite3
    conn = sqlite3.connect('database.db')   
    cursor = conn.cursor()
    
    # Consulta SQL para obtener el usuario por nombre de usuario
    cursor.execute("SELECT username, password FROM users WHERE username = '" +  username + "'")
    user = cursor.fetchone()  # Obtiene el primer registro que coincida

    # Si el usuario no existe, devuelve False
    if (len(user))==0:
        conn.close()  # Cerrar la conexión a la base de datos
        return False
    
    # Si el usuario existe, verifica la contraseña
    stored_username, stored_password = user
    if (stored_password== password):
        conn.close()  # Cerrar la conexión a la base de datos
        return True
    
    conn.close()  # Cerrar la conexión a la base de datos
    return False

def obtener_conexion():
    print ("Conectar....")
    server = '10.240.30.158' 
    database = 'PinkZebra'
    username = 'vladimir.rodriguez'
    password = 'P@sswort10!'
    port = '1433' 
    connection = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};'
                            f'SERVER={server},{port};'
                            f'DATABASE={database};'
                            f'UID={username};'
                            f'PWD={password}')
    print (connection)
    return pyodbc.connect(connection)

# Ruta para obtener datos de ejemplo
@app.route('/get_party/', methods=['GET'])
def obtener_party():
# Configuración de conexión
    server = os.getenv("DB_SERVER")
    database = os.getenv("DB_NAME")
    username = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    port    = os.getenv("DB_PORT")
    try:
       conn = pyodbc.connect(
           'DRIVER={ODBC Driver 17 for SQL Server};'
           f'SERVER={server},{port};'
           f'DATABASE={database};'
           f'UID={username};'
           f'PWD={password}'
        )
       return "Conexión exitosa a la base de datos!"

    except Exception as e:
        return f"Error al conectar con la base de datos: {e}"    
  # Cargar las variables de entorno

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
#    app.run(debug=True, port=8000)
    app.run(debug=True)
