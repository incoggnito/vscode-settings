import asyncio
import json
import logging
from contextlib import AsyncExitStack
from typing import Dict

import paho.mqtt.client as paho
import pandas as pd

LOGGER = logging.getLogger(__file__)
logging.basicConfig(level=logging.INFO)


def mqtt_publish_data(name, client, data: Dict):
    # json_object = {}
    # for _, row in df.iterrows():
    #     json_object = row.to_json()
    client.publish(name, json.dumps(data))


# async def cancel_tasks(tasks):
#     for task in tasks:
#         if task.done():
#             continue
#         try:
#             task.cancel()
#             await task
#         except asyncio.CancelledError:
#             pass
