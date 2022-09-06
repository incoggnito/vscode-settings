"""bigtoolbox testing package."""


import pathlib  # noqa: E402

import toml  # noqa: E402

import vallendb as master  # noqa: E402

REPO_PATH = pathlib.Path(__file__).parents[1]


def test_version() -> None:
    """Check that all the version tags are in sync."""

    toml_path = REPO_PATH / "pyproject.toml"
    expected = toml.load(toml_path)["tool"]["poetry"]["version"]

    actual = master.__version__
    assert actual == expected
