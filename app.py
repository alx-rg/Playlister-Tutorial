# remember to: source env/bin/activate
# to see the website : export FLASK_ENV=development; flask run

from flask import Flask
from flask.templating import render_template
from pymongo import MongoClient

client = MongoClient()
db = client.Playlister
playlists = db.playlists

app = Flask(__name__)

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

