"""creates an OPCUA server for the output of the machine control
"""
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

_logger = logging.getLogger("maschine_control_cmd")
_logger.setLevel(logging.WARNING)

async def select_parameter(variables: dict) -> tuple:

    params = list(variables.keys())
    sel_param = await select_list_entry("Bitte Einstellparameter auswählen:", params)
    return sel_param, variables[sel_param]

async def set_parameter(variables: dict, record: pd.DataFrame) -> pd.DataFrame:

    message = f"Event auswählen:"
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

async def cmd_input() -> pd.DataFrame:

    # load format json into an dataframe
    f= FileHandler(filename="machine_control.json", subdir=["data", "Settings", "opcua"])
    setup = f.read()
    variables = setup["process_data"]["Variables"]
    df = pd.DataFrame({key: [val["Value"]] for key, val in variables.items()})

    engine = create_engine("sqlite:///data/Measurements/user.db", echo=False)

    while True:
        df = await set_parameter(variables, df)
        df["Time"] = pd.Timestamp.now()
        df.to_sql(name="tblUser", con=engine, if_exists="append", index=False)
        await publish_machine_state(df)
        # df.to_sql(name="tblMeta", con=engine, if_exists="append", index=False)

async def publish_machine_state(df: pd.DataFrame):
    # We 💛 context managers. Let's create a stack to help
    # us manage them.
    async with AsyncExitStack() as stack:
        # Keep track of the asyncio tasks that we create, so that
        # we can cancel them on exit
        tasks = set()
        stack.push_async_callback(cancel_tasks, tasks)

        # Connect to the MQTT broker
        client = Client("192.168.102.109")
        await stack.enter_async_context(client)

        task = asyncio.create_task(mqtt_publish_data(client, df))
        tasks.add(task)

        # Wait for everything to complete (or fail due to, e.g., network
        # errors)
        await asyncio.gather(*tasks)

async def mqtt_publish_data(client, df):
    json_object = {} 
    json_object["data"] = df.loc[0].to_json()
    await client.publish("machine_data", json.dumps(json_object))


async def cancel_tasks(tasks):
    for task in tasks:
        if task.done():
            continue
        try:
            task.cancel()
            await task
        except asyncio.CancelledError:
            pass

async def main():
    # Run the advanced_example indefinitely. Reconnect automatically
    # if the connection is lost.
    reconnect_interval = 3  # [seconds]
    while True:
        try:
            df = await cmd_input()
            #await publish_machine_state()
        except MqttError as error:
            print(f'Error "{error}". Reconnecting in {reconnect_interval} seconds.')
        finally:
            await asyncio.sleep(reconnect_interval)


asyncio.run(main())