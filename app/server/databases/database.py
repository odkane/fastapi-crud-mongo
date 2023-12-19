import motor.motor_asyncio as motor

# I use here motor instead of MongoClient from PyMongo because
# You should use Motor when you're trying to interact with a MongoDB database in an asynchronous context.
# When you're making something that needs to be asynchronous
# (like a web server, or most commonly from what I've seen here, Discord bots),
# you also want all the database calls to be done asynchronously.
# But pymongo is synchronous, i.e it is blocking, and will block the execution of your asynchronous program
# for the time that it is talking to the database.

# MongoDB connection URL
# MONGO_URL = "mongodb://localhost:27017"
client = motor.AsyncIOMotorClient(host='localhost', port=27017, document_class=dict)
database = client["fast_api_db"]
items_collection = database.get_collection("items")
students_collection = database.get_collection("students")
