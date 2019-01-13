from flask_restful import Resource, request
from flask import jsonify
from bson.json_util import dumps
import json, datetime
from db import MONGO_POSTS as mongo_posts

class BlogPost(Resource):
    """
    Class for blogposts, used to create, update or delete single blogpost.
    """
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