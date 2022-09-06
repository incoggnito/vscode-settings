
import asyncio
import json
import pandas as pd


from contextlib import AsyncExitStack, asynccontextmanager
from asyncio_mqtt import Client

from fyrsonic.utils.input_handler import select_list_entry, cautious_float_input, cautious_integer_input


BROKER = "192.168.102.109"
PORT = 1883

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def publish_dataframe(broker:str, topic: str, df: pd.DataFrame):
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
    for _, row in df.iterrows():
        json_object["data"] = row.to_json()
    await client.publish(name, json.dumps(json_object))

async def cancel_tasks(tasks):
    for task in tasks:
        if task.done():
            continue
        try:
            task.cancel()
            await task
        except asyncio.CancelledError:
            pass

async def select_parameter(variables: dict) -> tuple:

    params = list(variables.keys())
    sel_param = await select_list_entry("Bitte Einstellparameter auswählen:", params)
    return sel_param, variables[sel_param]

async def set_parameter(variables: dict, record: pd.DataFrame) -> pd.DataFrame:

    message = f"Wert auswählen:"
    if not "Event" in variables:
        param, var = await select_parameter(variables)
    else:
        param, var = "Event", variables["Event"]
    default = var["Value"]
    if isinstance(default, int) or isinstance(default, str):
        if "valid" in var:
            defaults = var["valid"]
            sel = await select_list_entry(message, defaults)
    else:
        sel = await cautious_float_input(message)

    record.loc[0, param] = sel
    return record