import os 
import sys
import json

current_dir = os.path.dirname(__file__)
sys.path.append(os.path.dirname(current_dir))

#from CourseScraper.CourseScraper.spiders import UdemySpider,ClassCentralSpider,CourseraSpider,GreatLearningSpider
from CourseScraper.TempCourseScraper import CourseScraper
from YoutubeVideoInfoGetter.YoutubeGetterater import YoutubeVideoInfoGetterater
from WebsiteScrater.WebsiteScrater import WebsiteScrater

from FlaskApp import app,login_manager
from flask import render_template,redirect,url_for,request,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin,current_user,login_required
from FlaskApp.forms import SearchForm,LoginForm
from FlaskApp.models import Teacher,Student
from FlaskApp import app


  
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


@app.route('/login',methods=["POST","GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("hub"))
    form = LoginForm()
    if(form.validate_on_submit()):
        if(request.form.get("user_type")=="Student"):
            student = Student.query.filter_by(user_name=form.user_name.data).first()
            print("hello")
            if (student and student.password==form.password.data):
                login_user(student.id,0)
                flash(f"green : Successfully logged in as {student.user_name}")
                return redirect(url_for("hub", form=form))
            else:
                print("failed")
                flash("red : Doesnt exist or Invalid password")
        elif(request.form.get("user_type")=="Teacher"):
            teacher = Teacher.query.filter_by(user_name=form.user_name.data).first()
            print("hello")
            if (teacher and teacher.password==form.password.data):
                login_user(teacher.id,1)
                flash(f"green : Successfully logged in as {teacher.user_name}")
                return redirect(url_for("hub", form=form))
            else:
                print("failed")
                flash("red : Doesnt exist or Invalid password")
    return render_template("login.html",title="login",form=form)

@login_manager.user_loader
def login_user(u_id,user_type):
    if(user_type==0):
        return Student.query.filter_by(id=u_id).first()
    else:
        return Teacher.query.filter_by(id=u_id).first()



@app.route('/register')
def register():
    return render_template('register.html')

@login_required
@app.route('/hub')
def hub():
    teachers = Teacher.query.all()
    return render_template("hub.html",teachers=teachers)

@app.route('/student')
def student():
    return render_template('student.html')

@app.route('/teacher')
def teacher():
    return render_template('teacher.html')

'''@app.route('/search/youtube_videos')
def youtube_videos():
    return render_template("youtube_videos.html")'''

