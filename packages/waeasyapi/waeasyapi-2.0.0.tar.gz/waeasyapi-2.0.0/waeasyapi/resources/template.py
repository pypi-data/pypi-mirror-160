from .base import Resource
from ..constants.url import URL
import warnings


class Template(Resource):
    def __init__(self, client=None):
        super(Template, self).__init__(client)
        self.base_url = URL.TEMPLATE_URL

    def createTemplate(self, data={}):
        url = "{}/create".format(self.base_url)
        return self.post_url(url, data)

    def getTemplates(self, data={}):
        url = "{}/list".format(self.base_url)
        return self.get_url(url, data)

    def deleteTemplate(self, templateName, data={}):
        url = "{}/delete".format(self.base_url, templateName)
        return self.delete_url(url, data)

    
