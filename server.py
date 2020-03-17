"""Hummingbirds"""

from flask import Flask, redirect, request, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension

from jinja2 import StrictUndefined

from model import connect_to_db, db, BirdType, Taxon, BirdSighting, Checklist, Location


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar:
app.secret_key = "ABC"

# This will cause Jinja to automatically reload templates if they've been
# changed. This is a resource-intensive operation so it should only be
# set while debugging:
app.jinja_env.auto_reload = True

# If you use an undefined variable in Jinja2, this raises an error:
app.jinja_env.undefined = StrictUndefined





@app.route('/')
def begin_search():
    """Render the template "homepage.html"""


    birds = BirdType.query.all()


    return render_template("homepage.html", humlist=birds)




@app.route('/sightings/<ebird_id>')
def show_sightings(ebird_id):
    """Render the template hummingbird.html"""

    #bird = BirdType.query.get(ebird_id)

    sightings = BirdSighting.query.filter_by(ebird_id=ebird_id).all()


    return render_template("hummingbird.html", sightings_list=sightings)




if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    # Site can be found at http://localhost:5000
    app.run(port=5000, host='0.0.0.0')
