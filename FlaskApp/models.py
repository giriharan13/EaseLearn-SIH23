from FlaskApp import db
from datetime import datetime,timezone
from flask_login import UserMixin


class Student(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    user_name = db.Column(db.String(25),unique=True,nullable=False)
    email = db.Column(db.String(50),unique=True,nullable=False)
    password = db.Column(db.String(60),nullable=False)

    def __repr__(self):
        return f"Student('{self.user_name}','{self.id}','{self.email}')"
    
    def get_role(self):
        return "STUDENT"
    

class Teacher(db.Model,UserMixin): 
    id = db.Column(db.Integer,primary_key=True)
    user_name = db.Column(db.String(25),unique=True,nullable=False)
    email = db.Column(db.String(50),unique=True,nullable=False)
    type = db.Column(db.String(20),nullable=False)
    password = db.Column(db.String(60),nullable=False)

    def __repr__(self):
        return f"Teacher('{self.user_name}','{self.id}','{self.email}','{self.type}')"
    
    def get_role(self):
        return "TEACHER"
    


    



