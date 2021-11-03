# remember to: source env/bin/activate
# to see the website : export FLASK_ENV=development; flask run
# http://localhost:5000
# Start DB with: brew services start mongodb-community@5.0 
# Stop DB with: brew services stop mongodb-community@5.0
# https://playlister-arg.herokuapp.com/
# heroku create playlister-arg
# https://playlister-arg.herokuapp.com/ | https://git.heroku.com/playlister-arg.git
# https://playlister-arg.herokuapp.com/
# Push updated app to Heroku : git add . // then git commit // git push heroku main


from flask import Flask, render_template, redirect, url_for, request
from bson.objectid import ObjectId
from pymongo import MongoClient
from dotenv import load_dotenv
import os
# pip install dnspython
# pip3 install certifi
import certifi
# Info from wd3.myworkday.com/shopify/d/home.htmld and https://medium.com/analytics-vidhya/deploy-a-web-api-with-python-flask-and-mongodb-on-heroku-in-10-mins-71c4571c505d

ca = certifi.where()
app = Flask(__name__)
host = os.environ.get('MONGODB_URI') 
DATABASE_URL = f'mongodb+srv://alexross:{os.environ.get("password")}@cluster0.c3gdz.mongodb.net/Cluster0?retryWrites=true&w=majority'

client = MongoClient(DATABASE_URL, tlsCAFile=ca)
db = client.Playlister
# MongoDB Database collections
playlists = db.playlists
comments = db.comments
load_dotenv()

@app.route('/')
def playlists_index():
    return render_template('playlists_index.html', playlists=playlists.find())

@app.route('/playlists/new')
def playlists_new():
    playlist = {
        'title': "",
        'description': "",
        'videos': "",
        'video_ids': ""
    }
    return render_template('playlists_new.html', playlist=playlist)

@app.route('/playlists', methods=['POST'])
def playlists_submit():
    video_ids = request.form.get('video_ids').split()
    videos = video_url_creator(video_ids)
    playlist = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'videos': videos,
        'video_ids': video_ids,
    }
    playlists.insert_one(playlist)
    return redirect(url_for('playlists_index'))

@app.route('/playlists/<playlist_id>')
def playlists_show(playlist_id):
    playlist = playlists.find_one({'_id': ObjectId(playlist_id)})
    playlist_comments = comments.find({'playlist_id': playlist_id})
    return render_template('playlists_show.html', playlist=playlist, comments=playlist_comments)

@app.route('/playlists/<playlist_id>/edit')
def playlists_edit(playlist_id):
    playlist = playlists.find_one({'_id': ObjectId(playlist_id)})
    return render_template('playlists_edit.html', playlist=playlist, title='Edit Playlist')


@app.route('/playlists/<playlist_id>', methods=['POST'])
def playlists_update(playlist_id):
    video_ids = request.form.get('video_ids').split()
    videos = video_url_creator(video_ids)
    updated_playlist = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'videos': videos,
        'video_ids': video_ids
    }
    playlists.update_one(
        {'_id': ObjectId(playlist_id)},
        {'$set': updated_playlist})
    return redirect(url_for('playlists_show', playlist_id=playlist_id))

@app.route('/playlists/<playlist_id>/delete', methods=['POST'])
def playlists_delete(playlist_id):
    playlists.delete_one({'_id': ObjectId(playlist_id)})
    return redirect(url_for('playlists_index'))

# Comment Route Below


@app.route("/playlists/comments", methods=["POST"])
def comments_new():
    playlist_id = request.form.get("playlist_id")
    comment = {
        "title":request.form.get("title"),
        "content":request.form.get("content"),
        "playlist_id":playlist_id
    }
    comments.insert_one(comment)
    return redirect(url_for(f"playlists_show", playlist_id=playlist_id))


@app.route("/playlists/comments/<comment_id>", methods=["POST"])
def comments_delete(comment_id):
    comments.delete_one({"_id": ObjectId(comment_id)})
    return redirect(url_for("playlists_show", playlist_id=request.form.get("playlist_id")))

def video_url_creator(id_lst):
    videos = []
    for vid_id in id_lst:
        video = 'https://youtube.com/embed/' + vid_id
        videos.append(video)
    return videos

if __name__ == '__main__':
    app.run(debug=True)
