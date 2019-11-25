import json
from ..schema_converter import SchemaConvertor
from ..utils import camelize, DEFAULT_STATUS_CODE

class Operation(object):

    def __init__(self, request_item, ignorespec=None):
        self.request_item = request_item
        self.ignorespec = ignorespec
    
    def get_path(self, normalized=False):
        return self.request_item.get_request().get_path(normalized)
    
    def get_method(self):
        return self.request_item.get_request().get_method()

    def id(self):
        return camelize(self.get_path(True) +' '+ self.get_method())
    
    def get_ignores(self, path, method, code):
        if not self.ignorespec:
            return []
        if 'schema' not in self.ignorespec:
            return []
        for _path, schemas in self.ignorespec['schema'].items():
            if camelize(_path) == camelize(str(path)):
                for _method, responsecode in schemas.items():
                    if _method == method:
                        return responsecode.get(int(code), [])
        return []
        
    def get(self):
        _operation = dict()
        method = self.get_method()
        _operation[method] = dict(
            operationId = self.id(),
            summary = self.request_item.summary,
        )

        if self.request_item.description:
            _operation[method]['description'] = self.request_item.description

        #params
        params = self.parameters()
        if len(params):
            _operation[method]['parameters'] = params
        
        #request body
        requestbody = self.request_body()
        if requestbody:
            _operation[method]['requestBody'] = requestbody
        
        #responses
        _operation[method]['responses'] = self.responses() or\
             {DEFAULT_STATUS_CODE: {'description': ''}}
        
        return  _operation

    def responses(self):
        response_schema = dict()
        for response in self.request_item.get_responses():
            ignoreschema = self.get_ignores(self.get_path(), self.get_method(), response.code)
            schema = SchemaConvertor.convert(response.body, ignore=ignoreschema)
            exampleDescription = self.id() + str(response.code)
            response_content = dict()
            response_content[response.content_type] = dict(
                schema = schema,
                examples = {
                    camelize(response.description): {
                        'value': response.body,
                        'x-response-id': response.id
                    },
                },
            )
            response_schema[int(response.code)] = dict(
                content = response_content,
                description = response.description
            )
        return response_schema
    
    def append_param_example(self, location, name, responses=None):
        """
        This extracts the param `name` in `location` (ex- query, header etc)
        from resonse example and append them to the location
        """
        if not responses:
            responses = self.request_item.get_responses()
        links = []
        for response in responses:
            example_request = response.get_example()

            try:
                for _name, _value in getattr(example_request, location).items():
                    if name == _name:
                        links.append({
                            'value': _value,
                            'x-response-id': response.id
                        })
                        break
            except AttributeError as e:
                pass                
        return links
    
    def append_body_example(self, location, name, responses=None):
        """
        This extracts the param `name` in `location` (ex- query, header etc)
        from resonse example and append them to the location
        """
        if not responses:
            responses = self.request_item.get_responses()
        links = []
        for response in responses:
            example_request = response.get_example()
            if example_request.body:
                links.append({
                    'value': example_request.body,
                    'x-response-id': response.id
                })  
        return links
    
    def parameters(self):
        """
        Constructs OpenAPI Spec compatible parameters spec
        Parameters can be one of four: path, cookie, query, header
        @link https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md#parameter-locations
        """
        params = []
        request = self.request_item.get_request()
        responses = self.request_item.get_responses()
        # Build Query params
        if isinstance(request.query_string, dict):
            for name, value in request.query_string.items():
                query_params = dict()
                query_params['in'] =  'query'
                query_params['name'] = name
                query_params['schema'] = SchemaConvertor.convert(value)
                query_params['schema'].update(dict(example=value))
                query_params['x-link-response'] = []
                # Check if any response has this param in their request
                query_params['x-link-response'] = self.append_param_example('query_string', name, responses)

                params.append(query_params)
        
        # Build headers params
        if isinstance(request.headers, dict):
            for name, value in request.headers.items():
                header_params = dict()
                header_params['in'] =  'header'
                header_params['name'] = name
                header_params['schema'] = SchemaConvertor.convert(value)
                header_params['schema'].update(dict(example=value))
                header_params['x-link-response'] = self.append_param_example('headers', name, responses)
                params.append(header_params)
        
        # Build Path params
        # Build cookie params
        
        return params
    
    def request_body(self):
        request_body = dict()
        request = self.request_item.get_request()
        responses = self.request_item.get_responses()
        if request.body:
            bodyschema = SchemaConvertor.convert(request.body)
            header = request.get_headers('content-type') or '*/*'
            request_body['content'] = {
                header: {
                    'schema': bodyschema,
                    'example': dict(value=request.body),
                    'x-link-response': self.append_body_example('body', request.body, responses)
                }
            }

        return request_body
