import unittest
import os, json
from openman.spec import Spec
from openman.parser import CollectionParser
from openman import from_collection


class TestOperation(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.fixture_path = os.path.abspath("tests/fixtures")
        self.collection_file = os.path.join(
            self.fixture_path, "postman-echo.json"
        )

    def test_info(self):
        collection = CollectionParser(from_collection(self.collection_file))
        spec = Spec(collection)
        self.assertEqual(
            dict(
                title="Postman Echo",
                description="Postman Echo is service you can use to test your REST clients and make sample API calls. It provides endpoints for `GET`, `POST`, `PUT`, various auth mechanisms and other utility endpoints.\n\nThe documentation for the endpoints as well as example responses can be found at [https://postman-echo.com](https://postman-echo.com/?source=echo-collection-app-onboarding)",
                version="1.0.0",
            ),
            spec.info,
        )
        self.assertEqual(
            dict(
                title="Postman Echo",
                description="Postman Echo is service you can use to test your REST clients and make sample API calls. It provides endpoints for `GET`, `POST`, `PUT`, various auth mechanisms and other utility endpoints.\n\nThe documentation for the endpoints as well as example responses can be found at [https://postman-echo.com](https://postman-echo.com/?source=echo-collection-app-onboarding)",
                version="1.0.0",
            ),
            spec.get_info(),
        )

    def test_openapi(self):
        collection = CollectionParser(from_collection(self.collection_file))
        spec = Spec(collection)
        self.assertEqual("3.0.0", spec.openapi)

    def test_servers(self):
        collection = CollectionParser(from_collection(self.collection_file))
        spec = Spec(collection)
        self.assertEqual(["http://localhost"], spec.servers)
        spec.add_servers(["http://abc", "http://def"])
        self.assertEqual(
            ["http://localhost", "http://abc", "http://def"], spec.servers
        )

        spec.add_servers("jhk")
        self.assertEqual(
            ["http://localhost", "http://abc", "http://def", "jhk"],
            spec.servers,
        )