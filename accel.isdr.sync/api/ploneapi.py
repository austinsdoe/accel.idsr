from utils import config
from utils.config import settings
import json
import urllib
import urllib2


class PloneApi:
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

    def getContent(self, content_type, **kwargs):
        url = self.jsonapi_url + '/plone/api/1.0/search?portal_type='\
            + content_type
        for key, value in kwargs.iteritems():
            url += "&%s=%s" % (key, value)
        if 'limit' not in kwargs:
            url += '&limit=9999'
        result = self.send_request(url)
        return result

    def getGeo(self, content):
        """
        Getting Geo objects from Bika Instance using JsonAPi
        :param content: can be 'Districts' or 'States' for now.
        :type content: String
        """
        url = self.plone_site_url + '/getGeo'+content
        url += '?country=Liberia'
        result = self.send_request(url)
        return result

    def create(self, obj):
        """
        Creates an object using Plone Api Routing.
        :param obj: object to be created
        :type obj: any object type with get_api_format function
        """
        url = self.jsonapi_url + '/create'
        params = urllib.urlencode(obj.get_api_format())
        result = self.send_request(url, params)
        return result

    def getUID(self, obj_id, portal_type=None):
        url = self.jsonapi_url + '/plone/api/1.0/search?id='+obj_id
        if portal_type:
            url += '&portal_type='+portal_type
        result = self.send_request(url)
        return result['items'][0]['uid']

    def send_request(self, url, params=None):
        try:
            if params:
                f = self.opener.open(url, params)
            else:
                f = self.opener.open(url)
            data = f.read()
            f.close()
            return json.loads(data)
        except Exception, e:
            return {"errors": str(e),
                    "message": str(e)}
