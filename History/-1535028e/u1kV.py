"""atoolbox testing package."""


import pathlib

import toml

import atoolbox

REPO_PATH = pathlib.Path(__file__).parents[1]


def test_version() -> None:
    """Check that all the version tags are in sync."""

    toml_path = REPO_PATH / "pyproject.toml"
    expected = toml.load(toml_path)["tool"]["poetry"]["version"]

    actual = atoolbox.__version__
    assert actual == expected
