import csv
import sys

from tools import generate_key

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

    source_geo_names = list(map(lambda x,y: (x, y[0]), enumerate(source_csv)))
    target_geo_names = list(map(lambda x,y: (x, y[0]), enumerate(target_csv)))

    source_keys_and_geo_names = list(map(lambda x,y: (x, generate_key(y), y), source_geo_names))
    target_keys_and_geo_names = list(map(lambda x,y: (x, generate_key(y), y), target_geo_names))

    matches = []

    for source_id, source_key, geo_name in source_keys_and_geo_names:
        these_matches = []
        for target_id, target_key, geo_name in target_keys_and_geo_names:
            if source_key == target_key:
                these_matches.append((source_id, target_id))
            
        if len(these_matches) > 1:
            raise DoubleKeyError("Key relationship not one-to-one.")
        elif len(these_matches) == 1:
            matches.append(these_matches[0])

    csvwriter = csv.writer()

    for source_id, target_id in match:
        csvwriter.writerow(source_csv[source_id] + target_csv[target_id])

###############################################################################
# Argument parsing with argparse

# Create the top-level argument parser
parser = argparse.ArgumentParser(
    description='A program that joins data about geographies on their names')
parser.set_defaults(func=merge)

# Create arguments
parser.add_argument('source_csv', help='The CSV file to which to join data')
parser.add_argument('target_csv', help='The CSV file that contains data to be joined')

# Parse arguments
args = parser.parse_args()
args.func(args)