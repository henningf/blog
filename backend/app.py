from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required
from db import MONGO_POSTS, MONGO_USERS, MONGO_BLACKLISTED_TOKENS

app = Flask(__name__)
CORS(app)
api = Api(app)
jwt = JWTManager(app)

POST_URI = "mongodb://localhost:27017/posts"
MONGO_POSTS.init_app(app, uri=POST_URI)
USERS_URI = "mongodb://localhost:27017/users"
MONGO_USERS.init_app(app, uri=USERS_URI)
BLACKLIST_URI = "mongodb://localhost:27017/blacklisted"
MONGO_BLACKLISTED_TOKENS.init_app(app, uri=BLACKLIST_URI)
app.config['SECRET_KEY'] = 'some-secret-string'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']


from blogposts import BlogPost, PostList
from images import Images
import user

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return user.RevokedTokenModel.is_jti_blacklisted(jti)

# Adding user info
api.add_resource(user.UserRegistration, '/registration')
api.add_resource(user.UserLogin, '/login')
api.add_resource(user.UserLogoutAccess, '/logout/access')
api.add_resource(user.UserLogoutRefresh, '/logout/refresh')
api.add_resource(user.TokenRefresh, '/token/refresh')
api.add_resource(user.AllUsers, '/users')
api.add_resource(user.SecretResource, '/secret')

# Get blog resources
api.add_resource(BlogPost, '/post', '/post/<string:slug>')
api.add_resource(PostList, '/posts')
# Get and post images
api.add_resource(Images, '/image', '/image/<string:name>')

if __name__=="__main__":
    app.run(port=5000,debug=True)
