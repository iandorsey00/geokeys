'''
Tools primarily intended for non-Census strings representing places. For use
after keys have been initially generated.
'''

import sys

from basic_tools import preprocess
from keys import key_list

def has_prefix(geostring):
    '''Does the string have a prefix, e.g. 'us:ca:'?'''
    return ':' in geostring

def get_key(geostring):
    '''
    This function is intended for non-Census geostrings after key_list
    is available
    '''
    geostring = preprocess(geostring)

    # If the string already has a prefix, we are done.
    if has_prefix(geostring):
        return geostring
    # Otherwise, search for and find the prefix.
    else:
        geostring = ':' + geostring
        length = len(geostring)
        for key in key_list:
            if key[0][-length:] == geostring:
                return key[0]
