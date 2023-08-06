import click

from src.transformation import cli
from click.testing import CliRunner

def test_good_json():
    runner = CliRunner()
    result = runner.invoke(cli, ['test/valid.json'])
    assert result.exit_code == 0

    transformed_file = open("test/transformed.json")
    transformed_text = transformed_file.read()
    assert result.output == transformed_text
    transformed_file.close()

def test_good_yaml():
    runner = CliRunner()
    result = runner.invoke(cli, ['test/valid.yaml'])
    assert result.exit_code == 0

    transformed_file = open("test/transformed.json")
    transformed_text = transformed_file.read()
    assert result.output == transformed_text
    transformed_file.close()

def test_bad_template():
    runner = CliRunner()
    result = runner.invoke(cli, ['test/invalid.json'])
    assert result.exit_code == 1

if __name__ == "__main__":
    test_good_json()
    click.echo("test_valid_json ... ok")
    test_good_yaml()
    click.echo("test_valid_yaml ... ok")
    test_bad_template()
    click.echo("test_invalid_json ... ok")