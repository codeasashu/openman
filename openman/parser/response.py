import json
import uuid
from ..errors import ResponseParserException,  RequestParserException
from ..utils import filter_env_var, is_response, map_to_dict, \
    strip_charset
from .request import Request

class Response(object):

    def __init__(self, response=None):
        if (response is None) \
            or (not isinstance(response, dict) \
                or (not is_response(response))):
            raise ResponseParserException('Not a valid response')
        self.response = response
        self.uuid = uuid.uuid4()
    
    @classmethod
    def parse(cls, response=None):
        return cls(response)
    
    @property
    def code(self):
        return self.get_code()
    
    @property
    def id(self):
        return self.get_id()
    
    @property
    def headers(self):
        return self.get_headers()
    
    @property
    def content_type(self):
        return self.get_content_type()
    
    @property
    def body(self):
        return self.get_body()
    
    @property
    def description(self):
        return self.get_description()
    
    @property
    def example(self):
        return self.get_example()
    
    def get_id(self):
        return str(self.uuid)
    
    def get_code(self, default_code=200):
        return self.response.get('code', default_code)
    
    def get_description(self):
        return self.response.get('name', '')
    
    def get_headers(self, header=None):
        """
        Return headers for given response.
        if `header` is provided, it returns
        the first matching header value
        """
        if header is None:
            return map_to_dict(self.response['header'])
        for name, value in map_to_dict(self.response.get('header') or []).items():
            # @TODO name.lower() in header.lower() might be better
            if header and (name.lower() == header.lower()):
                return value
        return None
    
    def get_content_type(self):
        header = self.get_headers('Content-Type') or '*/*'
        return strip_charset(header)
    
    def get_body(self):
        responsebody = self.response['body'] if 'body' in self.response \
                        else None
        try:
            return json.loads(responsebody)
        except Exception:
            return responsebody
    
    def get_example(self):
        if 'originalRequest' in self.response:
            try:
                return Request(self.response['originalRequest'])
            except RequestParserException:
                pass
        return None