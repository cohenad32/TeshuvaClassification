from pymongo import MongoClient
import datetime

# create a client to the running mongod client. This connects to default host and port
client = MongoClient()

# connect by giving name of host and port number
client = MongoClient('localhost', 27017)

# connect using URI
client = MongoClient('mongodb://localhost:27017/')

db = client.test_database

# example of a document in mongodb (json style document --> stored as a dictionary)
post = {"author": "Mike",
        "text": "My first blog post!",
        "tags": ["mongodb", "python", "pymongo"],
        "date": datetime.datetime.utcnow()}

# insert document using insert_one() function

posts = db.posts
post_id = posts.insert_one(post).inserted_id
post_id

db.collection_names(include_system_collections=False)
[u'posts']