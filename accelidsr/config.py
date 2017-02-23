"""Parse the init file and return a neat settings dict
"""

from ConfigParser import ConfigParser
import os.path

config = ConfigParser()

dirname = os.path.dirname(__file__)
config.read(os.path.join(dirname, "accel.idsr.ini"))
if not config.has_section("bika_lims"):
    print("Adding [bika_lims] section to accel.idsr.ini with default values")
    config.add_section("bika_lims")
    config.set("bika_lims", "plone_site_url", "http://localhost:8080/Plone")
    config.set("bika_lims", "jsonapi_username", "admin")
    config.set("bika_lims", "jsonapi_password", "adminsecret")
    config.write(open('accel.idsr.ini', 'w'))

settings = {
    "plone_site_url": config.get("bika_lims", "plone_site_url").strip('/'),
    "jsonapi_username": config.get("bika_lims", "jsonapi_username"),
    "jsonapi_password": config.get("bika_lims", "jsonapi_password"),
}
