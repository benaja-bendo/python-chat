from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.getenv('SECRET_KEY')

db = SQLAlchemy(app)
migrate = Migrate(app=app, db=db, command='migrate')