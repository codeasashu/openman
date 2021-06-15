import unittest
import os
import openman
from openman.parser import FolderParser


def test_folder_nested_request(mock_json):
    nested_folder_json = mock_json("nested_folder.json")
    print("a", nested_folder_json)
    folder = FolderParser(nested_folder_json)
    items = folder.get_requestitems()
    assert len(items) == 2


class TestFolderParser(unittest.TestCase):
    def setUp(self):
        self.openman = openman
        self.fixture_path = os.path.abspath('tests/fixtures')
        self.collection_file = os.path.join(self.fixture_path, 'postman-echo.json')
    
    def test_parsefolder_ctor(self):
        try:
            folder = FolderParser()
        except Exception as e:
            self.assertTrue(isinstance(e, openman.errors.FolderParserException))
        
        try:
            folder = FolderParser.parse()
        except Exception as e:
            self.assertTrue(isinstance(e, openman.errors.FolderParserException))
        
        try:
            folder = FolderParser([1,2])
        except Exception as e:
            self.assertTrue(isinstance(e, openman.errors.FolderParserException))
        
        # folder should be a valid postman folder and not a collection
        postmancollection = openman.from_collection(self.collection_file)
        try:
            folder = FolderParser(postmancollection)
        except Exception as e:
            self.assertTrue(isinstance(e, openman.errors.FolderParserException))
    
    def test_name(self):
        postmancollection = openman.from_collection(self.collection_file)
        samplefolder = postmancollection['item'][0]
        assert isinstance(samplefolder, dict)
        folder = FolderParser.parse(samplefolder)
        self.assertEqual('Request Methods', folder.summary)
        self.assertEqual('Request Methods', folder.get_summary())
    
    def test_description(self):
        postmancollection = openman.from_collection(self.collection_file)
        samplefolder = postmancollection['item'][0]
        assert isinstance(samplefolder, dict)
        folder = FolderParser.parse(samplefolder)
        self.assertEqual('HTTP has multiple request \"verbs\", such as `GET`, `PUT`, `POST`, `DELETE`,\n`PATCH`, `HEAD`, etc. \n\nAn HTTP Method (verb) defines how a request should be interpreted by a server. \nThe endpoints in this section demonstrate various HTTP Verbs. Postman supports \nall the HTTP Verbs, including some rarely used ones, such as `PROPFIND`, `UNLINK`, \netc.\n\nFor details about HTTP Verbs, refer to [RFC 2616](http://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html#sec9)\n', folder.description)
        self.assertEqual('HTTP has multiple request \"verbs\", such as `GET`, `PUT`, `POST`, `DELETE`,\n`PATCH`, `HEAD`, etc. \n\nAn HTTP Method (verb) defines how a request should be interpreted by a server. \nThe endpoints in this section demonstrate various HTTP Verbs. Postman supports \nall the HTTP Verbs, including some rarely used ones, such as `PROPFIND`, `UNLINK`, \netc.\n\nFor details about HTTP Verbs, refer to [RFC 2616](http://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html#sec9)\n', folder.get_description())
    
    def test_requests(self):
        postmancollection = openman.from_collection(self.collection_file)
        samplefolder = postmancollection['item'][0]
        assert isinstance(samplefolder, dict)
        folder = FolderParser.parse(samplefolder)
        requests =  folder.get_requestitems()
        self.assertTrue(set([
            'GET Request',
            'POST Raw Text'
        ]).issubset(set([request.summary for request in requests])))
        self.assertEqual(set(['get', 'post', 'put', 'delete', 'patch']),
        set([request.get_request().method for request in requests]))

