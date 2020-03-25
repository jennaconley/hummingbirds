"""Hummingbirds"""

from flask import Flask, redirect, request, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension

from jinja2 import StrictUndefined

from model import connect_to_db, db, BirdType, BirdSighting, Checklist, Location
# from model import Taxon

#from associations import loc_diversity_dict


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar:
app.secret_key = "hummingbird"

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

    bird = BirdType.query.get(ebird_id)

    sightings = BirdSighting.query.filter_by(ebird_id=ebird_id).all()


    # locations = Location.query.all()


    loc_birdcount_dict = {}

    for sighting_object in sightings:
        checklist_object = sighting_object.checklist
        location_object = checklist_object.location
        loc_birdcount_dict[location_object.location_id] = loc_birdcount_dict.get(location_object.location_id, 0) + sighting_object.number_of_birds
    
    list_of_dicts = []

    for loc_code in loc_birdcount_dict.keys():
        location_object = Location.query.get(loc_code)

        current_dict = {'latitude': location_object.latitude, 'longitude': location_object.longitude, 'country': location_object.country, 
          'this_species': loc_birdcount_dict[loc_code]}

        list_of_dicts.append(current_dict)

    clat = 9.7489
    clong = 83.7534

    return render_template("speciesmap.html", clat=clat, clong=clong, list_of_dicts=list_of_dicts, bird_object=bird)
    # return render_template("hummingbird.html", list_of_dicts=list_of_dicts, bird_object=bird)

    # Link to eBird info:
    # https://ebird.org/species/ebird_id


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
