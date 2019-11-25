from ..errors import RequestParserException
from ..utils import filter_env_var, is_request, format_path, \
    map_to_dict

# Postman to Content-Type mapping
request_contenttype_map = {
    "raw": '*/*',
    "text": "text/plain",
    "json": "application/json",
    "urlencoded": 'application/x-www-form-urlencoded',
    "formdata": 'multipart/form-data',
}

class Request(object):

    def __init__(self, request=None):
        if (request is None) \
            or (not isinstance(request, dict) \
                or (not is_request(request))):
            raise RequestParserException('Not a valid request')
        self.request = request
    
    @classmethod
    def parse(cls, request=None):
        return cls(request)

    @property
    def description(self):
        return self.get_description()

    @property
    def path(self):
        return self.get_path(True)
    
    @property
    def method(self):
        return self.get_method()
    
    @property
    def query_string(self):
        return self.get_query_string()
    
    @property
    def headers(self):
        return self.get_headers()
    
    @property
    def body(self):
        return self.get_body()
    
    @property
    def body_contenttype(self):
        return self.get_body_contenttype()
    
    def get_description(self):
        return self.request.get('description')

    def get_path(self, formatted=False):
        path = list(map(
            lambda path: path[1:-1] if filter_env_var(path) else path,
            self.request['url']['path']))
        return format_path(path) if formatted else path 

    # Return LOWERCASED method name
    # @TODO Make some constant in class to refer method name
    # so that other classes can use constants instead of hardcoded
    def get_method(self):
        return self.request['method'].lower() if 'method' in self.request else None
    
    def get_query_string(self):
        if self.request['url'].get('query', None) is None:
            return None
        return map_to_dict(self.request['url'].get('query'))
    
    def get_headers(self, header=None):
        if header is None:
            return map_to_dict(self.request['header'])
        for name, value in map_to_dict(self.request['header']).items():
            if name.lower() == header.lower():
                return value
        return None

    def get_body(self):
        if 'body' in self.request:
            bodyitem = self.request['body'][self.request['body']['mode']]
            if isinstance(bodyitem, list):
                return map_to_dict(bodyitem)
            return bodyitem
        return None
    
    def get_body_contenttype(self, default='*/*'):
        mode = self.request['body']['mode']
        # We try to deduce from given langugae
        if mode == 'raw' and 'options' in self.request['body']:
            if 'language' in self.request['body']['options']:
                mode = self.request['body']['options']['language'].get(mode, 'raw')
        return request_contenttype_map.get(mode, default)
