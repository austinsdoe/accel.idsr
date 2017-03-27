"""A flask endpoint for accessing the jsonapi.
Any javascript code that needs to talk to bika lims should use this URL.
"""

import json
import urllib
import urllib2

from config import settings


class JSONAPI(object):
    def __init__(self):
        self.plone_site_url = settings['plone_site_url']
        self.jsonapi_url = '/'.join([self.plone_site_url, '@@API'])
        self.username = settings['jsonapi_username']
        self.password = settings['jsonapi_password']
        # We will attempt to connect at first startup, and so there is a
        # requirement that a Bika LIMS server can be contacted before this
        # application will start!
        self.opener = self._connect()

    def _connect(self):
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        login_url = '/'.join([self.plone_site_url, 'login_form'])
        try:
            params = urllib.urlencode({
                "form.submitted": 1,
                "pwd_empty": 0,
                "__ac_name": self.username,
                "__ac_password": self.password,
                "submit": "Log in"
            })
            f = opener.open(login_url, params)
            data = f.read()
            f.close()
            return opener
        except urllib2.HTTPError as e:
            if e.code == 404:
                raise RuntimeError(
                    "Login page at '%s' was not found (404)." % login_url)
        except urllib2.URLError as e:
            if e.reason.errno == 111:
                raise RuntimeError(
                    "Bika LIMS server at '%s' cannot be contacted (111)." %
                    self.plone_site_url)

    def get_index_values(self, **kwargs):
        url = '/'.join([self.jsonapi_url, 'get_index_values'])
        f = self.opener.open(url, data=urllib.urlencode(kwargs))
        data = f.read()
        f.close()
        return json.loads(data)

    def read(self, **kwargs):
        url = '/'.join([self.jsonapi_url, 'read'])
        f = self.opener.open(url, data=urllib.urlencode(kwargs))
        print type(f)
        print f
        data = f.read()
        f.close()
        return json.loads(data)

    def update(self, **kwargs):
        url = '/'.join([self.jsonapi_url, 'update'])
        pass
        f = self.opener.open(url, data=urllib.urlencode(kwargs))
        data = f.read()
        f.close()
        return json.loads(data)

    def create(self, **kwargs):
        url = '/'.join([self.jsonapi_url, 'create'])
        f = self.opener.open(url, data=urllib.urlencode(kwargs))
        data = f.read()
        f.close()
        return json.loads(data)
