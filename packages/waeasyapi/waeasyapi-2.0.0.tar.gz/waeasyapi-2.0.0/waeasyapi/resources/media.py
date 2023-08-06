from .base import Resource
from ..constants.url import URL
import warnings


class Media(Resource):
    def __init__(self, client=None):
        super(Media, self).__init__(client)
        self.base_url = URL.MEDIA_URL

    def getMedia(self, mediaId, data={}):
        url = "{}/retrieve".format(self.base_url, mediaId)
        return self.get_url(url, data)

    
