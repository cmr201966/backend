# resources.py
from flask_restful import Resource, reqparse
from models import get_users, add_user

class UserList(Resource):
    """Recurso para gestionar la lista de usuarios."""
    def get(self):
        """Devuelve la lista de usuarios."""
        users = get_users()
        return {'users': users}

    def post(self):
        """Crea un nuevo usuario."""
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, help="Username cannot be blank")
        parser.add_argument('email', required=True, help="Email cannot be blank")
        args = parser.parse_args()

        add_user(args['username'], args['email'])
        return {'message': 'User created successfully'}, 201

