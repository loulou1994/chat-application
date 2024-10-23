from flask import Flask
# from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
# socketio = SocketIO(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'home'

from chat_app import routes, models