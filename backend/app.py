from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
from flask import send_from_directory
from flask_pymongo import PyMongo
import os
import datetime
from bson.json_util import dumps
import json

IMAGE_FOLDER = 'IMAGES/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


app = Flask(__name__)
CORS(app)
api = Api(app)

app.config['IMAGE_FOLDER'] = IMAGE_FOLDER
# Setup local mongodb store, will need to split on images, blogposts and users, but will take that later
app.config['MONGO_URI'] = "mongodb://localhost"
mongo_db = PyMongo(app)

mongo_posts = PyMongo(app, uri="mongodb://localhost:27017/posts")

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


class BlogPost(Resource):
    # Create a class to find one slug
    def _find_one_post(self, slug):
        """
        Takes slug as input and searches for a blogpost, if found returns post, else returns false
        """
        blogpost = mongo_posts.db.posts.find_one({"Slug" : slug})
        if blogpost:
            return dumps(blogpost)
        else:
            return None


    def get(self, slug):
        """
        Takes slug input and returns blogpost
        """
        post_name = self._find_one_post(slug)
        json_post = json.loads(post_name)
        return json_post, 200 if post_name else 404


    def post(self):
        """
        This will take a request input of a json, The json needs a Title and a Body key.
        """
        data = request.get_json()
        # Need to rewrite this to check "some more"
        if data.get('Title', None) is not None and data.get('Body', None) is not None:
        # Some sort of check so that I don't duplicate posts.
            slug = { "Slug": str(data.get('Title')).replace(' ','-')}
            only_slug = str(data.get('Title')).replace(' ','-')
            if self._find_one_post(only_slug) is not None:
                response = jsonify({'ok': False, 'message': 'Post with slug title already exists'})
                response.staus_code = 400
                return response
            else:
                jsondata = data
                time_now = str(datetime.datetime.utcnow())
                Created_at = { "Created_at" : time_now }
                # Insert slug and time post has been created into the json.
                jsondata.update(slug)
                jsondata.update(Created_at)
                mongo_posts.db.posts.insert_one(jsondata)
                response = jsonify({'ok': True, 'message': 'Post created successfully!'})
                response.status_code = 200
                return response
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400

    def delete(self, slug):
        post = self._find_one_post(slug)
        if post is not None:
            mongo_posts.db.posts.delete_one({"Slug": slug})
            response = jsonify({'ok': True, 'message': 'post with slug: ' +slug+' is deleted'})
            return response
        else:
            return jsonify({'ok': False, 'message': slug+' not found, nothing deleted'})


class PostList(Resource):
    """
    Returns a list of posts, this will be updated later, will need some 
    funtionality to get the first 5 posts, etc.
    """
    def get(self):
        # This will only return the 20 latest posts, will need to fix this later
        all_posts = dumps(mongo_posts.db.posts.find())
        create_json = json.loads(all_posts)
        response = jsonify({'blog_posts': create_json})
        response.status_code = 200
        return response



api.add_resource(BlogPost, '/post', '/post/<string:slug>')
api.add_resource(PostList, '/posts')
api.add_resource(Images, '/image', '/image/<string:name>')

app.run(port=5000)
