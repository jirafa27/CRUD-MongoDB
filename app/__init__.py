from flask import Flask
from flask_bootstrap import Bootstrap
import pymongo



app = Flask(__name__)
app.config.from_object('config')
Bootstrap(app)
client = pymongo.MongoClient('localhost', 27017)
db = client['TasksDB']
from app import views
