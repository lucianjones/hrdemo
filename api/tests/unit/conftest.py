import pytest

from rest_framework.test import APIRequestFactory


@pytest.fixture(scope="function")
def factory() -> APIRequestFactory:
    """
    Fixture to provide an API client Factory
    :return: APIRequestFactory
    """
    yield APIRequestFactory()
