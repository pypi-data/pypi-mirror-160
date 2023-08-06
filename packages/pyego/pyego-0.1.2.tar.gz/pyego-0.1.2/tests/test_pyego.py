import pyego as ego
import pytest


def test_cli(capsys):
    ego.cli.execute()
    stdout, stderr = capsys.readouterr()
    assert stdout == "Hello World! from an API endpoint.\n"
