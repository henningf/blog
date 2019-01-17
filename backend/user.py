from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token, create_refresh_token, 
jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
import hashlib
from db import MONGO_USERS as mongo_users

parser = reqparse.RequestParser()
parser.add_argument('username', help='This field cannot be blank', required = True)
parser.add_argument('password', help='This field cannot be blank', required = True)

# Get this from config file
password_salt = 'somesecretsalt'

def _hash_password(password):
        '''
        takes password as input, returns salted password.
        '''
        password_salted = str(password) + password_salt
        hashed_password = str(hashlib.sha512(password_salted).hexdigest())
        return hashed_password

class UserRegistration(Resource):
    def post(self):
        '''
        Takes input of username and password, if user
        does not exist in database, saves user in database with salted password
        '''
        data = parser.parse_args()
        if not mongo_users.db.posts.find_one({'username': data.get('username')}):
            username = str(data.get('username'))
            hashed_password = _hash_password(str(data.get('password')))
            jsondata = {'username': username, 'password': hashed_password}
            mongo_users.db.posts.insert_one(jsondata)
            return {'sucess': 'sucess', 'user_created': '{}'.format(username)}
        else:
            username_exists = str('Username {} exists'.format(data.get('username')))
            return {'message': username_exists}

class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()
        # Should draw this out into a model, will look into it later
        user = mongo_users.db.posts.find_one({'username': data.get('username')})
        if not user:
            return {'message': 'User {} doesn\'t exist'.format(data['username'])}
        if user['password'] == _hash_password(data.get('password')):
            access_token = create_access_token(identity = data['username'])
            refresh_token = create_refresh_token(identity = data['username'])
            return {'message': 'Logged in as {}'.format(user['username']),
            'access_token': access_token,
            'refresh_token': refresh_token}
        else:
            return {'message': 'Wrong credentials'}
      
class UserLogoutAccess(Resource):
    def post(self):
        return {'message': 'User logout'}
      
      
class UserLogoutRefresh(Resource):
    def post(self):
        return {'message': 'User logout'}

class TokenRefresh(Resource):
    def post(self):
        return {'message': 'Token refresh'}
      
      
class AllUsers(Resource):
    def get(self):
        return {'message': 'List of users'}

    def delete(self):
        return {'message': 'Delete all users'}
      
      
class SecretResource(Resource):
    def get(self):
        return {
            'answer': 42
}