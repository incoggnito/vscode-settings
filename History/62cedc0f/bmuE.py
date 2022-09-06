import logging
from datetime import date, datetime, time, timedelta
from typing import Union

import caldav
import pandas as pd
import pytz

from icalendar import Event

LOGGER = logging.getLogger(__file__)


def string2date_tz(
    data: pd.DataFrame, timeformat: str = "%m/%d/%Y %H:%M", tz: str = "Europe/Berlin"
) -> pd.DataFrame:
    mytimezone = pytz.timezone(tz)
    data.startdate = pd.to_datetime(data.startdate, utc=True)
    data.enddate = pd.to_datetime(data.enddate, utc=True)
    data.startdate = pd.to_datetime(
        data.startdate.dt.tz_convert(mytimezone), format=timeformat
    )
    data.enddate = pd.to_datetime(
        data.enddate.dt.tz_convert(mytimezone), format=timeformat
    )
    return data


class MyCalendar:
    """Connect to a caldav calendar"""

    def __init__(self, url: str):
        self.url = url.lower()

    def connect_server(self, user: str, password: str) -> None:
        """Connect to an caldav server, get logged-in principal and all calendars"""
        self.client = caldav.DAVClient(self.url, username=user, password=password)
        self.principal = self.client.principal()
        self.calendars = self.principal.calendars()

    def get_calendar(self, name: str = "") -> None:
        """Select a specific calendar"""
        if name:
            self.calendar = [cal for cal in self.calendars if f"{name}/" in str(cal)][0]
        else:
            if len(self.calendars) > 0:
                self.calendar = self.calendars[0]

    def create_event(self, start: datetime, end: datetime, summary: str) -> None:
        start = start.to_pydatetime()
        end = end.to_pydatetime()
        e = Event()
        e.add("summary", summary)
        e.add("dtstart", start)
        e.add("dtend", end)
        self.calendar.save_event(e)

    def get_events_in_timerange(
        self,
        start: datetime = datetime(2021, 1, 1),
        end: datetime = datetime(2024, 1, 1),
    ) -> None:
        """Get all events in a time range

        Args:
            startdate (datetime, optional): Start date. Defaults to datetime(2021, 1, 1).
            enddate (datetime, optional): End date. Defaults to datetime(2024, 1, 1).
        """ "Get all events between two dates"
        self.events = self.calendar.date_search(start, end, expand=True)

    def get_events(self) -> None:
        """Get all events from a certain calendar"""
        self.events = self.calendar.events()

    @staticmethod
    def _format_datetime(dt: Union[datetime, date], add_time: time) -> datetime:
        try:
            if str(type(dt)) == "<class 'datetime.date'>":
                if add_time == time(22, 59):
                    dt = datetime.combine(
                        dt - timedelta(days=1), add_time, pytz.timezone("UTC")
                    )
                else:
                    dt = datetime.combine(dt, add_time, pytz.timezone("UTC"))

            if not dt.tzname():
                dt = dt.astimezone(pytz.timezone("UTC"))
        except:
            LOGGER.error("Time {dt} occurs errors")

        return dt

    def get_data_from_events(self) -> pd.DataFrame:
        """Select data from calender events

        Returns:
            pd.DataFrame: Return a table of events
        """
        data: dict = {"summary": [], "startdate": [], "enddate": []}
        for eventraw in self.events:
            try:
                e = eventraw.instance.vevent
                eventraw.load()
                data["summary"].append(e.summary.value)
                data["startdate"].append(
                    self._format_datetime(e.dtstart.value, time(0, 0))
                )
                data["enddate"].append(
                    self._format_datetime(e.dtend.value, time(22, 59))
                )
            except:
                LOGGER.error(f"The calendar event is not readable: {e}")
                continue

        return self._format_data(pd.DataFrame(data))

    @staticmethod
    def _format_data(data: pd.DataFrame) -> pd.DataFrame:
        data = string2date_tz(data)
        data["duration"] = (data.enddate - data.startdate).astype("timedelta64[m]") / 60
        data.sort_values(by="startdate", inplace=True)
        data = data.reset_index(drop=True)
        data.index = [i for i in range(len(data))]
        return data

if __name__
    base_url = f"https://cloud.amitronics.net/remote.php/dav/calendars/{args[0]}/{cal_name}/"
    username = s.name
    decrypt_password(s.hashed_password)

    cal = MyCalendar(base_url)
    cal.connect_server(args[0], args[1])
    idx_tags = {k.lower(): v for k, v in args[2].items()}
    cal.get_calendar(cal_name.lower())
    last_month_day = get_last_month_day(year, month)
    cal.get_events_in_timerange(
        datetime(year, month, 1, 0, 0),
        datetime(year, month, last_month_day, 23, 59),
    )
    df = cal.get_data_from_events()
