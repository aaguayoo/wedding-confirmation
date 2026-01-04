"""Fixtures for testing."""

import pytest


@pytest.fixture(scope="session")
def dummy_fixture(request: object) -> None:
    """Docstring.

    Args:
        requset (object):
            Pytest request.

    """
    pass
