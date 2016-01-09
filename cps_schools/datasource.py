import csv
import os
import StringIO

import requests

class SchoolDatasourceRegistry(object):
    def __init__(self):
        self._datasources = {}

    def register(self, datasource_cls):
        self._datasources[datasource_cls.slug] = datasource_cls

    def get(self, slug):
        return self._datasources[slug]

    def all(self):
        return self._datasources.values()


registry = SchoolDatasourceRegistry()


class BaseDatasource(object):
    @property
    def files(self):
        return [(self.filename, self.url)]

    def fetch(self):
        for filename, url in self.files:
            r = requests.get(url)
            yield (filename, StringIO.StringIO(r.content))

    @classmethod
    def normalize_row(cls, row):
        normalized = {
            'source': cls.slug,        
            'school_year': cls.school_year,
        }
        for orig, normal, parser in cls.column_map:
            normalized[normal] = parser(row[orig])

        return normalized    


class Schools20132014Datasource(BaseDatasource):
    slug = "cps-schools-2013-2014"
    school_year = "2013-2014" 
    homepage = "https://data.cityofchicago.org/Education/CPS-Schools-2013-2014-Academic-Year/c7jj-qjvh"
    url = 'https://data.cityofchicago.org/api/views/c7jj-qjvh/rows.csv?accessType=DOWNLOAD'
    filename = "CPS_Schools_2013-2014_Academic_Year.csv"
    column_map = [
            ('SchoolID', 'school_id', str),
            ('SchoolName', 'name', str),
            ('FullName', 'name_full', str),
            ('SchoolName2', 'name_2', str),
            ('ZIP', 'zip', str),
            ('NCES ID', 'nces_id', str),
            ('CPS Unit', 'cps_unit', str),
            ('ISBE ID', 'rcts_id', str),
            ('Governance', 'governance', str),
            ('Grade Structure', 'grade_category', str),
            ('Attending Grades', 'grades', str),
            ('Latitude', 'lat', float),
            ('Longitude', 'lon', float),
        ]

    # TODO: Implement normalize_row to
    # Merge "Street Number", "Street Direction", "Street Name", "City"
    # and "State" into a single "address" field

    def load_rows(self, data_directory):
        for filename, _ in self.files:
            with open(os.path.join(data_directory, filename)) as f:
                reader = csv.DictReader(f)
                yield [self.normalize_row(r) for r in reader]

registry.register(Schools20132014Datasource)

    
class SchoolLocations20152016Datasource(BaseDatasource):
    slug = "cps-school-locations-2015-2016"
    school_year = "2015-2016"
    homepage = "https://data.cityofchicago.org/Education/CPS-School-Locations-SY1516/2mts-wp7t"
    url = "https://data.cityofchicago.org/api/views/mb74-gx3g/rows.csv?accessType=DOWNLOAD"
    filename = "CPS_School_Locations_SY1516.csv"
    column_map = [
        ('School_ID', 'school_id', str),
        ('Short_Name', 'name', str),
        ('Address', 'address', str),
        ('Zip', 'zip', str),
        ('Lat', 'lat', float),
        ('Long', 'lon', float),
        ('Network', 'network', str),
        ('Governance', 'governance', str),
        ('Grade_Cat', 'grade_category', str),
        ('Grades', 'grades', str),
    ]
    # TODO: Somehow save additional fields, or decide definitively not to do
    # this
    # * Geographic network
    # * Community area
    # * Ward
    # * Alderman

    def load_rows(self, data_directory):
        for filename, _ in self.files:
            with open(os.path.join(data_directory, filename)) as f:
                reader = csv.DictReader(f)
                yield [self.normalize_row(r) for r in reader]



registry.register(SchoolLocations20152016Datasource)
