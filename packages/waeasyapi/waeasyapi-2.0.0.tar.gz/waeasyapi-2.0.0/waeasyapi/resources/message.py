from .base import Resource
from ..constants.url import URL
import warnings


class Message(Resource):
    def __init__(self, client=None):
        super(Message, self).__init__(client)
        self.base_url = URL.MESSAGE_URL

    def sendTextMessage(self, data={}):
        url = "{}/text".format(self.base_url)
        return self.post_url(url, data)

    def sendImageMessage(self, data={}):
        url = "{}/image".format(self.base_url)
        return self.post_url(url, data)

    def sendVideoMessage(self, data={}):
        url = "{}/video".format(self.base_url)
        return self.post_url(url, data)

    def sendAudioMessage(self, data={}):
        url = "{}/audio".format(self.base_url)
        return self.post_url(url, data)

    def sendVoiceMessage(self, data={}):
        url = "{}/voice".format(self.base_url)
        return self.post_url(url, data)

    def sendURLMessage(self, data={}):
        url = "{}/url".format(self.base_url)
        return self.post_url(url, data)

    def sendTemplateMessage(self, data={}):
        url = "{}/template".format(self.base_url)
        return self.post_url(url, data)

    def sendDocumentMessage(self, data={}):
        url = "{}/document".format(self.base_url)
        return self.post_url(url, data)

    def sendStickerMessage(self, data={}):
        url = "{}/sticker".format(self.base_url)
        return self.post_url(url, data)

    def sendLocationMessage(self, data={}):
        url = "{}/location".format(self.base_url)
        return self.post_url(url, data)

    def sendContactMessage(self, data={}):
        url = "{}/contacts".format(self.base_url)
        return self.post_url(url, data)

    def sendInteractiveMessage(self, data={}):
        url = "{}/interactive".format(self.base_url)
        return self.post_url(url, data)

    
