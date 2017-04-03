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
    config.set("bika_lims", "jsonapi_username", "admin")
    config.set("bika_lims", "jsonapi_password", "adminsecret")
    config.write(open('config.ini', 'w'))

settings = {
    "plone_site_url": config.get("bika_lims", "plone_site_url").strip('/'),
    "jsonapi_username": config.get("bika_lims", "jsonapi_username"),
    "jsonapi_password": config.get("bika_lims", "jsonapi_password"),
    "db_host": config.get("database", "host"),
    "db_port": int(config.get("database", "port")),
    "db_name": config.get("database", "name"),
}

intervals = {
    "country": int(config.get("intervals", "country"))*60,
    "district": int(config.get("intervals", "district")*60),
    "aprofile": int(config.get("intervals", "analysisprofile"))*60,
    "sampletype": int(config.get("intervals", "sampletype"))*60,
    "disease": int(config.get("intervals", "disease"))*60,
    "idsrform": int(config.get("intervals", "idsrform"))*60,
}
