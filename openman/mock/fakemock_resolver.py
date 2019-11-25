import random, json
from faker import Faker
from connexion.mock import MockResolver
from ..utils import strip_charset, sanitized
from connexion.utils import all_json
from connexion.http_facts import FORM_CONTENT_TYPES
from connexion.apis.flask_api import FlaskApi

class FakerMockResolver(MockResolver):
    def __init__(self, mock_all):
        super().__init__(mock_all)
        self.faker = Faker()
    
    def example_resolver(self, operation):
        linked_responses = []

        consumes = operation.consumes
        request = FlaskApi.get_request()

        if all_json(consumes):
            request_body = request.json
        elif consumes[0] in FORM_CONTENT_TYPES:
            request_body = {sanitized(k): v for k, v in request.form.items()}
        else:
            request_body = request.body

        try:
            query = request.query.to_dict(flat=False)
        except AttributeError:
            query = dict(request.query.items())

        content_type_header = request.headers.get('Content-Type')
        content_type_header = content_type_header or request.headers.get('Accept', '*/*')
        content_type_header = strip_charset(content_type_header)

        # first priority - Request body
        if request_body:
            try:
                operation_request_body = operation.request_body['content'][content_type_header]
                for item in operation_request_body.get('x-link-response'):
                    if dict(item.get('value')) ==  request_body:
                        linked_responses.append(item.get('x-response-id'))
            except KeyError:
                pass
        
        # second priority - Query params
        if query:
            query_params = filter(lambda x: x.get('in') == 'query', operation.parameters)
            for param in query_params:
                param_val = query.get(param.get('name'), None)
                if param_val is not None:
                    for item in param.get('x-link-response'):
                        if item.get('value') in  param_val:
                            linked_responses.append(item.get('x-response-id'))
        
        # third priority - Headers
        if content_type_header:
            header_params = filter(lambda x: x.get('in') == 'header', operation.parameters)
            for param in header_params:
                if param.get('name').lower() in ['accept', 'content-type']:
                    for item in param.get('x-link-response'):
                        if item.get('value') ==  content_type_header:
                            linked_responses.append(item.get('x-response-id'))

        return linked_responses

    def _fake(self, schema, example=None):
        # use faker to generate fake data from jsonschema
        example = example or schema.get('example')

        if 'oneOf' in schema:
            return self._fake(schema['oneOf'][random.randint(0, (len(schema['oneOf']) - 1))], example)
        
        if ('additionalProperties' in schema) or (schema == {}):
            return example or getattr(self.faker, 'pydict')()

        if schema["type"].lower() == "array":
            if isinstance(example, list) and  len(example):
                return [self._fake(schema["items"], example[i]) for i in range(len(example))]
            else:
                return [self._fake(schema["items"]) for i in range(2)]

        if schema["type"].lower() == "object":
            if example:
                return {k: self._fake(v, example.get(k)) for k, v in schema["properties"].items()}
            else:
                return {k: self._fake(v) for k, v in schema["properties"].items()}
            

        if "enum" in schema:
            # if enum, just choose one of enum items at random
            return random.choice(schema["enum"])

        if schema["type"].lower() == "string":
            if example:
                return str(example)
            return getattr(self.faker, schema.get("format", "word"))()

        if schema["type"].lower().startswith("int"):
            if example:
                return int(example)
            return int(example) or self.faker.random_int()

        return getattr(self.faker, schema.get("type", "word"))()

    def example_filter(self, schema, response_id):
        if 'examples' in schema:
            for name, example in schema['examples'].items():
                if example.get('x-response-id') == response_id:
                    return example.get('value')
        elif 'example' in schema:
            if schema['example'].get('x-response-id') == response_id:
                return schema['example'].get('value')
        return None

    def mock_operation(self, operation, *args, **kwargs):
        _schema = _example = None
        linked_responses = self.example_resolver(operation)

        if len(linked_responses):
            linked_response = linked_responses[random.randint(0, (len(linked_responses) - 1))]
            for code, response in operation.responses.items():
                for media_type, schema in response['content'].items():
                    _example = self.example_filter(schema, linked_response)
                    status_code = code
        
        if not _example:
            _example, status_code = operation.example_response()

        if not _example:
            status_code = sorted(operation._responses.keys())[0]
            _schema = operation.response_schema(status_code, operation.get_mimetype())

        status_code = int(status_code) or 200

        if _example:
            return _example, status_code
        
        #If there are no example,  we try to fake from schema
        return self._fake(_schema or {}), status_code