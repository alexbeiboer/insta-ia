from flask import *
from app import app,Instagram_Data_Analysis
from flask import Flask, render_template, request
import sys
import os


#
# UPLOAD_FOLDER = os.path.basename('images')
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/display_data', methods=['GET', "POST"])
def display_data():
    user_data = dict (request.form)
    username = user_data["username"]
    password = user_data["password"]
    #login with username and password entered into form
    InstagramAPI_ = Instagram_Data_Analysis.login(username, password)
    #get posts
    posts = Instagram_Data_Analysis.get_posts(InstagramAPI_)
    # #get post metric
    mean_likes, top_likers, post_objects = Instagram_Data_Analysis.get_metrics(posts)
    print (top_likers)
    # #analyse metrics
    Instagram_Data_Analysis.analyze_metrics(post_objects)
    #full_filename = os.path.join(app.config['UPLOAD_FOLDER'], '/Users/2020abeiboer/Documents/Data_Conv2d8839/app/images/likes_months.png')
    return render_template('display_data.html', output_filepath = "../static/likes_months.png", avg_likes = "Mean number of likes: " + str(int(mean_likes)), top_likers = top_likers)
    #return render_template('display_data.html')
