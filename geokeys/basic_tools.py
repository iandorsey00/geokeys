'''
Tools primarily intended for Census display labels and initial generation
of reference keys.
'''

import re

from places import places_list

def has_state(geostring):
    '''Does the string have state information?'''
    return ',' in geostring

def get_state(geostring):
    '''Get state information from the string'''
    if geostring == 'Islamorada, Village of Islands village; Florida':
        return 'Florida'
    elif geostring == 'Lynchburg, Moore County metropolitan government; Tennessee':
        return 'Tennessee'
    else:
        state = re.search(', (.*?)$', geostring)
        return state.group(1)

def get_prefix(state):
    '''Reference conversion for Census Bureau display labels into keys.'''
    state = state.lower()

    prefixes = {
        'alabama': 'us:al:',
        'alaska': 'us:ak:',
        'arizona': 'us:az:',
        'arkansas': 'us:ar:',
        'california': 'us:ca:',
        'colorado': 'us:co:',
        'connecticut': 'us:ct:',
        'delaware': 'us:de:',
        'district of columbia': 'us:dc:',
        'florida': 'us:fl:',
        'georgia': 'us:ga:',
        'hawaii': 'us:hi:',
        'idaho': 'us:id:',
        'illinois': 'us:il:',
        'indiana': 'us:in:',
        'iowa': 'us:ia:',
        'kansas': 'us:ks:',
        'kentucky': 'us:ky:',
        'louisiana': 'us:la:',
        'maine': 'us:me:',
        'maryland': 'us:md:',
        'massachusetts': 'us:ma:',
        'michigan': 'us:mi:',
        'minnesota': 'us:mn:',
        'mississippi': 'us:ms:',
        'missouri': 'us:mo:',
        'montana': 'us:mt:',
        'nebraska': 'us:ne:',
        'nevada': 'us:nv:',
        'new hampshire': 'us:nh:',
        'new jersey': 'us:nj:',
        'new mexico': 'us:nm:',
        'new york': 'us:ny:',
        'north carolina': 'us:nc:',
        'north dakota': 'us:nd:',
        'ohio': 'us:oh:',
        'oklahoma': 'us:ok:',
        'oregon': 'us:or:',
        'pennsylvania': 'us:pa:',
        'rhode island': 'us:ri:',
        'south carolina': 'us:sc:',
        'south dakota': 'us:sd:',
        'tennessee': 'us:tn:',
        'texas': 'us:tx:',
        'utah': 'us:ut:',
        'vermont': 'us:vt:',
        'virginia': 'us:va:',
        'washington': 'us:wa:',
        'west virginia': 'us:wv:',
        'wisconsin': 'us:wi:',
        'wyoming': 'us:wy:',
        'al': 'us:al:',
        'ak': 'us:ak:',
        'az': 'us:az:',
        'ar': 'us:ar:',
        'ca': 'us:ca:',
        'co': 'us:co:',
        'ct': 'us:ct:',
        'de': 'us:de:',
        'dc': 'us:dc:',
        'fl': 'us:fl:',
        'ga': 'us:ga:',
        'hi': 'us:hi:',
        'id': 'us:id:',
        'il': 'us:il:',
        'in': 'us:in:',
        'ia': 'us:ia:',
        'ks': 'us:ks:',
        'ky': 'us:ky:',
        'la': 'us:la:',
        'me': 'us:me:',
        'md': 'us:md:',
        'ma': 'us:ma:',
        'mi': 'us:mi:',
        'mn': 'us:mn:',
        'ms': 'us:ms:',
        'mo': 'us:mo:',
        'mt': 'us:mt:',
        'ne': 'us:ne:',
        'nv': 'us:nv:',
        'nh': 'us:nh:',
        'nj': 'us:nj:',
        'nm': 'us:nm:',
        'ny': 'us:ny:',
        'nc': 'us:nc:',
        'nd': 'us:nd:',
        'oh': 'us:oh:',
        'ok': 'us:ok:',
        'or': 'us:or:',
        'pa': 'us:pa:',
        'ri': 'us:ri:',
        'sc': 'us:sc:',
        'sd': 'us:sd:',
        'tn': 'us:tn:',
        'tx': 'us:tx:',
        'ut': 'us:ut:',
        'vt': 'us:vt:',
        'va': 'us:va:',
        'wa': 'us:wa:',
        'wv': 'us:wv:',
        'wi': 'us:wi:',
        'wy': 'us:wy:'
        }

    return prefixes[state]

def preprocess(geostring):
    geostring_before = geostring

    # Handle special cases

    ## Places with commas in their names
    if geostring == 'Islamorada, Village of Islands village; Florida':
        return 'us:fl:islamorada'
    elif geostring == 'Lynchburg, Moore County metropolitan government; Tennessee':
        return 'us:tn:lynchburg'

    ## Consolidations
    if geostring == 'Nashville-Davidson metropolitan government (balance), Tennessee':
        return 'us:tn:nashville'
    if geostring == 'Louisville/Jefferson County metro government (balance), Kentucky':
        return 'us:tn:louisville'
    if geostring == 'Lexington-Fayette urban county, Kentucky':
        return 'us:ky:lexington'
    if geostring == 'Augusta-Richmond County consolidated government (balance), Georgia':
        return 'us:ga:augusta'
    if geostring == 'Macon-Bibb County, Georgia':
        return 'us:ga:macon'
    if geostring == 'Athens-Clarke County unified government (balance), Georgia':
        return 'us:ga:athens'
    if geostring == 'Butte-Silver Bow (balance), Montana':
        return 'us:mt:butte'
    if geostring == 'Cusseta-Chattahoochee County unified government, Georgia':
        return 'us:ga:cusseta'
    if geostring == 'Hartsville/Trousdale County, Tennessee':
        return 'us:tn:hartsville'
    if geostring == 'Anaconda-Deer Lodge County, Montana':
        return 'us:mt:anaconda'
    if geostring == 'Echols County consolidated government, Georgia':
        return 'us:ga:statenville'
    if geostring == 'Webster County unified government, Georgia':
        return 'us:ga:preston'
    if geostring == 'Greeley County unified government (balance), Kansas':
        return 'us:ks:tribune'

    ## Places with official names that are less commonly used
    if geostring == 'San Buenaventura (Ventura) city, California':
        return 'us:ca:ventura'

    state = ''
    prefix = ''

    # Get state and prefix
    if has_state(geostring):
        state = get_state(geostring)
        prefix = get_prefix(state)

    # Remove place_types
    place_types_for_removal = []

    place_types_for_removal.append(' city,.*?$')
    place_types_for_removal.append(' town,.*?$')
    place_types_for_removal.append(' CDP,.*?$')
    place_types_for_removal.append(' borough,.*?$')
    place_types_for_removal.append(' municipality,.*?$')
    place_types_for_removal.append(' village,.*?$')
    place_types_for_removal.append(' corporation,.*?$')
    place_types_for_removal.append(' CDP \(.*?\),.*?$')
    place_types_for_removal.append(' city \(.*?\),.*?$')
    place_types_for_removal.append(' borough \(.*?\),.*?$')
    place_types_for_removal.append(' village \(.*?\),.*?$')

    for place_type in place_types_for_removal:
        geostring = re.sub(place_type, '', geostring)

    # Remove state
    geostring = re.sub(',.*?$', '', geostring)

    geostring_after = geostring

    # Covert to lowercase
    geostring = geostring.lower()
    # Remove whitespace
    geostring = ''.join(geostring.split())

    # Remove other characters
    chars_for_removal = "-.,;'"
    
    for char in chars_for_removal:
        geostring = geostring.replace(char, '')

    # Add prefix
    geostring = prefix + geostring

    return geostring

def generate_key(geostring):
    '''Tranform a geostring into a key'''
    return preprocess(geostring)
