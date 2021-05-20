import json
from click.testing import CliRunner
import pytest  # type: ignore
from openman import cli


def test_input_file_required():
    runner = CliRunner()
    result = runner.invoke(cli.convert)
    assert result.exit_code == 2
    assert "Error: Missing argument 'POSTMANFILE'" in result.output


def test_convert(postman_file):
    runner = CliRunner()
    result = runner.invoke(cli.convert, f"{postman_file}")
    assert result.exit_code == 0
    assert "/digest-auth" in result.output


def test_convert_output_file(postman_file, tmp_path):
    output_filepath = tmp_path / "abc.txt"
    runner = CliRunner()
    result = runner.invoke(cli.convert, f"{postman_file} {output_filepath}")
    assert result.exit_code == 0
    assert "Schema converted successfully to" in result.output
    assert "/digest-auth" in output_filepath.read_text()


def test_convert_to_json(postman_file):
    runner = CliRunner()
    result = runner.invoke(cli.convert, f"-f json {postman_file}")
    assert result.exit_code == 0
    assert "/digest-auth" in result.output
    try:
        json_loadable = json.loads(result.output)
        assert "/digest-auth" in json_loadable["paths"].keys()
    except json.JSONDecodeError:
        pytest.fail("Output should be in json")
