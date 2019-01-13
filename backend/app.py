from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
from flask import send_from_directory
import os
import datetime
from bson.json_util import dumps
import json
from db import MONGO_POSTS

IMAGE_FOLDER = 'IMAGES/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


app = Flask(__name__)
CORS(app)
api = Api(app)

app.config['IMAGE_FOLDER'] = IMAGE_FOLDER
# Setup local mongodb store, will need to split on images, blogposts and users, but will take that later
app.config['MONGO_URI'] = "mongodb://localhost"
#mongo_db = PyMongo(app)

POST_URI = "mongodb://localhost:27017/posts"
MONGO_POSTS.init_app(app, uri=POST_URI)

"""
blog_posts = [{"ID": "1", "Title": "my first blogpost","Slug": "my-first-blogpost","Body": "<h1>test</h1> <br> <b>test2</b>",
"feature_image": "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/intermediary/f/65a25b7b-5ce1-488b-a377-d71689d07659/d1xmvaz-11288f67-c6c2-4330-a075-74e288310327.jpg",
"Feature_text": "This is my first blogpost", "Created_at":  "2018-12-15T12:36:28.363Z"},
{"ID": "2","Title": "my second blogpost","Slug": "my-second-blogpost","Body": "<h1>test</h1> <br> <b>test2</b>",
"feature_image": "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/intermediary/f/65a25b7b-5ce1-488b-a377-d71689d07659/d1xmvaz-11288f67-c6c2-4330-a075-74e288310327.jpg",
"Feature_text": "This is my second blogpost", "Created_at":  "2018-12-16T12:36:28.363Z"},
{"ID": "3","Title": "my third blogpost","Slug": "my-third-blogpost","Body": "<h1>test</h1> <br> <b>test2</b>",
"feature_image": "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/intermediary/f/65a25b7b-5ce1-488b-a377-d71689d07659/d1xmvaz-11288f67-c6c2-4330-a075-74e288310327.jpg",
"Feature_text": "This is my third blogpost", "Created_at":  "2018-12-17T12:36:28.363Z"},
{"ID": "4","Title": "my fourth blogpost","Slug": "my-fourth-blogpost","Body": "<h1>test</h1> <br> <b>test2</b>",
"feature_image": "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/intermediary/f/65a25b7b-5ce1-488b-a377-d71689d07659/d1xmvaz-11288f67-c6c2-4330-a075-74e288310327.jpg",
"Feature_text": "This is my fourth blogpost", "Created_at":  "2018-12-18T12:36:28.363Z"},
{"ID": "5","Title": "my fifth blogpost","Slug": "my-fifth-blogpost","Body": "<h1>test</h1> <br> <b>test2</b>",
"feature_image": "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/intermediary/f/65a25b7b-5ce1-488b-a377-d71689d07659/d1xmvaz-11288f67-c6c2-4330-a075-74e288310327.jpg",
"Feature_text": "This is my fifth blogpost", "Created_at":  "2018-12-19T12:36:28.363Z"}]
"""
images = []



class Images(Resource):
    """
    Pointers to image will be stored in a database,
    the images will be stored and served from disk.

    Note, the post DOES NOT store info in database yet

    PS: Need to harden this code, as it is not safe as of now.
    """
    def get(self, name):
        return send_from_directory(app.config['IMAGE_FOLDER'],
                               name)
 
    def post(self):
        if 'file' not in request.files:
            return {"Error": "No file in request"}, 404
        image_file = request.files['file']
        name = image_file.filename
        image_file.seek(0)
        image_file.save(os.path.join(app.config['IMAGE_FOLDER'], name))
        return {"image saved": name}, 200
 
    def delete(self, name):
        os.remove(os.path.join(app.config['IMAGE_FOLDER'], name))
        return {"image deleted ": name}, 200

    # Using this to check for allowed extensions
    def allowed_file(self, filename):
        return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


from blogposts import BlogPost, PostList

api.add_resource(BlogPost, '/post', '/post/<string:slug>')
api.add_resource(PostList, '/posts')
api.add_resource(Images, '/image', '/image/<string:name>')

if __name__=="__main__":
    app.run(port=5000,debug=True)
