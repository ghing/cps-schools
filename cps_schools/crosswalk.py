import os.path
import sys
if sys.version_info[0] == 2:
    import unicodecsv as csv
else:
    import csv

def load_crosswalk(path, from_field, to_field):
    crosswalk = {}
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            crosswalk[row[from_field]] = row[to_field]

    return crosswalk        

id_to_name = load_crosswalk(os.path.join(os.path.dirname(__file__),
    'data', 'name_to_id_crosswalk.csv'), 'name', 'school_id')
