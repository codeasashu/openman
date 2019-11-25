import unittest
import os
import openman
from openman.parser import ResponseParser

class TestResponseParser(unittest.TestCase):
    def setUp(self):
        self.openman = openman
        self.fixture_path = os.path.abspath('tests/fixtures')
        self.collection_file = os.path.join(self.fixture_path, 'postman-echo.json')
    
    def test_parseresponse_ctor(self):
        try:
            response = ResponseParser()
        except Exception as e:
            self.assertTrue(isinstance(e, openman.errors.ResponseParserException))
        
        try:
            response = ResponseParser.parse()
        except Exception as e:
            self.assertTrue(isinstance(e, openman.errors.ResponseParserException))
        
        try:
            response = ResponseParser([1,2])
        except Exception as e:
            self.assertTrue(isinstance(e, openman.errors.ResponseParserException))
        
        # response should be a single valid postman response, not a collection
        collection = openman.from_collection(self.collection_file)
        try:
            response = ResponseParser(collection)
        except Exception as e:
            self.assertTrue(isinstance(e, openman.errors.ResponseParserException))

    def test_code(self):
        collection = openman.from_collection(self.collection_file)
        sampleresponse = collection['item'][0]['item'][0]['response'][0]
        assert isinstance(sampleresponse, dict)
        response = ResponseParser.parse(sampleresponse)
        self.assertEqual(200, response.code)
        self.assertEqual(200, response.get_code())
    
    def test_headers(self):
        collection = openman.from_collection(self.collection_file)
        sampleresponse = collection['item'][0]['item'][0]['response'][0]
        assert isinstance(sampleresponse, dict)
        response = ResponseParser.parse(sampleresponse)
        self.assertTrue(set({'Connection':'keep-alive'}).issubset(response.headers))
        self.assertEqual('keep-alive', response.get_headers('Connection'))
        self.assertTrue(
            set({'Content-Type': 'application/json; charset=utf-8'}).issubset(
                response.get_headers()
            ))
    
    def test_content_type(self):
        collection = openman.from_collection(self.collection_file)
        sampleresponse = collection['item'][0]['item'][0]['response'][0]
        assert isinstance(sampleresponse, dict)
        response = ResponseParser.parse(sampleresponse)
        self.assertEqual('application/json', response.content_type)
        self.assertEqual('application/json', response.get_content_type())
    
    def test_body(self):
        collection = openman.from_collection(self.collection_file)
        sampleresponse = collection['item'][0]['item'][0]['response'][0]
        assert isinstance(sampleresponse, dict)
        response = ResponseParser.parse(sampleresponse)
        response_body = response.get_body()
        self.assertEqual(['args', 'headers', 'url'], list(response.body.keys()))
        self.assertEqual(
            'https://postman-echo.com/get?foo1=bar1&foo2=bar2',
            response_body['url'])
        self.assertEqual({
                "foo1": "bar1",
                "foo2": "bar2"
            }, response_body['args'])
    
    def test_request(self):
        collection = openman.from_collection(self.collection_file)
        sampleresponse = collection['item'][0]['item'][0]['response'][0]
        assert isinstance(sampleresponse, dict)
        response = ResponseParser.parse(sampleresponse)
        example = response.example
        self.assertIsInstance(example, openman.parser.RequestParser)
        self.assertEqual('/get', example.get_path(True))
        self.assertEqual('get', example.method)