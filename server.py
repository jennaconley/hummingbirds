"""Hummingbirds"""

from flask import Flask, redirect, request, render_template, session, flash, jsonify, send_from_directory
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import extract
from flask_debugtoolbar import DebugToolbarExtension
import math 
from jinja2 import StrictUndefined
import time
import random
from datetime import datetime, date
from ebird.api import *
import os
from model import connect_to_db, db, BirdType, BirdSighting, Checklist, Location


EBIRD_API_KEY = os.environ.get("EBIRD_API_KEY")
OSM_ACCESS_TOKEN = os.environ.get("OSM_ACCESS_TOKEN")
FLASK_SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar:
app.secret_key = FLASK_SECRET_KEY

# # This will cause Jinja to automatically reload templates if they've been
# # changed. This is a resource-intensive operation so it should only be
# # set while debugging:
# app.jinja_env.auto_reload = True

# If you use an undefined variable in Jinja2, this raises an error:
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def begin_search():
    """Render the template "homepage.html"""

    birds = BirdType.query.all()

    print("Beginning locations query!")
    beginning = time.time()

    # Determining the current month
    today = date.today()
    current_month = today.month

    if cache.get(current_month):
        print(f"Month {current_month} already in cache!")
        lat_long_tuples_set = cache.get(current_month)
    else:
        # Query to get the locations that have sightings this month. Sighting dates are in the checklist table.
        checklist_location_list = db.session.query(Checklist, Location).join(Checklist.location).filter(extract('month', Checklist.datetime_object) == current_month).all()
       
        post_query_time = time.time()
        print(f"We just finished the main query. It took {post_query_time - beginning} seconds.")

        # Eliminating duplicate locations
        location_set = set()
        for checklist_object, location_object in checklist_location_list:
            location_set.add(location_object)
        
        # Reducing the number of markers that need to be mapped by condensing nearby locations into one marker
        lat_long_tuples_set = set()
        for location_object in location_set:
            lat_long_tuples_set.add((round(location_object.latitude, 1), round(location_object.longitude, 1)))

        post_sets_time = time.time()
        print(f"We just finished the location condensing loops.  It took {post_sets_time - post_query_time}")

        # Storing processed query results in the cache for next time.
        cache.set(current_month, lat_long_tuples_set)
        
    return render_template("homepage.html", humlist=birds, lat_long_tuples_set=lat_long_tuples_set, OSM_ACCESS_TOKEN=OSM_ACCESS_TOKEN)




@app.route('/sightings/<ebird_id>')
def show_sightings(ebird_id):
    """Gather sighting information to display using speciesmap.html"""

    beginning = time.time()

    bird = BirdType.query.get(ebird_id)
    post_BirdType_time = time.time()
    print(f"We just finished the BirdType query. It took {post_BirdType_time - beginning} seconds")
    
    if cache.get(ebird_id):
        print(f"{ebird_id} is in the cache!")
        list_of_dicts = cache.get(ebird_id)
    else:
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

        cache.set(ebird_id, list_of_dicts)    
        
        post_current_dict_time = time.time()
        print(f"We just finished the current_dict loop.  It took {post_current_dict_time - post_birdcount_time}")
        print(f"The whole thing took {post_current_dict_time - beginning} seconds")

    clat = list_of_dicts[0]['latitude']
    clong = list_of_dicts[0]['longitude']
        
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

    # eBird API wrapper function from https://pypi.org/project/ebird-api/
    locations = get_nearest_species(EBIRD_API_KEY, speciesCode, latitude, longitude, back=30, max_results=20,)
   
    return jsonify(locations)

    # The eBird API returns the closest places to see a species as a list of dictionaries. 
    # Example: 
    # {'speciesCode': 'rthhum', 
    # 'comName': 'Ruby-throated Hummingbird', 
    # 'sciName': 'Archilochus colubris', 
    # 'locId': 'L1521686', 
    # 'locName': '2223 Kodiak Dr NE', 
    # 'obsDt': '2020-03-03 17:07', 
    # 'howMany': 1, 
    # 'lat': 33.8334575, 
    # 'lng': -84.2980854, 
    # 'obsValid': True, 
    # 'obsReviewed': True, 
    # 'locationPrivate': True, 
    # 'subId': 'S65407994'}

@app.route('/favicon.ico')
def favicon():


    return send_from_directory(os.path.join(app.root_path, 'static/img/'), 
        'favicon.ico', mimetype='image/vnd.microsoft.icon')



       


if __name__ == "__main__":
    # Set debug=True if using the DebugToolbarExtension below:
    # app.debug = True
    
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    app.config["CACHE_TYPE"] = "simple" # Flask-Caching related config
    app.config["CACHE_DEFAULT_TIMEOUT"] = 300 # Flask-Caching related config
    cache = Cache(app) # Creating the Cache instance/object

    # Use the DebugToolbar:
    # DebugToolbarExtension(app)

    # Site can be found at http://localhost:5000
    app.run(
        port=5000,
        # host='0.0.0.0'
        host='127.0.0.1'
    )
