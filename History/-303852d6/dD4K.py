
import asyncio
import logging
import datetime
import json
import pandas as pd
from atoolbox import FileHandler
from sqlalchemy import create_engine

from fyrsonic.utils.input_handler import (
    cautious_float_input,
    select_list_entry,
    yes_no,
)

from contextlib import AsyncExitStack, asynccontextmanager
from asyncio_mqtt import Client, MqttError

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def publish_machine_state(broker:str, topic: str, df: pd.DataFrame):
    # We 💛 context managers. Let's create a stack to help
    # us manage them.
    async with AsyncExitStack() as stack:
        # Keep track of the asyncio tasks that we create, so that
        # we can cancel them on exit
        tasks = set()
        stack.push_async_callback(cancel_tasks, tasks)

        # Connect to the MQTT broker
        client = Client(broker)
        await stack.enter_async_context(client)

        task = asyncio.create_task(mqtt_publish_data(topic, client, df))
        tasks.add(task)

        # Wait for everything to complete (or fail due to, e.g., network
        # errors)
        await asyncio.gather(*tasks)

async def mqtt_publish_data(name, client, df):
    json_object = {} 
    json_object["data"] = df.loc[0].to_json()
    await client.publish(name, json.dumps(json_object))