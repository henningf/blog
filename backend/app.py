from flask import Flask, request
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)

blog_posts = []

class BlogPost(Resource):
    def get(self, post_name):
        post_name = next(filter(lambda x: x['post_name'] == post_name, blog_posts), None)
        return {'post_name' : post_name}, 200 if post_name else 404


    def post(self, post_name):
        if next(filter(lambda x: x['post_name'] == post_name, blog_posts), None) is not None:
            return {'message': '%s already exists' %post_name}, 400
        data = request.get_json()
        blog_post = {'post_name' : post_name, 'header_text' : data['header_text'], \
            'activation_date' : data['activation_date'], \
            'front_page_text' : data['front_page_text'], \
            'blog_body' : data['blog_body']}
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

app.run(port=5000)
