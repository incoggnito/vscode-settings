import pytest

from restapi import KimaiAPI
from restapi.kimai import Activity


@pytest.fixture
def test_session() -> KimaiAPI:
    return KimaiAPI()


def test_post_activity(api: KimaiAPI = test_session) -> None:
    activity = Activity(
        name="test",
    )
    response = api.post_activity("ping")
    assert 



def test_pingpong(api: KimaiAPI = test_session) -> None:
    response = api.get_from_query("ping")
    assert response.json() == {"message": "pong"}
