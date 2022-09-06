from restapi import KimaiAPI
from restapi.kimai import Activity

# .env File needed!


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
    assert isinstance(new_id, idef test_ping_pong() -> None:
nt)


    api = KimaiAPI()
    response = api.get_from_query("ping")
    assert response.json() == {"message": "pong"}
