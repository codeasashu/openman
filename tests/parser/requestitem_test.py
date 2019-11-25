import unittest
import os
import openman
from openman.parser import RequestItemParser

class TestRequestItemParser(unittest.TestCase):
    def setUp(self):
        self.openman = openman
        self.fixture_path = os.path.abspath('tests/fixtures')
        self.collection_file = os.path.join(self.fixture_path, 'postman-echo.json')
    
    def test_parserequest_ctor(self):
        try:
            requestitem = RequestItemParser()
        except Exception as e:
            self.assertTrue(isinstance(e, openman.errors.RequestItemParserException))
        
        try:
            requestitem = RequestItemParser.parse()
        except Exception as e:
            self.assertTrue(isinstance(e, openman.errors.RequestItemParserException))
        
        try:
            requestitem = RequestItemParser([1,2])
        except Exception as e:
            self.assertTrue(isinstance(e, openman.errors.RequestItemParserException))
        
        # request should be a single valid postman request, not a collection
        collection = openman.from_collection(self.collection_file)
        try:
            requestitem = RequestItemParser(collection)
        except Exception as e:
            self.assertTrue(isinstance(e, openman.errors.RequestItemParserException))
    
    def test_summary(self):
        collection = openman.from_collection(self.collection_file)
        samplerequest = collection['item'][0]['item'][0]
        assert isinstance(samplerequest, dict)
        requestitem = RequestItemParser.parse(samplerequest)
        self.assertEqual('GET Request', requestitem.summary)
        self.assertEqual('GET Request', requestitem.get_summary())
    
    def test_description(self):
        collection = openman.from_collection(self.collection_file)
        samplerequest = collection['item'][0]['item'][0]
        assert isinstance(samplerequest, dict)
        requestitem = RequestItemParser.parse(samplerequest)
        self.assertEqual('The HTTP `GET` request method is meant to retrieve data from a server. The data\nis identified by a unique URI (Uniform Resource Identifier). \n\nA `GET` request can pass parameters to the server using \"Query String \nParameters\". For example, in the following request,\n\n> http://example.com/hi/there?hand=wave\n\nThe parameter \"hand\" has the value \"wave\".\n\nThis endpoint echoes the HTTP headers, request parameters and the complete\nURI requested.', requestitem.description)
        self.assertEqual('The HTTP `GET` request method is meant to retrieve data from a server. The data\nis identified by a unique URI (Uniform Resource Identifier). \n\nA `GET` request can pass parameters to the server using \"Query String \nParameters\". For example, in the following request,\n\n> http://example.com/hi/there?hand=wave\n\nThe parameter \"hand\" has the value \"wave\".\n\nThis endpoint echoes the HTTP headers, request parameters and the complete\nURI requested.', requestitem.get_description())
    
    def test_get_request(self):
        collection = openman.from_collection(self.collection_file)
        samplerequest = collection['item'][0]['item'][0]
        assert isinstance(samplerequest, dict)
        requestitem = RequestItemParser.parse(samplerequest)
        request = requestitem.get_request()
        self.assertEqual('get', request.method)
    
    def test_get_response(self):
        collection = openman.from_collection(self.collection_file)
        samplerequest = collection['item'][0]['item'][0]
        assert isinstance(samplerequest, dict)
        requestitem = RequestItemParser.parse(samplerequest)
        responses = requestitem.get_responses()
        self.assertIn(200, [response.code for response in responses])