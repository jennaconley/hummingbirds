
from flask_sqlalchemy import SQLAlchemy

# Importing and instantiating a SQLAlchemy object. 
# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.), and the
# db.Model super-class that our database table classes will inherit from.

db = SQLAlchemy()


##############################################################################
# Model definitions

class BirdType(db.Model):
    """Type of bird."""
    
    __tablename__ = "birdtypes"

    ebird_id = db.Column(db.String(64), nullable=False, primary_key=True)
    genus = db.Column(db.String(64), nullable=False)
    species = db.Column(db.String(64), nullable=False)
    common_name = db.Column(db.String(64), nullable=False)
    range_notes =  db.Column(db.Text, nullable=True)

    # birdsightings = db.relationship("BirdSighting")
    # taxon = db.relationship("Taxon")

    def __repr__(self):
        """provide helpful representation when printed""" 
        return f"<BirdType Object: ebird_id is {self.ebird_id}.>" 


# 'speciesCode': 'rthhum'
# 'comName': 'Ruby-throated Hummingbird',
# 'sciName': 'Archilochus colubris',


class Taxon(db.Model):
    """Table of genuses and their clade membership. Hummingbirds fall into nine main clades,  
    organized which define their relationships to nectar-bearing flowering plants 
    and their continued spread into new geographic areas: 
    Topazes, Hermits, Mangoes, Brilliants, Coquettes, Patagona, Mountain Gems, Bees, and Emeralds.
    """
    
    __tablename__ = "taxa"

    genus = db.Column(db.String(64), nullable=False, primary_key=True)
    clade = db.Column(db.String(64), nullable=True)

    def __repr__(self):
        """provide helpful representation when printed""" 
        return f"<Taxon Object: genus is {self.genus}, clade is {self.clade}.>" 



class BirdSighting(db.Model):
    """Sighting of Bird"""
    
    __tablename__ = "birdsightings"

    bird_sighting_id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True)
    ebird_id = db.Column(db.String(64), db.ForeignKey('birdtypes.ebird_id'), nullable=False)
    checklist_id = db.Column(db.String(64), db.ForeignKey('checklists.checklist_id'), nullable=False)
    number_of_birds = db.Column(db.Integer, nullable=False)

    # birdtype = db.relationship("BirdType")
    # checklist = db.relationship("Checklist")

    def __repr__(self):
        """provide helpful representation when printed""" 
        return f"<BirdSighting Object: ebird_id is {self.ebird_id}, number_of_birds is {self.number_of_birds}.>"  


class Checklist(db.Model):
    """Birding checklist."""
    
    __tablename__ = "checklists"

    checklist_id = db.Column(db.String(64), nullable=False, primary_key=True)
    datetime_object = db.Column(db.DateTime, nullable=False)
    location_id = db.Column(db.String(64), db.ForeignKey('locations.location_id'), nullable=False)

    # birdsightings = db.relationship("BirdSighting")
    # location = db.relationship("Location")

    def __repr__(self):
        """provide helpful representation when printed""" 
        return f"<Checklist Object: checklist_id is {self.checklist_id}.>"  


class Location(db.Model):
    """Birding location."""
    
    __tablename__ = "locations"

    location_id = db.Column(db.String(64), nullable=False, primary_key=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    country = db.Column(db.String(64), nullable=True)

    # checklists = db.relationship("Checklist")

    def __repr__(self):
        """provide helpful representation when printed""" 
        return f"<Location Object: location_id is {self.location_id}.>" 



# 'subId': 'S65407994'
# 'obsDt': '2020-03-03 17:07'
# 'lat': 33.8334575, 
# 'lng': -84.2980854,


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our database.
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///hummingbirds"
    app.config["SQLALCHEMY_ECHO"] = True
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # If you run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to declarative base!")