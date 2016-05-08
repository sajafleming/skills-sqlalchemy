"""

This file is the place to write solutions for the
skills assignment called skills-sqlalchemy. Remember to
consult the exercise directions for more complete
explanations of the assignment.

All classes from model.py are being imported for you
here, so feel free to refer to classes without the
[model.]User prefix.

"""

from model import *

from sqlalchemy import func
from sqlalchemy.sql import label

init_app()

# -------------------------------------------------------------------
# Part 2: Write queries


# Get the brand with the **id** of 8.
db.session.query(Brand).get(8)

m = Model.query
b = Brand.query

# Get all models with the **name** Corvette and the **brand_name** Chevrolet.
m.filter(Model.name == "Corvette", Model.brand_name == "Chevrolet")

# Get all models that are older than 1960.
m.filter(Model.year < 1960)

# Get all brands that were founded after 1920.
b.filter(Brand.founded > 1920)

# Get all models with names that begin with "Cor".
m.filter(Model.name.like('Cor%'))

# Get all brands that were founded in 1903 and that are not yet discontinued.
b.filter(Brand.founded == 1903, Brand.discontinued == None)

# Get all brands that are either 1) discontinued (at any time) or 2) founded 
# before 1950.
b.filter( db.or_(Brand.discontinued.isnot(None), Brand.founded < 1950) )

# Get any model whose brand_name is not Chevrolet.
m.filter(Model.brand_name != "Chevrolet")

# Fill in the following functions. (See directions for more info.)

def get_model_info(year):
    '''Takes in a year, and prints out each model, brand_name, and brand
    headquarters for that year using only ONE database query.'''
    # looks ugly when printed

    cars = Model.query.filter(Model.year == year)

    for car in cars:
        print "\n\n"
        print ("Model: %s, Brand: %s, Headquarters %s" % 
              (car.name, car.brand_name, car.brand.headquarters))


def get_brands_summary():
    '''Prints out each brand name, and each model name for that brand
     using only ONE database query.'''

    list_of_all = db.session.query(Model.brand_name, 
        label("models", func.array_agg(Model.name))).group_by(Model.brand_name).all()

    for item in list_of_all:
        print
        print "Brand: %s, Model %s, " % (item.brand_name, set(item.models))


# -------------------------------------------------------------------
# Part 2.5: Discussion Questions (Include your answers as comments.)

# 1. What is the returned value and datatype of ``Brand.query.filter_by(name='Ford')``?
#  The returned value is all the brands with name "Ford" and the datatype is a Query object
# 2. In your own words, what is an association table, and what *type* of relationship
# does an association table manage?
# It's a table that doesn't necessarily contain much information but is used
# to relate 2 other (or more tables). These "bridge" tables help resolve the 
# complications of tables with many to many relationships by turning them into
# a bunch of many to one relationships. 

# -------------------------------------------------------------------
# Part 3

def search_brands_by_name(mystr):
    """Returns list of objects that are brands that contain or are equal to 
    the string entered"""
    
    return Brand.query.filter(Brand.name.like('%' + mystr + '%')).all()

def get_models_between(start_year, end_year):
    """Returns a list of objects that are models with years that fall 
    between the two years entered"""

    return Model.query.filter(Model.year > start_year, Model.year < end_year)

