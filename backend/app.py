from flask import Flask, request, jsonify
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
    def get(self, slug):
        """
        Takes slug input and returns blogpost
        """
        post_name = next(filter(lambda x: x['post_name'] == post_name, blog_posts), None)
        return {'blogpost' : post_name}, 200 if post_name else 404


    def post(self):
        """
        This will need to be rewritten, won't take post as input anymore.
        """
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
    """
    Returns a list of posts, this will be updated later
    """
    def get(self):
        return jsonify({'blog_posts': blog_posts})



api.add_resource(BlogPost, '/post', '/post/<string:post_name>')
api.add_resource(PostList, '/api/v1.0/posts')
api.add_resource(Images, '/image', '/image/<string:name>')

app.run(port=5000)
