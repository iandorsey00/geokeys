import sys

from basic_tools import preprocess
from keys import key_list

def has_prefix(geostring):
    return ':' in geostring

def get_key(geostring):
    '''
    This function is intended for non-Census geostrings after key_list
    is available
    '''
    geostring = preprocess(geostring)

    if has_prefix(geostring):
        return geostring
    else:
        geostring = ':' + geostring
        length = len(geostring)
        for key in key_list:
            if key[0][-length:] == geostring:
                return key[0]
