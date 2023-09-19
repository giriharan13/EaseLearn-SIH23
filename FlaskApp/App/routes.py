from App import app
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import random
random_hex = ''.join(random.choice('0123456789ABCDEF') for _ in range(12))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Note the correct URI format
app.config["SECRET_KEY"] =random_hex
db=SQLAlchemy(app)



class User(db.Model,UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(length=20), nullable=False)
    password =db.Column(db.String(length=80), nullable=False)
    usertype=db.Column(db.String(length=80), nullable=False )

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

