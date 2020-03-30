"""Hummingbirds"""

from flask import Flask, redirect, request, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
import math 
from jinja2 import StrictUndefined
import time
import random

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
    """Gather sighting information to display using speciesmap.html"""

    beginning = time.time()

    bird = BirdType.query.get(ebird_id)
    post_BirdType_time = time.time()
    print(f"We just finished the BirdType query. It took {post_BirdType_time - beginning} seconds")
    
    sighting_checklist_location_list = db.session.query(BirdSighting, Checklist, Location).filter(BirdSighting.ebird_id == ebird_id).join(BirdSighting.checklist).join(Checklist.location).all()
    post_sightings_time = time.time()
    print(f"We just finished the BirdSighting, Checklist, Location query. It took {post_sightings_time - beginning} seconds")

    
    loc_birdcount_dict = {}
    for sighting_object, checklist_object, location_object in sighting_checklist_location_list:
        birdcount = sighting_object.number_of_birds
        loc_id = location_object.location_id
        loc_birdcount_dict[loc_id] = loc_birdcount_dict.get(loc_id, 0) + birdcount

    post_birdcount_time = time.time()
    print(f"We just finished the loc_birdcount_dict loop.  This last part took {post_birdcount_time - post_sightings_time} seconds")


    list_of_dicts = []
    for loc_code in loc_birdcount_dict.keys():
        location_object = Location.query.get(loc_code)
        current_dict = {'latitude': location_object.latitude, 'longitude': location_object.longitude, 'country': location_object.country, 'this_species': loc_birdcount_dict[loc_code], 'circle_size': math.sqrt(loc_birdcount_dict[loc_code])}
        list_of_dicts.append(current_dict)

    post_current_dict_time = time.time()
    print(f"We just finished the current_dict loop.  It took {post_current_dict_time - post_birdcount_time}")

    clat = list_of_dicts[0]['latitude']
    clong = list_of_dicts[0]['longitude']
    
    print(f"The whole thing took {post_current_dict_time - beginning} seconds")

    return render_template("speciesmap.html", clat=clat, clong=clong, list_of_dicts=list_of_dicts, bird_object=bird)


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
