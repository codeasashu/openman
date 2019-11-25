import unittest
import os
import uuid
from unittest.mock import patch
from openman.spec import Operation
from openman.parser import RequestItemParser
from openman import from_collection

class TestOperation(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.fixture_path = os.path.abspath('tests/fixtures')
        self.collection_file = os.path.join(self.fixture_path, 'postman-echo.json')
    
    def test_operationid(self):
        collection = from_collection(self.collection_file)
        samplerequestitem = collection['item'][0]['item'][0]
        assert isinstance(samplerequestitem, dict)
        request_item = RequestItemParser(samplerequestitem)

        operation_id = Operation(request_item).id()
        self.assertEqual(
            'GetGet',
            operation_id
        )

    @patch.object(uuid, attribute='uuid4', side_effect=['a'])
    def test_responses(self, *args, **kwargs):
        collection = from_collection(self.collection_file)
        samplerequestitem = collection['item'][0]['item'][0]
        assert isinstance(samplerequestitem, dict)
        request_item = RequestItemParser(samplerequestitem)

        response_spec = Operation(request_item).responses()
        self.assertEqual(
            {200: {'content': {'application/json': {'schema': {'type': 'object', 'properties': {'args': {'type': 'object', 'properties': {'foo1': {'type': 'string'}, 'foo2': {'type': 'string'}}, 'required': ['foo1', 'foo2']}, 'headers': {'type': 'object', 'properties': {'x-forwarded-proto': {'type': 'string'}, 'host': {'type': 'string'}, 'accept': {'type': 'string'}, 'accept-encoding': {'type': 'string'}, 'cache-control': {'type': 'string'}, 'postman-token': {'type': 'string'}, 'user-agent': {'type': 'string'}, 'x-forwarded-port': {'type': 'string'}}, 'required': ['x-forwarded-proto', 'host', 'accept', 'accept-encoding', 'cache-control', 'postman-token', 'user-agent', 'x-forwarded-port']}, 'url': {'type': 'string'}}, 'required': ['args', 'headers', 'url']}, 'examples': {'GetRequestWoops': {'value': {'args': {'foo1': 'bar1', 'foo2': 'bar2'}, 'headers': {'x-forwarded-proto': 'https', 'host': 'postman-echo.com', 'accept': '*/*', 'accept-encoding': 'gzip, deflate', 'cache-control': 'no-cache', 'postman-token': '5c27cd7d-6b16-4e5a-a0ef-191c9a3a275f', 'user-agent': 'PostmanRuntime/7.6.1', 'x-forwarded-port': '443'}, 'url': 'https://postman-echo.com/get?foo1=bar1&foo2=bar2'}, 'x-response-id': 'a'}}}}, 'description': 'GET Request Woops'}},
            response_spec
        )
    
    @patch.object(uuid, attribute='uuid4', side_effect=['a'])
    def test_parameters(self, *args, **kwargs):
        collection = from_collection(self.collection_file)
        samplerequestitem = collection['item'][0]['item'][0]
        assert isinstance(samplerequestitem, dict)
        request_item = RequestItemParser(samplerequestitem)
        param_spec = Operation(request_item).parameters()
        self.assertEqual(
            [{'in': 'query', 'name': 'foo1', 'schema': {'type': 'string', 'example': 'bar1'}, 'x-link-response': [{'value': 'bar1', 'x-response-id': 'a'}]}, {'in': 'query', 'name': 'foo2', 'schema': {'type': 'string', 'example': 'bar2'}, 'x-link-response': [{'value': 'bar2', 'x-response-id': 'a'}]}],
            param_spec
        )
    
    @patch.object(uuid, attribute='uuid4', side_effect=['b'])
    def test_requestbody(self, *args, **kwargs):
        collection = from_collection(self.collection_file)
        samplerequestitem = collection['item'][0]['item'][2]
        assert isinstance(samplerequestitem, dict)
        request_item = RequestItemParser(samplerequestitem)
        requestbody_spec = Operation(request_item).request_body()
        self.assertEqual(
            {'content': {'*/*': {'schema': {'type': 'object', 'properties': {'foo1': {'type': 'string'}, 'foo2': {'type': 'string'}}, 'required': ['foo1', 'foo2']}, 'example': {'value': {'foo1': 'bar1', 'foo2': 'bar2'}}, 'x-link-response': []}}},
            requestbody_spec
        )
