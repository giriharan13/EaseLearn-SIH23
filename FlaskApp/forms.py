from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,SelectField,PasswordField
from wtforms.validators import DataRequired,Length

class SearchForm(FlaskForm):
    user_input = StringField("Search", validators=[DataRequired()])
    search_type = SelectField('Type', choices=[('Websites'), ('Youtube Videos'), ('Courses')])
    submit = SubmitField("Search")

class LoginForm(FlaskForm):
    user_type = SelectField('Type', choices=[('Student'), ('Teacher')])
    user_name = StringField("Username",validators=[DataRequired(),Length(min=5,max=100)])
    password = PasswordField("Password",validators=[DataRequired(),Length(min=4,max=50)])
    submit = SubmitField("Login")
    

    