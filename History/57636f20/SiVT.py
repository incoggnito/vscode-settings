from restapi import KimaiAPI
from restapi.kimai import Activity, Timesheet

SAMPLE_ACTIVITY = {
    "name": "16.123456-Ticketname-Ticketbeschreibung",
    "comment": "Test",
    "project": 20,
    "budget": 28.78,
    "timeBudget": "08:00",
}

SAMPLE_TIMESHEET = {
    "begin": "2022-08-13T08:56:30",
    "end": "2022-08-13T08:56:30",
    "project": 0,
    "activity": 0,
    "description": "string",
    "fixedRate": 0,
    "hourlyRate": 0,
    "user": 0,
    "exported": True,
    "billable": True,
    "tags": "string",
}


def test_post_activity() -> None:

    api = KimaiAPI()
    activity = Activity(**SAMPLE_ACTIVITY)
    new_id = api.post_activity(activity)
    assert isinstance(new_id, int)


def test_post_timesheet() -> None:
    api = KimaiAPI()
    ts = Timesheet(**SAMPLE_TIMESHEET)
    new_id = api.post_timesheet(ts)
    assert isinstance(new_id, int)


def test_pingpong() -> None:
    api = KimaiAPI()
    response = api.get_from_query("ping")
    assert response.json() == {"message": "pong"}
