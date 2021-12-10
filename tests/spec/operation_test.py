import unittest
import os
import uuid
from unittest.mock import patch
from unittest import TestCase
from openman.spec import Operation
from openman.parser import RequestItemParser
from openman import from_collection


def test_operationid(get_folder_fixture, postman_json):
    folder = get_folder_fixture(postman_json["item"], "Request Methods")
    samplerequestitem = folder["item"][0]
    assert isinstance(samplerequestitem, dict)
    request_item = RequestItemParser(samplerequestitem)

    operation_id = Operation(request_item).id()
    assert "GetGet" == operation_id


@patch.object(uuid, attribute="uuid4", side_effect=["b"])
def test_requestbody(uuid, get_folder_fixture, postman_json):
    folder = get_folder_fixture(postman_json["item"], "Request Methods")
    samplerequestitem = folder["item"][2]
    assert isinstance(samplerequestitem, dict)
    request_item = RequestItemParser(samplerequestitem)
    requestbody_spec = Operation(request_item).request_body()
    TestCase().assertEqual(
        {
            "content": {
                "*/*": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "foo1": {"type": "string"},
                            "foo2": {"type": "string"},
                        },
                        "required": ["foo1", "foo2"],
                    },
                    "example": {"value": {"foo1": "bar1", "foo2": "bar2"}},
                    "x-link-response": [],
                }
            }
        },
        requestbody_spec,
    )


@patch.object(uuid, attribute="uuid4", side_effect=["a"])
def test_parameters(uuid, get_folder_fixture, postman_json):
    folder = get_folder_fixture(postman_json["item"], "Request Methods")
    samplerequestitem = folder["item"][0]
    assert isinstance(samplerequestitem, dict)
    request_item = RequestItemParser(samplerequestitem)
    param_spec = Operation(request_item).parameters()
    TestCase().assertEqual(
        [
            {
                "in": "query",
                "name": "foo1",
                "schema": {"type": "string", "example": "bar1"},
                "x-link-response": [{"value": "bar1", "x-response-id": "a"}],
            },
            {
                "in": "query",
                "name": "foo2",
                "schema": {"type": "string", "example": "bar2"},
                "x-link-response": [{"value": "bar2", "x-response-id": "a"}],
            },
        ],
        param_spec,
    )


@patch.object(uuid, attribute="uuid4", side_effect=["a"])
def test_responses(uuid, get_folder_fixture, postman_json):
    folder = get_folder_fixture(postman_json["item"], "Request Methods")
    samplerequestitem = folder["item"][0]
    assert isinstance(samplerequestitem, dict)
    request_item = RequestItemParser(samplerequestitem)

    response_spec = Operation(request_item).responses()
    TestCase().assertEqual(
        {
            200: {
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "object",
                            "properties": {
                                "args": {
                                    "type": "object",
                                    "properties": {
                                        "foo1": {"type": "string"},
                                        "foo2": {"type": "string"},
                                    },
                                    "required": ["foo1", "foo2"],
                                },
                                "headers": {
                                    "type": "object",
                                    "properties": {
                                        "x-forwarded-proto": {"type": "string"},
                                        "host": {"type": "string"},
                                        "accept": {"type": "string"},
                                        "accept-encoding": {"type": "string"},
                                        "cache-control": {"type": "string"},
                                        "postman-token": {"type": "string"},
                                        "user-agent": {"type": "string"},
                                        "x-forwarded-port": {"type": "string"},
                                    },
                                    "required": [
                                        "x-forwarded-proto",
                                        "host",
                                        "accept",
                                        "accept-encoding",
                                        "cache-control",
                                        "postman-token",
                                        "user-agent",
                                        "x-forwarded-port",
                                    ],
                                },
                                "url": {"type": "string"},
                            },
                            "required": ["args", "headers", "url"],
                            "title": "GET Request Woops",
                        },
                        "examples": {
                            "GetRequestWoops": {
                                "value": {
                                    "args": {
                                        "foo1": "bar1",
                                        "foo2": "bar2",
                                    },
                                    "headers": {
                                        "x-forwarded-proto": "https",
                                        "host": "postman-echo.com",
                                        "accept": "*/*",
                                        "accept-encoding": "gzip, deflate",
                                        "cache-control": "no-cache",
                                        "postman-token": "5c27cd7d-6b16-4e5a-a0ef-191c9a3a275f",
                                        "user-agent": "PostmanRuntime/7.6.1",
                                        "x-forwarded-port": "443",
                                    },
                                    "url": "https://postman-echo.com/get?foo1=bar1&foo2=bar2",
                                },
                                "x-response-id": "a",
                            }
                        },
                    }
                },
                "description": "GET Request Woops",
            }
        },
        response_spec,
    )


@patch.object(uuid, attribute="uuid4", return_value="a")
def test_multiple_responses(uuid, mock_json):
    multi_response_json = mock_json("multi-response.json")
    assert isinstance(multi_response_json, dict)
    request_item = RequestItemParser(multi_response_json["item"][0])

    response_spec = Operation(request_item).responses()
    assert [200, 400] == list(response_spec.keys())
    assert ["*/*"] == list(response_spec[200]["content"].keys())
    assert ["*/*"] == list(response_spec[400]["content"].keys())
    assert ["oneOf"] == list(
        response_spec[400]["content"]["*/*"]["schema"].keys()
    )
    assert {
        "title": "Setup user | Invalid Token",
        "type": "object",
        "properties": {
            "message": {"type": "string"},
            "status": {"type": "string"},
        },
        "required": ["status", "message"],
    } == response_spec[400]["content"]["*/*"]["schema"]["oneOf"][0]
    assert {
        "title": "Setup user | User Blacklisted",
        "type": "object",
        "properties": {
            "message": {"type": "string"},
            "status": {"type": "string"},
            "is_black_listed": {"type": "boolean", "format": "null"},
        },
        "required": ["status", "message", "is_black_listed"],
    } == response_spec[400]["content"]["*/*"]["schema"]["oneOf"][1]
    assert {
        "title": "Setup user | Request Failed",
        "type": "object",
        "properties": {
            "message": {"type": "string"},
            "status": {"type": "string"},
        },
        "required": ["status", "message"],
    } == response_spec[400]["content"]["*/*"]["schema"]["oneOf"][2]
