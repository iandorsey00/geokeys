import argparse
import csv
import sys

from keys import key_list
from advanced_tools import get_key

class DoubleKeyError(Exception):
    pass

def readcsv(csvfile):
    '''Load rows from the CSV file'''
    out = []

    with open(csvfile) as cf:
        csvreader = csv.reader(cf)
        for row in csvreader:
            out.append(row)

    return out

def merge(args):
    '''Merge data from two CSV files together on geographic names'''
    source_csv = readcsv(args.source_csv)
    target_csv = readcsv(args.target_csv)

    source_geo_names = list(map(lambda x: (x[0], x[1][0]), enumerate(source_csv)))
    target_geo_names = list(map(lambda x: (x[0], x[1][0]), enumerate(target_csv)))

    source_keys_and_geo_names = list(map(lambda x: (x[0], get_key(x[1]), x[1]), source_geo_names))
    target_keys_and_geo_names = list(map(lambda x: (x[0], get_key(x[1]), x[1]), target_geo_names))

    keys = []
    matches = []

    for source_id, source_key, geo_name in source_keys_and_geo_names:
        these_matches = []
        for target_id, target_key, geo_name in target_keys_and_geo_names:
            if source_key == target_key and source_key not in keys:
                these_matches.append((source_id, target_id))
                keys.append(source_key)
            
        # if len(these_matches) > 1:
        #     raise DoubleKeyError("Key relationship not one-to-one.")
        # elif len(these_matches) == 1:
        #     matches.append(these_matches[0])

        matches += these_matches

    csvwriter = csv.writer(sys.stdout)

    for source_id, target_id in matches:
        csvwriter.writerow(source_csv[source_id] + target_csv[target_id])

def query(args):
    # If a context was specified, narrow the pool (the keys to search)
    if args.context:
        pool = [i for i in key_list if i[0].startswith(args.context)]
    else:
        pool = key_list

    if args.population:
        population = args.population
    else:
        population = -1

    get_key(args.geostring, pool, population, print_mode=True)

###############################################################################
# Argument parsing with argparse

# Create the top-level argument parser
parser = argparse.ArgumentParser(
    description='A program that joins data about geographies on their names')
# Create top-level subparsers
subparsers = parser.add_subparsers(
    help='enter geokeys <subcommand> -h for more information.')

# Create the parsor for the "merge" command
merge_parser = subparsers.add_parser('merge', description='Merge data from two CSV files')
merge_parser.add_argument('-p', '--population', action='store_true', help='Specify populations for better matches')
merge_parser.add_argument('-c', '--context', help='Specify a context for better matches')
merge_parser.add_argument('source_csv', help='The CSV file to which to join data')
merge_parser.add_argument('target_csv', help='The CSV file that contains data to be joined')
merge_parser.set_defaults(func=merge)

# Create the parsor for the "query" command
query_parser = subparsers.add_parser('query', description='Query a string for a key')
query_parser.add_argument('-p', '--population', help='Specify population for a better match')
query_parser.add_argument('-c', '--context', help='Specify a context for a better match')
query_parser.add_argument('geostring', help='The string to query for a key')
query_parser.set_defaults(func=query)

# Parse arguments
args = parser.parse_args()
args.func(args)