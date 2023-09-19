from flask import Flask
from flask import render_template, url_for
from flask_sqlalchemy import  SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)

#app.config["SQLALCHEMY_DATABASE_URI"] =  os.environ["DATABASE_URI"]
#db = SQLAlchemy()
#db.init_app(app)
#login_manager = LoginManager(app)
#login_manager.login_view= "login"

from App import routes

