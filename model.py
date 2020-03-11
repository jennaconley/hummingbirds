
from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

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

    birdsightings = db.relationship("BirdSighting")

    def __repr__(self):
        """provide helpful representation when printed""" 
        return f"<BirdType Object: ebird_id is {self.ebird_id}.>" 


# 'speciesCode': 'rthhum'
# 'comName': 'Ruby-throated Hummingbird',
# 'sciName': 'Archilochus colubris',


# class Clade(db.Model):
#     """Table of genuses and their clade membership. Hummingbirds fall into nine main clades, the 
#     Topazes, Hermits, Mangoes, Brilliants, Coquettes, Patagona, Mountain Gems, Bees, and Emeralds, 
#     defining their relationship to nectar-bearing flowering plants 
#     and the birds' continued spread into new geographic areas"""
    
#     __tablename__ = "clades"

#     genus = db.Column(db.String(64), nullable=False, primary_key=True)
#     clade = db.Column(db.String(64), nullable=False)

    # def __repr__(self):
        # """provide helpful representation when printed""" 
        # return f"<Clade Object: genus is {self.genus}, clade is {self.clade}.>" 


class BirdSighting(db.Model):
    """Sighting of Bird"""
    
    __tablename__ = "birdsightings"

    bird_sighting_id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True)
    ebird_id = db.Column(db.String(64), db.ForeignKey('birdtypes.ebird_id'), nullable=False)
    checklist_id = db.Column(db.String(64), db.ForeignKey('checklists.checklist_id'), nullable=False)
    number_of_birds = db.Column(db.Integer, nullable=False)

    birdtype = db.relationship("BirdType")
    checklist = db.relationship("Checklist")

    def __repr__(self):
        """provide helpful representation when printed""" 
        return f"<BirdSighting Object: ebird_id is {self.ebird_id}, number_of_birds is {self.number_of_birds}.>"  


class Checklist(db.Model):
    """Birding checklist."""
    
    __tablename__ = "checklists"

    checklist_id = db.Column(db.String(64), nullable=False, primary_key=True)
    datetime_object = db.Column(db.DateTime, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    birdsightings = db.relationship("BirdSighting")
    
    def __repr__(self):
        """provide helpful representation when printed""" 
        return f"<Checklist Object: checklist_id is {self.checklist_id}.>"  


# 'subId': 'S65407994'
# 'obsDt': '2020-03-03 17:07'
# 'lat': 33.8334575, 
# 'lng': -84.2980854,
