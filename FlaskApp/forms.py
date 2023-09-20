from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,SelectField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    user_input = StringField("Search", validators=[DataRequired()])
    search_type = SelectField('Type', choices=[('Websites'), ('Youtube Videos'), ('Courses')])
    submit = SubmitField("Search")