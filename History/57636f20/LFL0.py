from restapi import KimaiAPI
from restapi.kimai import Activity


def test_post_activity() -> None:
    data = {
        "name": "16.123456-Ticketname-Ticketbeschreibung",
        "comment": "Test",
        "project": 20,
        "budget": 28.78,
        "timeBudget": "08:00",
    }
    api = KimaiAPI()
    activity = Activity(**data)
    new_id = api.post_activity(activity)
    assert isinstance(new_id, int)


def test_post_timesheet() -> None:
    data = {
        "name": "16.123456-Ticketname-Ticketbeschreibung",
        "comment": "Test",
        "project": 20,
        "budget": 28.78,
        "timeBudget": "08:00",
    }


def test_pingpong() -> None:
    api = KimaiAPI()
    response = api.get_from_query("ping")
    assert response.json() == {"message": "pong"}
