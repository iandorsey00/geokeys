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

def get_pool(args_context):
    if args_context:
        return [i for i in key_list if i[0].startswith(args.context)]
    else:
        return key_list

def get_data_dictionary(csvrows, pool, geostring_column=0, population_column=1):
    '''Construct (key, data_row) dictionaries'''
    data_dictionary = dict()

    for row in csvrows:
        if args.population:
            population = row[population_column]
        else:
            population = -1

        data_dictionary[get_key(row[geostring_column], pool, population)] = row

    return data_dictionary

def merge(args):
    '''Merge data from two CSV files together on geographic names'''
    # If a context was specified, narrow the pool (the keys to search)
    pool = get_pool(args.context)

    source_csv = readcsv(args.source_csv)
    target_csv = readcsv(args.target_csv)

    # Default values for the indexes of the *g*eostrings and *p*opulations
    # for the *s*ource CSV and the *t*arget CSV
    sg = 0
    sp = 1
    tg = 0
    tp = 1

    # Set values if specified on the command line.
    if args.sg:
        sg = args.sg
    if args.sp:
        sp = args.sp
    if args.tg:
        tg = args.tg
    if args.tp:
        tp = args.tp

    source_geos = get_data_dictionary(source_csv, pool, geostring_column=sg, population_column=sp)
    target_geos = get_data_dictionary(target_csv, pool, geostring_column=tg, population_column=tp)

    csvwriter = csv.writer(sys.stdout)

    for key in source_geos.keys():
        if key in target_geos.keys():
            csvwriter.writerow(source_geos[key] + target_geos[key])

def query(args):
    # If a context was specified, narrow the pool (the keys to search)
    pool = get_pool(args.context)

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
merge_parser.add_argument('--sg', type=int, help='Index of the geostring column for the source CSV')
merge_parser.add_argument('--sp', type=int, help='Index of the population column for the source CSV')
merge_parser.add_argument('--tg', type=int, help='Index of the geostring column for the target CSV')
merge_parser.add_argument('--tp', type=int, help='Index of the population column for the target CSV')
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