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

def partial_match(geostring, key):
    '''Determine if geostring is a partial match for a key'''

    # Currently, there are only two option strings in geokeys.
    option_strings = ['', '/', '//']

    for option_string in option_strings:
        length = len(geostring + option_string) + 1
        if ':' + geostring + option_string == key[-length:]:
            return True

    return False

def get_partial_matches(geostring, pool):
    '''Get a key for which the context is not known'''

    matches = []

    for key in pool:
        if partial_match(geostring, key[0]):
                matches.append(key)

    return matches

def get_key(geostring, pool, population, print_mode=False):
    '''
    This function is intended for non-Census geostrings after key_list
    is available
    '''
    geostring = preprocess(geostring)

    if population == -1:
        # Otherwise, search for and find the prefix.
        matches = get_partial_matches(geostring, pool)

        if not print_mode:
            return matches[0]
        else:
            for match in matches:
                print(match[0])
    # A population was specified.
    else:
        # Remove all chars that aren't digits.
        population = re.sub('[^0-9]', '', population)
        # Convert to int
        try:
            population = int(population)
        except ValueError:
            population = 0

        matches = get_partial_matches(geostring, pool)
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
            print(candidate)
