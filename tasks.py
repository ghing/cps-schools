import sys

if sys.version_info[0] == 2:
    import unicodecsv as csv
else:
    import csv

import os.path

import dataset
from invoke import task

from cps_schools.datasource import registry

DEFAULT_DATABASE = "postgresql://localhost:5432/cps_schools"

@task
def fetch(data_directory, datasource_slug=None):
    if datasource_slug is None:
        datasource_classes = registry.all()
    else:
        datasource_classes = [registry.get(datasource_slug)]

    for datasource_cls in datasource_classes:
        datasource = datasource_cls()
        for filename, f in datasource.fetch():
            with open(os.path.join(data_directory, filename), 'wb') as outf:
                outf.write(f.read())


@task
def load(data_directory, database=DEFAULT_DATABASE,
         datasource_slug=None):
    db = dataset.connect(database)
    table = db['schools']

    if datasource_slug is None:
        datasource_classes = registry.all()
    else:
        datasource_classes = [registry.get(datasource_slug)]

    for datasource_cls in datasource_classes:
        datasource = datasource_cls()

        for rows in datasource.load_rows(data_directory):
            table.insert_many(rows)


@task
def generate_name_to_id_crosswalk(database=DEFAULT_DATABASE):
    db = dataset.connect(database)
    query = """
    SELECT DISTINCT school_id, name
    FROM schools
    WHERE school_id != ''
    """
    writer = csv.DictWriter(sys.stdout, fieldnames=(('school_id', 'name')))
    writer.writeheader()
    for row in db.query(query):
        writer.writerow(row)

    query = """
    SELECT DISTINCT school_id, name_full as name
    FROM schools
    WHERE name_full IS NOT NULL AND school_id != ''
    """
    for row in db.query(query):
        writer.writerow(row)

    query = """
    SELECT DISTINCT school_id, name_2 as name
    FROM schools
    WHERE name_2 IS NOT NULL AND school_id != ''
    """
    for row in db.query(query):
        writer.writerow(row)


@task
def generate_cps_id_to_rcdts_id_crosswalk(database=DEFAULT_DATABASE):
    db = dataset.connect(database)
    query = """
    SELECT DISTINCT school_id, rcdts_id
    FROM schools
    WHERE school_id != ''
    AND rcdts_id IS NOT NULL
    AND rcdts_id != ''
    """
    writer = csv.DictWriter(sys.stdout, fieldnames=(('school_id', 'rcdts_id')))
    writer.writeheader()
    for row in db.query(query):
        writer.writerow(row)
