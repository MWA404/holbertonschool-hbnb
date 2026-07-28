from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace('users', description='User operations')

facade = HBnBFacade()

user_model = api.model('User', {
    'id': fields.String(readOnly=True, description='User ID'),
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name'),
    'email': fields.String(required=True, description='Email address'),
    'password': fields.String(required=True, description='User password')
})


@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    def post(self):
        """Register a new user."""
        data = api.payload
        existing_user = facade.get_user_by_email(data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        user = facade.create_user(data)
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 201

    def get(self):
        """Retrieve all users without password field."""
        users = facade.get_all_users()
        return [{
            'id': u.id,
            'first_name': u.first_name,
            'last_name': u.last_name,
            'email': u.email
        } for u in users], 200


@api.route('/<user_id>')
class UserResource(Resource):
    def get(self, user_id):
        """Get user details by ID without password."""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200
