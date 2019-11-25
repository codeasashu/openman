import unittest
import os
import openman
from openman.parser import RequestParser

class TestRequestParser(unittest.TestCase):
    def setUp(self):
        self.openman = openman
        self.fixture_path = os.path.abspath('tests/fixtures')
        self.collection_file = os.path.join(self.fixture_path, 'postman-echo.json')
    
    def test_parserequest_ctor(self):
        try:
            requests = RequestParser()
        except Exception as e:
            self.assertTrue(isinstance(e, openman.errors.RequestParserException))
        
        try:
            requests = RequestParser.parse()
        except Exception as e:
            self.assertTrue(isinstance(e, openman.errors.RequestParserException))
        
        try:
            requests = RequestParser([1,2])
        except Exception as e:
            self.assertTrue(isinstance(e, openman.errors.RequestParserException))
        
        # request should be a single valid postman request, not a collection
        collection = openman.from_collection(self.collection_file)
        try:
            requests = RequestParser(collection)
        except Exception as e:
            self.assertTrue(isinstance(e, openman.errors.RequestParserException))

    def test_path(self):
        collection = openman.from_collection(self.collection_file)
        samplerequest = collection['item'][0]['item'][0]['request'] # Request Methods
        assert isinstance(samplerequest, dict)
        request = RequestParser.parse(samplerequest)
        self.assertEqual('/get', request.path)
        self.assertEqual('/get', request.get_path(True))
        self.assertEqual(['get'], request.get_path())

    def test_method(self):
        collection = openman.from_collection(self.collection_file)
        samplerequest = collection['item'][0]['item'][0]['request']
        assert isinstance(samplerequest, dict)
        request = RequestParser.parse(samplerequest)
        self.assertEqual('get', request.method)
        self.assertEqual('get', request.get_method())
    
    def test_query_string(self):
        collection = openman.from_collection(self.collection_file)
        samplerequest = collection['item'][0]['item'][0]['request']
        assert isinstance(samplerequest, dict)
        request = RequestParser.parse(samplerequest)
        self.assertEqual({'foo1': 'bar1', 'foo2': 'bar2'}, request.query_string)
        self.assertEqual({'foo1': 'bar1', 'foo2': 'bar2'}, request.get_query_string())
        # Disabled query string ignores item
        samplerequest['url']['query'][0]['disabled'] = True
        request = RequestParser.parse(samplerequest)
        self.assertEqual({'foo2': 'bar2'}, request.query_string)
        self.assertEqual({'foo2': 'bar2'}, request.get_query_string())
        # Non disabled query string includes item
        samplerequest['url']['query'][0]['disabled'] = False
        request = RequestParser.parse(samplerequest)
        self.assertEqual({'foo1': 'bar1', 'foo2': 'bar2'}, request.query_string)
        self.assertEqual({'foo1': 'bar1', 'foo2': 'bar2'}, request.get_query_string())
    
    def test_headers(self):
        collection = openman.from_collection(self.collection_file)
        samplerequest = collection['item'][1]['item'][0]['request']
        assert isinstance(samplerequest, dict)
        request = RequestParser.parse(samplerequest)
        self.assertEqual({'my-sample-header': 'Lorem ipsum dolor sit amet'}, request.headers)
        self.assertEqual({'my-sample-header': 'Lorem ipsum dolor sit amet'}, request.get_headers())
        self.assertEqual('Lorem ipsum dolor sit amet', request.get_headers('my-sample-header'))
        self.assertIsNone(request.get_headers('NonExistant'))

    def test_body(self):
        collection = openman.from_collection(self.collection_file)
        samplerequest = collection['item'][0]['item'][2]['request']
        assert isinstance(samplerequest, dict)
        request = RequestParser.parse(samplerequest)
        self.assertEqual({'foo1': 'bar1', 'foo2': 'bar2'}, request.body)
        self.assertEqual({'foo1': 'bar1', 'foo2': 'bar2'}, request.get_body())

        samplerequest = collection['item'][0]['item'][1]['request']
        request = RequestParser.parse(samplerequest)
        self.assertEqual(
            'This is expected to be sent back as part of response body.',
            request.body)
        self.assertEqual(
            'This is expected to be sent back as part of response body.',
            request.get_body())
    
    def test_body_contenttype(self):
        collection = openman.from_collection(self.collection_file)
        samplerequest = collection['item'][0]['item'][2]['request']
        assert isinstance(samplerequest, dict)
        request = RequestParser.parse(samplerequest)
        self.assertEqual('application/x-www-form-urlencoded', request.body_contenttype)
        self.assertEqual('application/x-www-form-urlencoded', request.get_body_contenttype())

        samplerequest = collection['item'][0]['item'][1]['request']
        request = RequestParser.parse(samplerequest)
        self.assertEqual('*/*', request.body_contenttype)
        self.assertEqual('*/*', request.get_body_contenttype())