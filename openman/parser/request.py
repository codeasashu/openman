import json
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
            # Raw body can be in string, even if content-type is json
            if self.body_contenttype in ["application/json"] \
                    and isinstance(bodyitem, str):
                return json.loads(bodyitem)
            return bodyitem
        return None

    def determine_language(self, body=None):
        if not body:
            return None
        mode = body.get('mode', 'raw')
        if 'options' not in body:
            return mode
        language = body['options'].get('language', None)
        if not language:
            language = body['options'].get(mode, {"language": None})['language']
        return language or mode

    def get_body_contenttype(self, default='*/*'):
        content_type = self.get_headers('Content-Type')
        if content_type:
            return content_type
        # We try to deduce from given langugae
        language = self.determine_language(self.request['body']) or default
        return request_contenttype_map.get(language)
