"""File to seed database"""
from sqlalchemy import func
from server import app
from datetime import datetime
from model import connect_to_db, db, BirdType, Taxon, BirdSighting, Checklist, Location
import sys


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



def gse_dict():
    """Create a quick ebird_id reference to reduce demand on database while seeding: 
    {genus: {species: ebird_id}, genus: {species: ebird_id, species: ebird_id}}
    """
    hum_dict = {}
    hum_list = BirdType.query.all()
    for hum in hum_list:
        if hum.genus in hum_dict.keys():
            hum_dict[hum.genus][hum.species] = hum.ebird_id
        else:
            hum_dict[hum.genus] = {hum.species: hum.ebird_id}

    return hum_dict    



# def load_taxa():
    """Load row objects into database."""
    # genus = ""

   # clade = 'TBD'

    # Taxon(genus=genus, clade='TBD')



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
    for row in open("seed_data/ebd_calhum.txt"):
        row_list = row.split("\t")
        if row_list[8].isdigit(): 
            quantity = row_list[8]
        else:
            continue
        checklist = row_list[30]
        # Create new row object:
        birdsighting = BirdSighting(ebird_id="calhum", checklist_id=checklist, number_of_birds=quantity)
        # Add new row object to the session so it will be stored:
        db.session.add(birdsighting)

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
    """Load row objects into database."""
    print()
    print("Checklist Objects")
    print()
    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Checklist.query.delete()

    # Open file and return a corresponding file object. 
    # Split on tab with \t
    # Extract data from the file object's row attributes.
    """Load row objects into database."""
    unique_checklists = []
    # for i, row in enumerate(open("seed_data/all_hummingbird_sightings_since_2017.txt")):
    for row in open("seed_data/first100sightings.txt"):
        row = row.rstrip()
        row_list = row.split("\t")
        # if len(row_list) < 43:
        #     if len(row_list) > 1:
        #         print(len(row_list), "is less than 43:", row_list)
        #         continue
        if row_list[30] in unique_checklists:
            continue
        date = row_list[27]
        year = date[0:4]
        # print(year)
        if int(year) > 2016:
            if row_list[3] == 'species':
                location = row_list[23]
                checklist = row_list[30]

                date = row_list[27]
                time = row_list[28]
                datetime_object = date + time

                
                print("checklist_id= ", checklist, "location_id= ", location, "datetime_object= ", datetime)
                sys.exit()
                # break
                checklist_object = Checklist(location_id=location, checklist_id=checklist, datetime_object=datetime)

                # Add new row object to the session so it will be stored:
                db.session.add(checklist_object)
                # db.session.commit()
                unique_checklists.append(checklist)
                # sys.exit()
                if i % 100 == 0:
                    print("row: ", i)
                    print("Unique Checklists: ", len(unique_checklists))
                    # Commit all the new work: 
                    db.session.commit()
    
    sys.exit()                
    # Commit all the new work:
    db.session.commit()





def load_locations():

    print()
    print("Location Objects")
    print()
    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Location.query.delete()

    # Open file and return a corresponding file object. 
    # Split on tab with \t
    # Extract data from the file object's row attributes.
    """Load row objects into database."""
    previous_loc_list = []
    for i, row in enumerate(open("seed_data/all_hummingbird_sightings_since_2017.txt")):
    # for row in open("seed_data/first100sightings.txt"):
        row = row.rstrip()
        row_list = row.split("\t")
        # if len(row_list) < 43:
        #     if len(row_list) > 1:
        #         print(len(row_list), "is less than 43:", row_list)
        #         continue
        if row_list[23] in previous_loc_list:
            continue
        date = row_list[27]
        year = date[0:4]
        # print(year)
        if int(year) > 2016:
            if row_list[3] == 'species':
                location = row_list[23]
                latitude =  row_list[25]
                longitude = row_list[26]
                country = row_list[12]
                previous_loc_list.append(location)
                # sys.exit()
                # print("We didn't exit :-(")
                # break
                location_object = Location(location_id=location, latitude=latitude, longitude=longitude, country=country)
                # Add new row object to the session so it will be stored:
                db.session.add(location_object)
                # db.session.commit()
                # sys.exit()
                if i % 100 == 0:
                    print("row: ", i)
                    print("Unique Locations: ", len(previous_loc_list))
                    # Commit all the new work: 
                    db.session.commit()
                    
    # Commit all the new work:
    db.session.commit()


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
    
    # load_taxa()
    # load_locations()

    # load_birdtypes()
    load_checklists()   

    # ebird_match_dict = gse_dict()
   
    # load_birdsightings()