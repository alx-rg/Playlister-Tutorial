# remember to: source env/bin/activate
# to see the website : export FLASK_ENV=development; flask run
# http://localhost:5000

from flask import Flask, render_template, request, redirect, url_for
from flask.templating import render_template
from pymongo import MongoClient

client = MongoClient()
db = client.Playlister
playlists = db.playlists

app = Flask(__name__)

def video_url_creator(id_lst):
    videos = []
    for vid_id in id_lst:
        video = 'https://youtube.com/embed/' + vid_id
        videos.append(video)
    return videos

# @app.route('/')
# def index():
#    """Return homepage."""
#    return render_template('home.html', msg='Flask is pretty cool...')

if __name__ == '__main__':
   app.run(debug=True)

# OUR MOCK ARRAY OF PROJECTS
playlists = [
   { 'title': 'Cat Videos', 'description': 'Cats acting weird' },
   { 'title': '80\'s Music', 'description': 'Don\'t stop believing!' },
   { 'title': 'Hockey Memes', 'description': 'Bloopers of the matches!' },
]
@app.route('/')
def playlists_index():
   """Show all playlists."""
   return render_template('playlists_index.html', playlists=playlists.find())

@app.route('/playlists/new')
def playlists_new():
   return render_template('playlists_new.html')

@app.route('/playlists', methods=['POST'])
def playlists_submit():
    #Submit a new playlist.
    print(request.form.to_dict())
    return redirect(url_for('playlists_index'))

@app.route('/playlists', methods=['POST'])
def playlists_submit():
    #Submit a new playlist.
    # Grab the video IDs and make a list out of them
    video_ids = request.form.get('video_ids').split()
    # call our helper function to create the list of links
    videos = video_url_creator(video_ids)
    playlist = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'videos': videos,
        'video_ids': video_ids
    }
    playlists.insert_one(playlist)
    return redirect(url_for('playlists_index'))
