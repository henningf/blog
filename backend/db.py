from flask_pymongo import PyMongo

# Only used to make a mongo database for posts
MONGO_POSTS = PyMongo()
# Store user data in mongodb
MONGO_USERS = PyMongo()
#  Stores blacklisted tokens
MONGO_BLACKLISTED_TOKENS = PyMongo()
# Store images in mongodb or only metadata, I'll see
MONGO_IMAGES = PyMongo()