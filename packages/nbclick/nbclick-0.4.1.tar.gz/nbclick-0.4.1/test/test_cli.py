from click.testing import CliRunner
from nbclick.__main__ import main

import os
import pytest


def notebook_file(filename):
    return os.path.join(os.path.split(__file__)[0], "notebooks", filename)


def test_help():
    runner = CliRunner()

    # Test help message
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0


@pytest.mark.parametrize(
    "data",
    [
        ("integer.ipynb", ["--num_samples", "20"]),
        ("string.ipynb", ["--outfile", "blubb.txt"]),
        ("boolean.ipynb", ["--output"]),
        ("boolean.ipynb", ["--no-output"]),
        ("list.ipynb", ["--integers", "1", "2", "3"]),
        ("hetlist.ipynb", ["--mixed", "17", "wrong"]),
    ],
)
def test_datatypes(data):
    runner = CliRunner()
    notebook, params = data

    # Test help message works
    result = runner.invoke(main, [notebook_file(notebook), "--help"])
    assert result.exit_code == 0

    # Run with defaults
    result = runner.invoke(main, [notebook_file(notebook)])
    assert result.exit_code == 0

    # Run with modified input
    result = runner.invoke(main, [notebook_file(notebook)] + params)
    assert result.exit_code == 0


def test_noparams_notebook():
    runner = CliRunner()
    result = runner.invoke(main, [notebook_file("noparams.ipynb")])
    assert result.exit_code == 0
