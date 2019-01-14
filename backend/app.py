from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from db import MONGO_POSTS, MONGO_USERS

app = Flask(__name__)
CORS(app)
api = Api(app)

POST_URI = "mongodb://localhost:27017/posts"
MONGO_POSTS.init_app(app, uri=POST_URI)
USERS_URI = "mongodb://localhost:27017/users"
MONGO_USERS.init_app(app, USERS_URI)
app.config['SECRET_KEY'] = 'some-secret-string'


from blogposts import BlogPost, PostList
from images import Images
import user

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
