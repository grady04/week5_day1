from flask import Flask
from config import Config
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)

# register plugins

# login section

login = LoginManager(app)

# initialize the database

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes