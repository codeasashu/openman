import unittest
import os
import openman
from openman.parser import CollectionParser, RequestItemParser

class TestCollectionParser(unittest.TestCase):
    def setUp(self):
        self.openman = openman
        self.fixture_path = os.path.abspath('tests/fixtures')
        self.collection_file = os.path.join(self.fixture_path, 'postman-echo.json')
    
    def test_parsecollection_ctor(self):
        try:
            collection = CollectionParser()
        except Exception as e:
            self.assertTrue(isinstance(e, openman.errors.CollectionParserException))
        
        try:
            collection = CollectionParser.parse()
        except Exception as e:
            self.assertTrue(isinstance(e, openman.errors.CollectionParserException))
        
        try:
            collection = CollectionParser([1,2])
        except Exception as e:
            self.assertTrue(isinstance(e, openman.errors.CollectionParserException))
        
        # collection should be a valid postman collection
        postmancollection = openman.from_collection(self.collection_file)
        try:
            collection = CollectionParser(postmancollection)
        except Exception as e:
            self.assertTrue(isinstance(e, openman.errors.CollectionParserException))
    
    def test_version(self):
        postmancollection = openman.from_collection(self.collection_file)
        assert isinstance(postmancollection, dict)
        collection = CollectionParser.parse(postmancollection)
        self.assertEqual('v2.1.0', collection.version)
        self.assertEqual('v2.1.0', collection.get_version())
    
    def test_name(self):
        postmancollection = openman.from_collection(self.collection_file)
        assert isinstance(postmancollection, dict)
        collection = CollectionParser.parse(postmancollection)
        self.assertEqual('Postman Echo', collection.name)
        self.assertEqual('Postman Echo', collection.get_name())
    
    def test_description(self):
        postmancollection = openman.from_collection(self.collection_file)
        assert isinstance(postmancollection, dict)
        collection = CollectionParser.parse(postmancollection)
        self.assertEqual('Postman Echo is service you can use to test your REST clients and make sample API calls. It provides endpoints for `GET`, `POST`, `PUT`, various auth mechanisms and other utility endpoints.\n\nThe documentation for the endpoints as well as example responses can be found at [https://postman-echo.com](https://postman-echo.com/?source=echo-collection-app-onboarding)', collection.description)
        self.assertEqual('Postman Echo is service you can use to test your REST clients and make sample API calls. It provides endpoints for `GET`, `POST`, `PUT`, various auth mechanisms and other utility endpoints.\n\nThe documentation for the endpoints as well as example responses can be found at [https://postman-echo.com](https://postman-echo.com/?source=echo-collection-app-onboarding)', collection.get_description())

    def test_folders(self):
        postmancollection = openman.from_collection(self.collection_file)
        assert isinstance(postmancollection, dict)
        collection = CollectionParser.parse(postmancollection)
        folders = collection.get_folders()
        self.assertIn('Request Methods', [folder.summary for folder in folders])
    
    def test_requestitems(self):
        postmancollection = openman.from_collection(self.collection_file)
        assert isinstance(postmancollection, dict)
        collection = CollectionParser.parse(postmancollection)
        requestitems = collection.get_requestitems()
        self.assertIsInstance(requestitems[0], RequestItemParser)
        self.assertIn('PUT Request', [requestitem.summary for requestitem in requestitems])
        