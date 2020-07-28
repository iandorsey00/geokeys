'''
This is the script that generates the keys from the place names and populations
in places.py
'''

import sqlite3
import pprint
import sys
from places import places_list
from tools import generate_key

# DuplicateException ##########################################################
class DuplicateException(Exception):
    pass

# Create the database
conn = sqlite3.connect(':memory:')
cur = conn.cursor()

# Create the table
conn.execute('''CREATE TABLE geokeys
                (key TEXT,
                 display_label TEXT,
                 population INTEGER)''')

conn.commit()

# Insert data into table
for place in places_list:
    conn.execute('''INSERT INTO geokeys
                    VALUES(?,?,?)''', (generate_key(place[0]), place[0], place[1]))

conn.commit()

# Get duplicates
cur.execute('''SELECT key, COUNT(*) c
                    FROM geokeys
                    GROUP BY key
                    HAVING c > 1''')

duplicates = cur.fetchall()

for duplicate in duplicates:
    cur.execute('''SELECT * FROM geokeys WHERE key = ?''', (duplicate[0], ))
    these_duplicates = cur.fetchall()
    these_duplicates.sort(key=lambda x: x[2], reverse=True)

    for index, item in enumerate(these_duplicates):
        key = item[0]
        display_label = item[1]
        pop = item[2]
        if index == 1:
            cur.execute('''UPDATE geokeys
                            SET key = ?
                            WHERE key = ? AND display_label = ? AND population = ?''', (key + '/', key, display_label, pop))
            conn.commit()
        elif index == 2:
            cur.execute('''UPDATE geokeys
                            SET key = ?
                            WHERE key = ? AND display_label = ? AND population = ?''', (key + '//', key, display_label, pop))
            conn.commit()

# Get duplicates again
cur.execute('''SELECT key, COUNT(*) c
                    FROM geokeys
                    GROUP BY key
                    HAVING c > 1''')

duplicates = cur.fetchall()

if len(duplicates) > 1:
    raise DuplicateException('There are duplicate keys in the database.')

# Get all records
cur.execute('''SELECT * FROM geokeys''')

keys_list_raw = cur.fetchall()

pp = pprint.PrettyPrinter(indent=4)
keys_list = 'keys_list = ' + pp.pformat(keys_list_raw)
print(keys_list)
