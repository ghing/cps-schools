cps_schools
===========

Python package for handling Chicago Public School schools.

Data loading
------------

First create a database:

    createdb cps_schools

Regenerating crosswak files
---------------------------

    invoke generate_name_to_id_crosswalk > cps_schools/data/name_to_id_crosswalk.csv
