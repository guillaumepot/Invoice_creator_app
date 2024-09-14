import os

host= os.getenv('FLASK_HOST', '0.0.0.0')
port= os.getenv('FLASK_PORT', 5000)

mongo_host= os.getenv('MONGO_HOST', 'localhost')
mongo_port= os.getenv('MONGO_PORT', 27017)