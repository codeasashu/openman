import os
from typing import Sequence, Callable
import json
import pytest  # type: ignore


@pytest.fixture
def postman_file():
    return os.path.abspath("tests/fixtures/postman-echo.json")

@pytest.fixture
def mock_json():
    def get_json_from_file(filename):
        filepath = os.path.abspath(f"tests/fixtures/{filename}")
        with open(filepath) as f:
            content = json.load(f)
            return content
    return get_json_from_file


@pytest.fixture
def postman_json():
    filepath = os.path.abspath("tests/fixtures/postman-echo.json")
    with open(filepath) as f:
        content = json.load(f)
        return content


@pytest.fixture
def get_folder_fixture() -> Callable:
    def get_folder(fixture_json: Sequence[dict], folder_name: str):
        folders = list(filter(lambda x: x["name"] == folder_name, fixture_json))
        return folders[0] if len(folders) else None

    return get_folder
