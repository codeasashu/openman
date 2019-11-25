from ..errors import RequestItemParserException
from ..utils import is_requestitem
from .request import Request
from .response import Response

class RequestItem(object):
    def __init__(self, requestitem=None):
        if (requestitem is None) \
            or (not isinstance(requestitem, dict) \
                or (not is_requestitem(requestitem))):
            raise RequestItemParserException('Not a valid request')
        self.requestitem = requestitem
        self.request = Request(requestitem['request'])
        self.responses = [Response(item) for item in requestitem['response']]
    
    @classmethod
    def parse(cls, requestitem=None):
        return cls(requestitem)
    
    @property
    def summary(self):
        return self.get_summary()
    
    @property
    def description(self):
        return self.get_description()
    
    def get_summary(self):
        return self.requestitem.get('name')
    
    def get_description(self):
        return self.request.description
    
    def get_request(self):
        return self.request
    
    def get_responses(self):
        return self.responses