import json
import logging
from typing import Dict


LOGGER = logging.getLogger(__file__)


def mqtt_publish_data(name, client, data: Dict):
    client.publish(name, json.dumps(data))
