"""
Инициализаця приложения
"""
import os

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
# from .models import User, Tag, Post
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

app = Flask(__name__)
app.config.from_object('config')
app.config['UPLOADS_PATH'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOADS_FOLDER'])

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

from . import views
