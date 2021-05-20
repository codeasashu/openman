from openman.utils import is_folder


def test_is_folder(postman_json):
    collection = postman_json
    assert is_folder(collection["item"][0])

    folder_without_description = list(
        filter(
            lambda x: x["name"] == "Folder Without description",
            collection["item"],
        )
    )
    assert is_folder(folder_without_description[0])
