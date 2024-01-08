from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__, static_url_path='/static')
app.config.from_object(Config)
app.secret_key = os.getenv('SECRET_KEY')
CORS(app, resources={r"/*": {"origins": "*"}})

db = SQLAlchemy(app)
migrate = Migrate(app=app, db=db, command='migrate')