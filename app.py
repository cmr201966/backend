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
    return 'Hola...'

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
    print ("Anuncios")
    print (anuncios)
    return jsonify(anuncios)

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
