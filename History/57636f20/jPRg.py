import pytest

from restapi import KimaiAPI
from restapi.kimai import Activity


@pytest.fixture
def test_session() -> KimaiAPI:
    api = KimaiAPI()
    return api


def test_post_activity(api: KimaiAPI = test_session) -> None:
    data = {
        "name": "16.123456-Ticketname-Ticketbeschreibung",
        "comment": "Test",
        "project": 20,
        "budget": 28.78,
        "timeBudget": "08:00",
    }

    activity = Activity(**data)
    response = api.post_activity(activity)
    assert response.json() == []


def test_pingpong(api: KimaiAPI = test_session) -> None:
    response = api.get_from_query("ping")
    assert response.json() == {"message": "pong"}
