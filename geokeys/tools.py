import re

from places import places_list

def standardize(geostring):
    '''Tranform a geostring into a key'''
    # Covert to lowercase
    geostring = geostring.lower()
    # Remove whitespace
    geostring = ''.join(geostring.split())
    # Remove ',califronia'
    geostring = re.sub(',california$', '', geostring)
    # Place 'us:ca:' at beginning of string
    geostring = re.sub('^', 'us:ca:', geostring)

    return geostring

def generate_key(geostring, context="p+us:ca"):
    '''Generate a key for a geostring'''
    if not geostring.endswith(', California'):
        geostring += ', California'
    
    # Geostring match with no change (not likely for non-Census data)
    for place, pop in places_list:
        if geostring == place:
            return standardize(geostring)

    # City geostring match
    city_geostring = geostring.replace(',', ' city,')

    for place, pop in places_list:
        if city_geostring == place:
            return standardize(geostring)
    
    # Town geostring match
    city_geostring = geostring.replace(',', ' city,')

    for place, pop in places_list:
        if city_geostring == place:
            return standardize(geostring)
    
    # CDP geostring match
    cdp_geostring = geostring.replace(',', ' CDP,')

    for place, pop in places_list:
        if cdp_geostring == place:
            return standardize(geostring)

    return standardize(geostring)
