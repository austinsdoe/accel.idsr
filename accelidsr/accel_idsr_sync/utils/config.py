"""Parse the init file and return a neat settings dict
"""

from ConfigParser import ConfigParser
import os.path

config = ConfigParser()

dirname = os.path.dirname(__file__)
config.read(os.path.join(dirname, "config.ini"))
if not config.has_section("bika_lims"):
    print("Adding [bika_lims] section to config.ini with default values")
    config.add_section("bika_lims")
    config.set("bika_lims", "plone_site_url", "http://localhost:8080/Plone")
    config.set("bika_lims", "plone_site_name", "Plone")
    config.set("bika_lims", "jsonapi_username", "admin")
    config.set("bika_lims", "jsonapi_password", "adminsecret")
    config.write(open('config.ini', 'w'))

settings = {
    "plone_site_url": config.get("bika_lims", "plone_site_url").strip('/'),
    "plone_site_name": config.get("bika_lims", "plone_site_name"),
    "jsonapi_username": config.get("bika_lims", "jsonapi_username"),
    "jsonapi_password": config.get("bika_lims", "jsonapi_password"),
    "db_host": config.get("database", "host"),
    "db_port": int(config.get("database", "port")),
    "db_name": config.get("database", "name"),
}

intervals = {
    "county": int(config.get("intervals", "county"))*60,
    "district": int(config.get("intervals", "district")*60),
    "aprofile": int(config.get("intervals", "analysisprofile"))*60,
    "sampletype": int(config.get("intervals", "sampletype"))*60,
    "disease": int(config.get("intervals", "disease"))*60,
    "facility": int(config.get("intervals", "facility"))*60,
    "idsrform": int(config.get("intervals", "idsrform"))*60,
    "caseoutcome": int(config.get("intervals", "caseoutcome"))*60
}

COUNTY_CODES = [
    {"title": "Bomi", "tla": "BOM", "bika_code": "15"},
    {"title": "Bong", "tla": "BON", "bika_code": "01"},
    {"title": "Gbarpolu", "tla": "GBR", "bika_code": "21"},
    {"title": "Grand Bassa", "tla": "GRB", "bika_code": "11"},
    {"title": "Grand Cape Mount", "tla": "GRC", "bika_code": "12"},
    {"title": "Grand Gedeh", "tla": "GRG", "bika_code": "19"},
    {"title": "Grand Kru", "tla": "GRK", "bika_code": "16"},
    {"title": "Lofa", "tla": "LOF", "bika_code": "20"},
    {"title": "Margibi", "tla": "MAR", "bika_code": "17"},
    {"title": "Maryland", "tla": "MAL", "bika_code": "13"},
    {"title": "Montserrado", "tla": "MON", "bika_code": "14"},
    {"title": "Nimba", "tla": "NIM", "bika_code": "09"},
    {"title": "River Gee", "tla": "RGE", "bika_code": "22"},
    {"title": "River Cess", "tla": "RIV", "bika_code": "18"},
    {"title": "Sinoe", "tla": "SIN", "bika_code": "10"},
]
