import os 
import sys
import json

current_dir = os.path.dirname(__file__)
sys.path.append(os.path.dirname(current_dir))

#from CourseScraper.CourseScraper.spiders import UdemySpider,ClassCentralSpider,CourseraSpider,GreatLearningSpider
from CourseScraper.TempCourseScraper import CourseScraper
from YoutubeVideoInfoGetter.YoutubeGetterater import YoutubeVideoInfoGetterater
from WebsiteScrater.WebsiteScrater import WebsiteScrater

from FlaskApp import app
from flask import render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from FlaskApp.forms import SearchForm
import random
random_hex = ''.join(random.choice('0123456789ABCDEF') for _ in range(12))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Note the correct URI format
app.config["SECRET_KEY"] =random_hex
#db=SQLAlchemy(app)


  
@app.route('/',methods=["GET","POST"])
@app.route('/home',methods=["GET","POST"])
def home():
    form = SearchForm()
    if(form.validate_on_submit()):
        if(request.form.get("search_type")=="Websites"):
            websites = WebsiteScrater(form.user_input.data)
            websites_res = json.dumps(websites.get_results())

            #print(websites_res)
            return redirect(url_for('websites',websites_res=websites_res))
        elif(request.form.get("search_type")=="Youtube Videos"):
            yt_videos = YoutubeVideoInfoGetterater(form.user_input.data).get_results()
            youtube_res = json.dumps(yt_videos)

            return redirect(url_for('youtube_videos',youtube_res=youtube_res))
        elif(request.form.get("search_type")=="Courses"):
            courses = CourseScraper(form.user_input.data).scrape_coursera()
            course_res = json.dumps(courses)

            return redirect(url_for('courses',course_res=course_res))


    return render_template('home.html',form=form)

@app.route('/websites',methods=["GET","POST"])
def websites():
    websites_res = json.loads(request.args["websites_res"])
    return render_template('websites.html',websites=websites_res)

@app.route('/youtube_videos',methods=["GET","POST"])
def youtube_videos():
    youtube_res = json.loads(request.args["youtube_res"])
    return render_template('youtube_videos.html',youtube_res=youtube_res)


@app.route('/courses',methods=["GET","POST"])
def courses():
    course_res = json.loads(request.args["course_res"])
    return render_template('courses.html',course_res=course_res)


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

'''@app.route('/search/youtube_videos')
def youtube_videos():
    return render_template("youtube_videos.html")'''

