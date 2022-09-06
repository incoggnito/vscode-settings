import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any

from dataclasses import dataclass
from dotenv import load_dotenv
from requests.structures import CaseInsensitiveDict

from restapi.main import Requestor

LOGGER = logging.getLogger(__name__)


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
    begin: datetime = datetime(22, 8, 1, 0, 0)
    end: datetime = datetime(22, 8, 1, 23, 59)
    project: int = 0
    activity: int = 0
    description: str = ""
    fixedRate: int = 0
    hourlyRate: int = 0
    exported: bool = True
    billable: bool = True
    tags: str = ""


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

    def post_timesheet(self, timesheet: AnueTimesheet) -> Any:

        try:
            r = self.post_query("activities", timesheet.__dict__)
        except:
            LOGGER.error("Can't post activity!")

        return r.json()["id"]

    def get_activity_by_search(self, params:dict={}):
        try:
            r = self.get_from_query("activities", params)
