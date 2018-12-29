from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
from flask import send_from_directory
import os

IMAGE_FOLDER = 'IMAGES/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


app = Flask(__name__)
CORS(app)
api = Api(app)

app.config['IMAGE_FOLDER'] = IMAGE_FOLDER

blog_posts = []
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
    def get(self, post_name):
        post_name = next(filter(lambda x: x['post_name'] == post_name, blog_posts), None)
        return {'blogpost' : post_name}, 200 if post_name else 404


    def post(self, post_name):
        if next(filter(lambda x: x['post_name'] == post_name, blog_posts), None) is not None:
            return {'message': '%s already exists' %post_name}, 400
        data = request.get_json()
        blog_post = {'post_name' : post_name, 'header_text' : data['header_text'], \
          'activation_date' : data['activation_date'], 'front_page_text' : data['front_page_text'], 'blog_body' : data['blog_body'] }
        blog_posts.append(blog_post)
        return blog_post, 201

    def delete(self, blog_post):
        # Create new list that removes the name from the list
        global blog_posts
        blog_posts = list(filter(lambda x: x['blog_post'] != blog_post, blog_posts))
        return {'message': blog_post + ' is deleted'}


class PostList(Resource):
    def get(self):
        return {'blog_posts': blog_posts}



api.add_resource(BlogPost, '/post/<string:post_name>')
api.add_resource(PostList, '/posts')
api.add_resource(Images, '/image', '/image/<string:name>')

app.run(port=5000)
