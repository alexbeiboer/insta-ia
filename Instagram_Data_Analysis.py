# import imageio
# imageio.plugins.ffmpeg.download()
import numpy as np
import time
from datetime import datetime
from InstagramAPI import InstagramAPI
import pandas as pd
import matplotlib.pyplot as plt


class Post:
    def __init__(self, likes = None, year = None,month = None,day = None,hour = None,comment_count = None):
        self.likes = likes
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.comment_count = comment_count


def login(username, password):
    #alexbeiboer
    #Mosmanprep1
    InstagramAPI_ = InstagramAPI(username, password)
    InstagramAPI_.login()

    InstagramAPI_.getProfileData()
    result = InstagramAPI_.LastJson
    user_name = result["user"]["username"]
    # print (result["status"])
    #print (result["user"]["username"])

    #get timeline
    InstagramAPI_.timelineFeed()
    return InstagramAPI_

def analyze_metrics(post_objects):
    months = []
    likess = []
    comment_counts = []
    for object in post_objects:
        month = object.month
        likes = object.likes
        comment_count = object.comment_count
        months.append(month)
        likess.append(likes)
        comment_counts.append(comment_count)
    #format months
    visitied = []
    for i in range(len(months)):
        month = months[i]
        if month in visitied:
            months[i] = int("1" + str(month))
        visitied.append(months[i])


    # df = pd.DataFrame({'likes': likess, "comment_counts":comment_counts},index = months)
    # df=df.astype(float)
    # lines = df.plot.line()
    # # lines = df.plot.line(x=months, y=likess)
    # fig = lines.get_figure()
    # fig.savefig('/Users/2020abeiboer/Documents/Data_Conv2d8839/app/images/likes_months.png')

    # fig = plt.figure()
    # plt.plot(likess, 'r')
    # plt.plot(months, 'g')
    # fig.savefig('/Users/2020abeiboer/Documents/Data_Conv2d8839/app/images/likes_months.png')

def get_metrics (posts):
    likes = []
    top_likers = []
    post_objects = []
    #print (posts[0])
    for post in posts:
        n_likes = post["like_count"]
        comment_count = post["comment_count"]
        date = post["taken_at"]
        post_object = Post()
        post_object.year = datetime.fromtimestamp(date).strftime('%Y')
        post_object.month = datetime.fromtimestamp(date).strftime('%m')
        post_object.day = datetime.fromtimestamp(date).strftime('%d')
        post_object.hour = datetime.fromtimestamp(date).strftime('%H')
        post_object.comment_count = post["comment_count"]
        post_object.likes = n_likes

        post_objecttop_likers = post["top_likers"]
        likes.append(n_likes)
        top_likers.append(post_objecttop_likers[0])
        post_objects.append(post_object)
    mean_likes = np.mean(likes)
    #format top_likers
    top_likers = list(set(top_likers))
    top_likers_str = ""
    for liker in top_likers:
        top_likers_str += liker + ", "
    return mean_likes, top_likers_str, post_objects

def get_posts (InstagramAPI_):
    myposts=[]
    has_more_posts = True
    max_id=""
    while has_more_posts:
        InstagramAPI_.getSelfUserFeed(maxid=max_id)
        if InstagramAPI_.LastJson['more_available'] is not True:
            has_more_posts = False #stop condition
            #print("stopped")
        max_id = InstagramAPI_.LastJson.get('next_max_id','')
        myposts.extend(InstagramAPI_.LastJson['items'])
        #lets server have time to make request
        time.sleep(2)
    return myposts

# posts = get_posts ()
# mean_likes, top_likers, post_objects = get_metrics (posts)
# analyze_metrics(post_objects)
# print ("mean number of likes: " + str(mean_likes))
# print ("Top likers: ")
# for liker in top_likers:
#     print (liker)
