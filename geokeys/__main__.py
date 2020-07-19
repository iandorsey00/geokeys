import csv

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

    source_geo_names = list(map(lambda x: x[0], source_csv))
    target_geo_names = list(map(lambda x: x[0], target_csv))

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