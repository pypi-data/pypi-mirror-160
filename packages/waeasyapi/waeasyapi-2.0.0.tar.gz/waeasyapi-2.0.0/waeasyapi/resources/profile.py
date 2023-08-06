from .base import Resource
from ..constants.url import URL
import warnings


class Profile(Resource):
    def __init__(self, client=None):
        super(Profile, self).__init__(client)
        self.base_url = URL.PROFILE_URL

    def getProfilePhoto(self, data={}):
        url = "{}/photo".format(self.base_url)
        return self.get_url(url, data)

    def getProfileAbout(self, data={}):
        url = "{}/about".format(self.base_url)
        return self.get_url(url, data)

    def getBusinessProfile(self, data={}):
        url = "{}/business-profile".format(self.base_url)
        return self.get_url(url, data)

    def deleteProfilePhoto(self, data={}):
        url = "{}/photo".format(self.base_url)
        return self.delete_url(url, data)

    def changeProfilePhoto(self, data={}):
        url = "{}/photo".format(self.base_url)
        return self.post_url(url, data)

    def changeProfileAbout(self, data={}):
        url = "{}/about".format(self.base_url)
        return self.post_url(url, data)

    def changeBusinessProfile(self, data={}):
        url = "{}/business-profile".format(self.base_url)
        return self.post_url(url, data)
