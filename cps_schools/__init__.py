from .crosswalk import id_to_name, cps_school_id_to_rcdts_id

def get_school_id(name):
    return id_to_name[name]

def get_rcdts_id(cps_school_id):
    return cps_school_id_to_rcdts_id[cps_school_id]
