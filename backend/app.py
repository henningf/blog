from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from db import MONGO_POSTS

app = Flask(__name__)
CORS(app)
api = Api(app)

POST_URI = "mongodb://localhost:27017/posts"
MONGO_POSTS.init_app(app, uri=POST_URI)


from blogposts import BlogPost, PostList
from images import Images

api.add_resource(BlogPost, '/post', '/post/<string:slug>')
api.add_resource(PostList, '/posts')
api.add_resource(Images, '/image', '/image/<string:name>')

if __name__=="__main__":
    app.run(port=5000,debug=True)
