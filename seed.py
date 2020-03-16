"""File to seed database"""
from sqlalchemy import func
from server import app
from datetime import datetime
from model import connect_to_db, db, BirdType, Taxon, BirdSighting, Checklist, Location



def load_birdtypes():
    """Load row objects into database."""
    print()
    print("BirdType Objects")
    print()
    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    BirdType.query.delete()

    # Open file and return a corresponding file object. 
    # Extract data from the file object's row attributes.
    for row in open("seed_data/HummingbirdSpecies.txt"):
        row_list = row.split(",")
        #print(row_list)
        if "Trochilidae" in row_list[10]:
            sci_name = row_list[0]
            #print(sci_name)
            sci_list = sci_name.split()
            genus = sci_list[0]
            species = sci_list[1]

            common_name = row_list[1]
            ebird_id = row_list[2]
            range_notes = "none"
            # print(ebird_id, genus, species, common_name, range_notes)    

            # Create new row object:
            birdtype = BirdType(ebird_id=ebird_id, genus=genus, species=species, common_name=common_name, range_notes=range_notes)
            # Add new row object to the session so it will be stored:
            db.session.add(birdtype)

    # Done, commit new work:
    db.session.commit()



def load_taxa():
    genus = ""

   # clade = 'TBD'

    Taxon(genus=genus, clade='TBD')



def load_birdsightings():
    """Load row objects into database."""
    print()
    print("BirdSighting Objects")
    print()
    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    BirdSighting.query.delete()

    # Open file and return a corresponding file object. 
    # Split on tab with \t
    # Extract data from the file object's row attributes.
    for row in open("seed_data/ebd_allhum.txt"):
        row_list = row.split("\t")
        if row_list[8].isdigit(): 
            quantity = row_list[8]
        else:
            continue
        checklist = row_list[30]
        # Create new row object:
        birdsighting = BirdSighting(ebird_id="allhum", checklist_id=checklist, number_of_birds=quantity)
        # Add new row object to the session so it will be stored:
        db.session.add(birdsighting)

    # Commit all the new work:
    db.session.commit()



def load_checklists():
    checklist_id = ""
    datetime_object = ""
    location_id = ""

    Checklist()



def load_locations():
    location_id = ""
    latitude = ""
    longitude = ""
    country = ""

    Location()




# 'TAXONOMIC ORDER', 2            
# 'CATEGORY',     3 #species
# 'COMMON NAME', 4
# 'SCIENTIFIC NAME', 5
# 'OBSERVATION COUNT', 8
# 'COUNTRY', 12
# 'COUNTRY CODE', 13
# 'LOCALITY ID', 23
# 'LATITUDE', 25
# 'LONGITUDE', 26
# 'OBSERVATION DATE', if int(row_list[27][0:4]) > 2016:
# 'TIME OBSERVATIONS STARTED', 28
# 'SAMPLING EVENT IDENTIFIER', 30   #checklist id,  https://ebird.org/checklist/S63462799
# 'GROUP IDENTIFIER', 39




if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, execute the method on the database connection that creates the tables:
    db.create_all()

    # Load data into row objects created from classes in model.py
    load_birdtypes()
    # load_taxa()
    load_birdsightings()
    # load_checklists()
    # load_locations()