import json
import logging
import sys

import requests

LOGGER = logging.getLogger(__name__)


class Requestor:
    """Creates a request session and some helper functions"""

    def __init__(self, url: str = ""):

        self.url = url
        self.s = requests.Session()

    def get_from_query(self, endpoint: str, params: dict = {}) -> requests.models.Response:
        """Return the response of a get method"""

        request_response = self.s.get(f"{self.url}{endpoint}", params=params)
        return request_response

    def post_query(self, endpoint: str, data_dict: dict) -> requests.models.Response:
        """Post data to the query"""

        data = json.dumps(data_dict)

        request_response = self.s.post(
            f"{self.url}{endpoint}",
            data=data,
        )

        if request_response.status_code == 200:
            LOGGER.info("Successful post!")
        else:
            LOGGER.error(request_response.text)

        return request_response

    def delete_id(self, endpoint: str, id: int):

        request_response = self.s.delete(f"{self.url}{endpoint}/{id}")

        if request_response.status_code == 200:
            LOGGER.info("Successful post!")
        else:
            LOGGER.error(request_response.text)

        return request_response
