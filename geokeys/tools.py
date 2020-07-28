import re

from places import places_list

def get_state(geostring):
    if geostring == 'Islamorada, Village of Islands village; Florida':
        return 'Florida'
    elif geostring == 'Lynchburg, Moore County metropolitan government; Tennessee':
        return 'Tennessee'
    else:
        state = re.search(', (.*?)$', geostring)
        return state.group(1)

def get_prefix(state):
    prefixes = {
        'Alabama': 'us:al:',
        'Alaska': 'us:ak:',
        'Arizona': 'us:az:',
        'Arkansas': 'us:ar:',
        'California': 'us:ca:',
        'Colorado': 'us:co:',
        'Connecticut': 'us:ct:',
        'Delaware': 'us:de:',
        'District of Columbia': 'us:dc:',
        'Florida': 'us:fl:',
        'Georgia': 'us:ga:',
        'Hawaii': 'us:hi:',
        'Idaho': 'us:id:',
        'Illinois': 'us:il:',
        'Indiana': 'us:in:',
        'Iowa': 'us:ia:',
        'Kansas': 'us:ks:',
        'Kentucky': 'us:ky:',
        'Louisiana': 'us:la:',
        'Maine': 'us:me:',
        'Maryland': 'us:md:',
        'Massachusetts': 'us:ma:',
        'Michigan': 'us:mi:',
        'Minnesota': 'us:mn:',
        'Mississippi': 'us:ms:',
        'Missouri': 'us:mo:',
        'Montana': 'us:mt:',
        'Nebraska': 'us:ne:',
        'Nevada': 'us:nv:',
        'New Hampshire': 'us:nh:',
        'New Jersey': 'us:nj:',
        'New Mexico': 'us:nm:',
        'New York': 'us:ny:',
        'North Carolina': 'us:nc:',
        'North Dakota': 'us:nd:',
        'Ohio': 'us:oh:',
        'Oklahoma': 'us:ok:',
        'Oregon': 'us:or:',
        'Pennsylvania': 'us:pa:',
        'Rhode Island': 'us:ri:',
        'South Carolina': 'us:sc:',
        'South Dakota': 'us:sd:',
        'Tennessee': 'us:tn:',
        'Texas': 'us:tx:',
        'Utah': 'us:ut:',
        'Vermont': 'us:vt:',
        'Virginia': 'us:va:',
        'Washington': 'us:wa:',
        'West Virginia': 'us:wv:',
        'Wisconsin': 'us:wi:',
        'Wyoming': 'us:wy:',
    }

    return prefixes[state]

def generate_key(geostring):
    '''Tranform a geostring into a key'''
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

    # Get state and prefix
    state = get_state(geostring)
    prefix = get_prefix(state)

    # Remove place_type
    geostring = re.sub(' city,.*?$', '', geostring)
    geostring = re.sub(' town,.*?$', '', geostring)
    geostring = re.sub(' CDP,.*?$', '', geostring)
    geostring = re.sub(' borough,.*?$', '', geostring)
    geostring = re.sub(' municipality,.*?$', '', geostring)
    geostring = re.sub(' village,.*?$', '', geostring)
    geostring = re.sub(' corporation,.*?$', '', geostring)
    geostring = re.sub(' CDP \(.*?\),.*?$', '', geostring)
    geostring = re.sub(' city \(.*?\),.*?$', '', geostring)
    geostring = re.sub(' borough \(.*?\),.*?$', '', geostring)
    geostring = re.sub(' village \(.*?\),.*?$', '', geostring)
    # geostring = re.sub(' \(balance\),.*?$', '', geostring)
    # geostring = re.sub(' metropolitan government \(balance\),.*?$', '', geostring)
    # geostring = re.sub(' metro government \(balance\),.*?$', '', geostring)
    # geostring = re.sub(' consolidated government \(balance\),.*?$', '', geostring)
    # geostring = re.sub(' consolidated government,.*?$', '', geostring)
    # geostring = re.sub(' urban government,.*?$', '', geostring)
    # geostring = re.sub(' urban county,.*?$', '', geostring)
    # geostring = re.sub(' unified government,.*?$', '', geostring)
    geostring_after = geostring

    # Covert to lowercase
    geostring = geostring.lower()
    # Remove whitespace
    geostring = ''.join(geostring.split())
    # Remove other characters
    geostring = geostring.replace('-', '')
    geostring = geostring.replace('.', '')
    geostring = geostring.replace(',', '')
    geostring = geostring.replace(';', '')
    geostring = geostring.replace("'", '')

    return prefix + geostring
