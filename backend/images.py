from flask_restful import Resource, request
from flask import send_from_directory
import os

# Load this from a config file, or app.py
IMAGE_FOLDER = 'IMAGES/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

images = []

class Images(Resource):
    """
    Pointers to image will be stored in a database,
    the images will be stored and served from disk.

    Note, the post DOES NOT store info in database yet

    PS: Need to harden this code, as it is not safe as of now.
    """
    def get(self, name):
        return send_from_directory(IMAGE_FOLDER,name)
 
    def post(self):
        if 'file' not in request.files:
            return {"Error": "No file in request"}, 404
        image_file = request.files['file']
        name = image_file.filename
        image_file.seek(0)
        image_file.save(os.path.join(IMAGE_FOLDER, name))
        return {"image saved": name}, 200
 
    def delete(self, name):
        os.remove(os.path.join(IMAGE_FOLDER, name))
        return {"image deleted ": name}, 200

    # Using this to check for allowed extensions
    def allowed_file(self, filename):
        return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS