import os 
import sys

current_dir = os.path.dirname(__file__)
sys.path.append(os.path.dirname(current_dir))

from CourseScrapper.CourseScrapper.spiders import UdemySpider,ClassCentralSpider,CourseraSpider,GreatLearningSpider
from YoutubeVideoInfoGetter.YoutubeGetterater import YoutubeVideoInfoGetterater
from WebsiteScrater.WebsiteScrater import WebsiteScrater

from App import app
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import random
random_hex = ''.join(random.choice('0123456789ABCDEF') for _ in range(12))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Note the correct URI format
app.config["SECRET_KEY"] =random_hex
db=SQLAlchemy(app)



@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')
@app.route('/student')
def student():
    return render_template('student.html')

@app.route('/teacher')
def teacher():
    return render_template('teacher.html')

