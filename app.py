# remember to: source env/bin/activate
# to see the website : export FLASK_ENV=development; flask run

from flask import Flask
from flask.templating import render_template

app = Flask(__name__)

@app.route('/')
def index():
   """Return homepage."""
   return render_template('home.html', msg='Flask is...')

if __name__ == '__main__':
   app.run(debug=True)

