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
            for key in key_list:
                if key[0] == geostring:
                    return key[0]
        # Otherwise, search for and find the prefix.
        else:
            geostring = ':' + geostring
            length = len(geostring)

            if not print_mode:
                for key in pool:
                    if key[0][-length:] == geostring:
                            return key[0]
            else:
                for key in pool:
                    if key[0][-length:] == geostring:
                            print(key[0])
    # A population was specified.
    else:
        if has_prefix(geostring):
            for key in key_list:
                if key[0] == geostring:
                    return key[0]
        else:
            # Remove all chars that aren't digits.
            population = re.sub('[^0-9]', '', population)
            # Convert to int
            population = int(population)

            matches = []

            geostring = ':' + geostring
            length = len(geostring)

            for key in pool:
                if key[0][-length:] == geostring:
                        matches.append(key)

            if not print_mode:
                if len(matches) == 0:
                    return None
                if len(matches) == 1:
                    return matches[0][0]
                else:
                    matches = sorted(matches, key=lambda x: abs(x[2] - population))
                    return matches[0][0]
            else:
                if len(matches) == 0:
                    print(None)
                if len(matches) == 1:
                    print(matches[0][0])
                else:
                    matches = sorted(matches, key=lambda x: abs(x[2] - population))
                    print(matches[0][0])


