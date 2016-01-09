import csv
import os.path
import sys

import dataset
from invoke import task

from cps_schools.datasource import registry

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
def load(data_directory, database="postgresql://localhost:5432/cps_schools",
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
def generate_name_to_id_crosswalk(database="postgresql://localhost:5432/cps_schools"):
    db = dataset.connect(database)    
    query = """SELECT DISTINCT school_id, name FROM schools"""
    writer = csv.DictWriter(sys.stdout, fieldnames=(('school_id', 'name')))
    writer.writeheader()
    for row in db.query(query):
        writer.writerow(row)
