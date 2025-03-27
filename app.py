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

# Crear la aplicación Flask
app = Flask(__name__)
CORS(app)  

app.config['SECRET_KEY'] = '*123571113*'

# Crear la API
api = Api(app)

# Inicializar la base de datos
init_db()
add_user("cmr", "cmr201966@gmail.com", "*123571113*")
datos=get_users()
for usuario in datos:
    print(f"Username: {usuario[1]}, Email: {usuario[2]}, Password: {usuario[3]}")

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
    print ("DELETE FROM anuncios WHERE id = ?", (id,))
    cursor.execute("DELETE FROM anuncios WHERE id = ?", (id,))
    conn.commit()
    print ("Borro")
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


if __name__ == '__main__':
    app.run(debug=True, port=5000)
    app.run(debug=True)
