from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token, create_refresh_token, 
jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
import hashlib
from db import MONGO_BLACKLISTED_TOKENS, MONGO_USERS as mongo_users

parser = reqparse.RequestParser()
parser.add_argument('username', help='This field cannot be blank', required = True)
parser.add_argument('password', help='This field cannot be blank', required = True)

# Get this from config file
password_salt = 'somesecretsalt'

def _hash_password(password):
        '''
        takes password as input, returns salted password.
        '''
        password_salted = str(password) + str(password_salt)
        unicode_salted = password_salted.encode('utf-8')
        hashed_password = str(hashlib.sha512(unicode_salted).hexdigest())
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
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            if not MONGO_BLACKLISTED_TOKENS.db.posts.find_one({'token': jti}):
                MONGO_BLACKLISTED_TOKENS.db.post.insert_one({'token': jti})
                return {'message': 'Access token has been revoked'}
            else:
                return {'message': 'Access token already revoked'}
        except:
            return {'message': 'Something went wrong'}, 500
      
      
class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti)
            revoked_token.add()
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'something went wrong'}, 500

class RevokedTokenModel():
    '''
    This class takes input of jti, needs to clean this up,
    Should add tokens to blacklist and check if tokens are blacklisted
    '''
    def __init__(self, jti):
        self.jti = jti

    def add(self):
        MONGO_BLACKLISTED_TOKENS.db.post.insert_one({'token': self.jti})

    def is_jti_blacklisted(self):
        query = MONGO_BLACKLISTED_TOKENS.db.posts.find_one({'token': self.jti})
        # This might be a bad way of doing it, I'm not shure
        return bool(query)

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        return {'access_token': access_token}
      
# Don't need this     
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