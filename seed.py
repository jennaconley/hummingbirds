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
    genus = 



    # clade = 'TBD'

    Taxon(genus=genus, clade='TBD')



def load_birdsightings():
    bird_sighting_id = 
    ebird_id = 
    checklist_id = 
    number_of_birds =

    BirdSighting()



def load_checklists():
    checklist_id = 
    datetime_object = 
    location_id = db.Column(db.String(64), db.ForeignKey('locations.location_id'), nullable=False)

    Checklist()



def load_locations():
    location_id = db.Column(db.String(64), nullable=False, primary_key=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    country = db.Column(db.String(64), nullable=True)

    Location()

# 0.Topaza pella,
# 1.Crimson Topaz,
# 2.critop1,
# 3.species,
# 4.4089.0,
# 5.CRTO,
# 6.TOPE,
# 7.,
# 8.Caprimulgiformes,
# 9.Hummingbirds,
# 10.Trochilidae,,,





# # Open file, return corresponding file object. Extract data from file object's row attributes. 
# with open("seed_data/ebd_sample.txt", "r") as file:
#         rows_list = file.readlines()

    for row in rows_list[0:2]:
        split_row = row.split("\t")
        print('TAXONOMIC ORDER', split_row[2])
        if split_row[3] == 'species': 
            print('CATEGORY', split_row[3])
        print('COMMON NAME', split_row[4])
        print('SCIENTIFIC NAME', split_row[5])
        print('OBSERVATION COUNT', split_row[8])
        print('COUNTRY', split_row[12])
        print('COUNTRY CODE', split_row[13])
        print('LOCALITY ID', split_row[23])
        print('LATITUDE', split_row[25])
        print('LONGITUDE', split_row[26])
        if split_row[27][0:4].isdigit():
            if int(split_row[27][0:4]) > 2016:
                print('OBSERVATION DATE', split_row[27])
        print('TIME OBSERVATIONS STARTED', split_row[28])
        print('SAMPLING EVENT IDENTIFIER', split_row[30])
        print('GROUP IDENTIFIER', split_row[39])    
        print()

# str.isdigit

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
# 'OBSERVATION DATE', if int(split_row[27][0:4]) > 2016:
# 'TIME OBSERVATIONS STARTED', 28
# 'SAMPLING EVENT IDENTIFIER', 30   #checklist id,  https://ebird.org/checklist/S63462799
# 'GROUP IDENTIFIER', 39

# Begin List
# ['GLOBAL UNIQUE IDENTIFIER', 
# 'LAST EDITED DATE', 
# 'TAXONOMIC ORDER', 2
# 'CATEGORY', 3
# 'COMMON NAME', 4
# 'SCIENTIFIC NAME', 5
# 'SUBSPECIES COMMON NAME', 
# 'SUBSPECIES SCIENTIFIC NAME', 
# 'OBSERVATION COUNT', 8
# 'BREEDING BIRD ATLAS CODE', 
# 'BREEDING BIRD ATLAS CATEGORY', 
# 'AGE/SEX', 
# 'COUNTRY', 12
# 'COUNTRY CODE', 13
# 'STATE', 
# 'STATE CODE', 
# 'COUNTY', 
# 'COUNTY CODE', 
# 'IBA CODE', 
# 'BCR CODE', 
# 'USFWS CODE', 
# 'ATLAS BLOCK', 
# 'LOCALITY', 
# 'LOCALITY ID', 23
# 'LOCALITY TYPE', 
# 'LATITUDE', 25
# 'LONGITUDE', 26
# 'OBSERVATION DATE', 27
# 'TIME OBSERVATIONS STARTED', 28
# 'OBSERVER ID', 
# 'SAMPLING EVENT IDENTIFIER', 30
# 'PROTOCOL TYPE', 
# 'PROTOCOL CODE', 
# 'PROJECT CODE', 
# 'DURATION MINUTES', 
# 'EFFORT DISTANCE KM', 
# 'EFFORT AREA HA', 
# 'NUMBER OBSERVERS', 
# 'ALL SPECIES REPORTED', 
# 'GROUP IDENTIFIER', 39
# 'HAS MEDIA', 
# 'APPROVED', 
# 'REVIEWED', 
# 'REASON', 
# 'TRIP COMMENTS', 
# 'SPECIES COMMENTS\n']


        # if "Trochilidae" in row_list[6]:
        #     taxon_order = row_list[0]
        #     species_code = row_list[2]
        #     common_name = row_list[3]

        #     sci_name = row_list[4]
        #     sci_list = sci_name.split()
        #     genus = sci_list[0]
        #     species = " ".join(sci_list[1:])

            # print([taxon_order, species_code, common_name, genus, species])


        # birdtype = BirdType(ebird_id=species_code, genus=genus, species=species, common_name=common_name)



# tab is \t


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Load data into row objects created from classes in model.py
    load_birdtypes()
    load_taxa()
    load_birdsightings()
    load_checklists()
    load_locations()