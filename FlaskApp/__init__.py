from flask import Flask
from flask import render_template, url_for
from flask_sqlalchemy import  SQLAlchemy
from flask_login import LoginManager
import os
import random


random_hex = ''.join(random.choice('0123456789ABCDEF') for _ in range(12))
app = Flask(__name__)
app.config["SECRET_KEY"] = random_hex
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db" 
db = SQLAlchemy()
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view= "login"

from FlaskApp import routes

