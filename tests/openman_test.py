import unittest
import os
import openman

class TestOpenman(unittest.TestCase):
    def setUp(self):
        self.openman = openman
        self.fixture_path = os.path.abspath('tests/fixtures')
    
    def test_fromcollection(self):
        try:
            openman.from_collection()
        except Exception as e:
            self.assertTrue(isinstance(e, openman.errors.OpenmanException))
        try:
            openman.from_collection('non-existant-file')
        except Exception as e:
            self.assertTrue(isinstance(e, FileNotFoundError))
    
    def test_relative_abs_filenames(self):
        collection = openman.from_collection(
            os.path.join(self.fixture_path, 'postman-echo.json'))
        assert isinstance(collection, dict)