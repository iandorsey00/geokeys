'''
Tools primarily intended for non-Census strings representing places. For use
after keys have been initially generated.
'''

import sys
import re

from basic_tools import preprocess

def has_prefix(geostring):
    '''Does the string have a prefix, e.g. 'us:ca:'?'''
    return ':' in geostring

def get_exact_match(geostring):
    '''Get the exact match for a geostring that has been finalized'''
        for key in key_list:
            if key[0] == geostring:
                return key[0]

def get_partial_matches(geostring):
    '''Get a key for which the context is not known'''
    geostring = ':' + geostring
    length = len(geostring)

    matches = []

    for key in pool:
        if key[0][-length:] == geostring:
                matches.append(key)

    return matches

def get_key(geostring, pool, population, print_mode=False):
    '''
    This function is intended for non-Census geostrings after key_list
    is available
    '''
    geostring = preprocess(geostring)

    if population == -1:
        # If the string already has a prefix, search for and find the exact
        # string.
        if has_prefix(geostring):
            get_exact_match(geostring)
        # Otherwise, search for and find the prefix.
        else:
            matches = get_partial_matches(geostring)

            if not print_mode:
                return matches
            else:
                for match in matches:
                    print(match)
    # A population was specified.
    else:
        if has_prefix(geostring):
            get_exact_match(geostring)
        else:
            # Remove all chars that aren't digits.
            population = re.sub('[^0-9]', '', population)
            # Convert to int
            population = int(population)

            matches = get_partial_matches(geostring)
            candidate = ''

            # If there is more than one match, select the one with the closest
            # population.
            if len(matches) == 1:
                candidate = matches[0][0]
            elif len(matches) > 1:
                matches = sorted(matches, key=lambda x: abs(x[2] - population))
                candidate = matches[0][0]

            # Return or print the match
            if not print_mode:
                return candidate
            else:
                print candidate
