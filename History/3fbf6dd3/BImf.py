import logging
import os
from datetime import datetime, date
from pathlib import Path
from typing import Any, Union

from dataclasses import dataclass
from dotenv import load_dotenv
from requests.structures import CaseInsensitiveDict

from restapi.main import Requestor

LOGGER = logging.getLogger(__name__)

KIMAI_PRJ_ACT_ID = {"G": [55, 315], "W": [22, 317], "K": [21, 62], "U": [8, 160], "S": [24, 316], "E": [25, 319]}


@dataclass
class Activity:
    """Creates a new activity"""

    name: str
    comment: str
    project: int
    budget: float
    timeBudget: str
    visible: bool = True
    billable: bool = True
    invoiceText: str = ""


@dataclass
class Timesheet:
    """Creates a new Timesheet"""

    user: int = 0
    begin: Union[date, datetime, str] = datetime(22, 8, 1, 0, 0)
    end: Union[date, datetime, str] = datetime(22, 8, 1, 23, 59)
    project: int = 0
    activity: int = 0
    description: str = ""
    fixedRate: int = 0
    hourlyRate: int = 0
    exported: bool = True
    billable: bool = True
    tags: str = ""

    def __post_init__(self):
        super().__init__(self.side, self.side)

    @staticmethod
    def _checkdate():
        if isinstance(date, datetime):
            date


@dataclass
class AnueTimesheet(Timesheet):
    project: int = 473
    activity: int = 297


class KimaiAPI(Requestor):
    """A special class for the Kimai API.

    Raises:
        EnvironmentError: Whenever a .env file is missing.

    """

    headers = {
        "accept": "text/plain",
        "Content-Type": "application/json",
    }
    url = "https://kimai.amitronics.net/api/"

    def __init__(self) -> None:

        super().__init__(url=self.url)
        self.s.headers = CaseInsensitiveDict(self.headers)
        self._login()

    def _load_dotenv(self, required_env_vars: list = ["X-AUTH-USER", "X-AUTH-TOKEN"]) -> dict:

        if all(os.getenv(env_var) for env_var in required_env_vars):
            LOGGER.info("Load environment variables from bash!")
        else:
            env_path = Path(".") / ".env"
            load_dotenv(dotenv_path=env_path)
            if all(os.getenv(env_var) for env_var in required_env_vars):
                result = {env_var: os.environ[env_var] for env_var in required_env_vars}
            else:
                LOGGER.error("Can't find the env variables!")
                raise EnvironmentError
        return result

    def _login(self) -> None:
        credentials = self._load_dotenv()
        self.s.headers.update(credentials)

    def post_activity(self, activity: Activity) -> Any:
        try:
            r = self.post_query("activities", activity.__dict__)
        except:
            LOGGER.error("Can't post activity!")

        return r.json()["id"]

    def post_timesheet(self, timesheet: Timesheet) -> Any:

        try:
            r = self.post_query("timesheets", timesheet.__dict__)
        except:
            LOGGER.error("Can't post activity!")

        return r.json()["id"]
