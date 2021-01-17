from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import time

app = Flask(__name__)

app.config['SECRET_KEY'] = '40f18b06814704e5a62edbf2bd9d41c3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from reminderquipo import routes

# from reminderquipo.scheduler import scheduler

