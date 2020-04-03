"""Hummingbirds"""

from flask import Flask, redirect, request, render_template, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
import math 
from jinja2 import StrictUndefined
import time
import random
from datetime import datetime
from ebird.api import *
import os
from model import connect_to_db, db, BirdType, BirdSighting, Checklist, Location


EBIRD_API_KEY = os.environ["EBIRD_API_KEY"]
OSM_ACCESS_TOKEN = os.environ["OSM_ACCESS_TOKEN"]
FLASK_SECRET_KEY = os.environ["FLASK_SECRET_KEY"]

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar:
app.secret_key = FLASK_SECRET_KEY

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




@app.route('/locations')
def map_locations():
    """Render the template "locations.html"""

    print("In locations route!")
    beginning = time.time()

    # Complicated Option 1/2 (also broken)
    # checklist_location_list = db.session.query(Checklist, Location).filter(Checklist.datetime_object[0:4] == '2019').filter(Checklist.datetime_object[5:7] == '04').join(Checklist.location).limit(10000)
    # location_set = set()

    #checklist_location_list = db.session.query(Checklist, Location).join(Checklist.location).filter(Checklist.datetime_object[0:4] == '2019').limit(1000)
    #location_set = set()

    
    # Simple Option 1/1
    # location_list = Location.query.limit(10000)

    # Too much for my computer - don't use
    # locations = Location.query.all()


    post_query_time = time.time()
    print(f"We just finished the main query. It took {post_query_time - beginning} seconds.")

    # Complicated option 2/2
    # for checklist_object, location_object in checklist_location_list:
    #     location_set.add(location_object)
    # location_list = list(location_set)

    # Works for both:        
    list_of_dicts = []
    for location_object in location_list:
        current_dict = {'latitude': location_object.latitude, 'longitude': location_object.longitude}
        list_of_dicts.append(current_dict)

    post_current_dict_time = time.time()
    print(f"We just finished the current_dict loop.  It took {post_current_dict_time - post_query_time}")


    return render_template("locations.html", list_of_dicts=list_of_dicts, OSM_ACCESS_TOKEN=OSM_ACCESS_TOKEN)




@app.route('/sightings/<ebird_id>')
def show_sightings(ebird_id):
    """Gather sighting information to display using speciesmap.html"""

    beginning = time.time()

    bird = BirdType.query.get(ebird_id)
    post_BirdType_time = time.time()
    print(f"We just finished the BirdType query. It took {post_BirdType_time - beginning} seconds")
    
    sighting_checklist_location_list = db.session.query(BirdSighting, Checklist, Location).filter(BirdSighting.ebird_id == ebird_id).join(BirdSighting.checklist).join(Checklist.location).limit(10000)
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

    # if ebird_id == 'gnbman':
    # add a dict to the list with its location info
    # current_dict = {'latitude': location_object.latitude, 'longitude': location_object.longitude, 'country': location_object.country, 'this_species': loc_birdcount_dict[loc_code], 'circle_size': math.sqrt(loc_birdcount_dict[loc_code])}
    #     list_of_dicts.append(current_dict)

    return render_template("speciesmap.html", clat=clat, clong=clong, list_of_dicts=list_of_dicts, bird_object=bird, OSM_ACCESS_TOKEN=OSM_ACCESS_TOKEN)



@app.route('/nearby.json')
def hummingbirds_near_me():
    """Request and return eBird API information """

    print("In the nearby route!")

    latitude = float(request.args.get("latitude"))
    longitude = float(request.args.get("longitude"))
    speciesCode = request.args.get("eBirdID")

    print()
    print(latitude)
    print(longitude)
    print(speciesCode)   
    print() 


    

    # Minneapolis:
    # latitude = 44.98
    # longitude = -93.27
    # speciesCode = 'beehum1'

    # eBird API wrapper function from https://pypi.org/project/ebird-api/
    locations = get_nearest_species(EBIRD_API_KEY, speciesCode, latitude, longitude, back=30, max_results=20,)
   

    return jsonify(locations)

    """Returns closest places to see a species as a list of dictionaries. 
    Dictionary example: 
    {'speciesCode': 'rthhum', 
    'comName': 'Ruby-throated Hummingbird', 
    'sciName': 'Archilochus colubris', 
    'locId': 'L1521686', 
    'locName': '2223 Kodiak Dr NE', 
    'obsDt': '2020-03-03 17:07', 
    'howMany': 1, 
    'lat': 33.8334575, 
    'lng': -84.2980854, 
    'obsValid': True, 
    'obsReviewed': True, 
    'locationPrivate': True, 
    'subId': 'S65407994'} """



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
