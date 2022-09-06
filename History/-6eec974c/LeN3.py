"""creates an OPCUA server for the output of the machine control
"""
import asyncio
import logging
from typing import Dict

import json
import pandas as pd
from atoolbox import FileHandler
from sqlalchemy import create_engine

from fyrsonic.opcua_servers import utils
from fyrsonic.utils.input_handler import (
    yes_no,
)

import paho.mqtt.client as paho

from contextlib import AsyncExitStack, asynccontextmanager
from random import randrange
from asyncio_mqtt import Client, MqttError

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

_logger = logging.getLogger("maschine_control_cmd")
_logger.setLevel(logging.WARNING)

async def select_parameter(variables: dict) -> tuple:

    params = list(variables.keys())
    sel_param = await select_list_entry("Bitte Einstellparameter auswählen:", params)
    return sel_param, variables[sel_param]

async def set_parameter(variables: dict, record: pd.DataFrame) -> pd.DataFrame:

    message = f"Wert eingeben:"
    param, var = await select_parameter(variables)
    default = var["Value"]
    if isinstance(default, int) or isinstance(default, str):
        if "valid" in var:
            defaults = var["valid"]
            sel = await select_list_entry(message, defaults)
    else:
        sel = await cautious_float_input(message)

    await update_variable(var["NodeID"], sel)

    record.loc[0, param] = sel
    return record

async def cmd_input():

    # load format json
    f= FileHandler(filename="machine_control.json", subdir=["data", "Settings", "opcua"])
    setup = f.read()
    variables = setup["process_data"]["Variables"]
    df = pd.DataFrame({key: [val["Value"]] for key, val in variables.items()})
    engine = create_engine("sqlite:///data/Measurements/meta.db", echo=False)
    while True:
        print("\nNeues Setup anlegen!")
        #df = await set_parameter(variables, df)
        df["Time"] = pd.Timestamp.now()
        while True:
            status = await yes_no("Weitere Parameter ändern?")
            if status:
                #df = await set_parameter(variables, df)
                df["Time"] = pd.Timestamp.now()
            else:
                break

        df.to_sql(name="tblMeta", con=engine, if_exists="append", index=False)

async def publish_machine_state():
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

        # Publish a random value to each of these topics

        task = asyncio.create_task(post_to_topics(client, topics))
        tasks.add(task)

        # Wait for everything to complete (or fail due to, e.g., network
        # errors)
        await asyncio.gather(*tasks)

async def post_to_topics(client, topics):
    while True:
        for topic in topics:
            message = randrange(100)
            print(f'[topic="{topic}"] Publishing message={message}')
            await client.publish(topic, message, qos=1)
            await asyncio.sleep(2)

async def publish_data(client, data_dict):
    for _, row in df.iterrows():        
        json_object["data"]["features"] = row.to_json()
        json_object["data"]["timestamp"] = datetime.utcnow().strftime(timestamp_format)
        await client.publish("vam_data", json.dumps(json_object))
        await asyncio.sleep(0.1)


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
            await publish_machine_state()
        except MqttError as error:
            print(f'Error "{error}". Reconnecting in {reconnect_interval} seconds.')
        finally:
            await asyncio.sleep(reconnect_interval)


asyncio.run(main())

# [ ] TODO add parameter "Ausgangsdraht": gewalzt (0), gezogen (1) -> gewalzter Ausgangsdraht läuft unruhiger als schon mal gezogener Draht


# async def main(setup: Dict) -> None:
#     print(
#         """
#     ~~~~~~~~~~~~~~~~~~~~~~~
#     ~~~~MACHINE CONTROL~~~~
#     ~~~~~~~~~~~~~~~~~~~~~~~
#     """
#     )
#     server = setup["mqtt"]
#     client = paho.Client(server.name)
#     client.on_connect = on_connect
#     client.on_disconnect = on_disconnect
#     client.connect(server.broker, server.port)

#     (server, setup) = await utils.initialize_opcua_sever(server, setup)

#     _logger.info("Starting machine control OPCUA server!")
#     engine = create_engine("sqlite:///data/Measurements/meta.db", echo=False)
#     async with server["server"]:
#         variables = setup["process_data"]["Variables"]
#         df = pd.DataFrame({key: [val["Value"]] for key, val in variables.items()})
#         while True:
#             print("\nNeues Setup anlegen!")
#             #df = await set_parameter(variables, df)
#             df["Time"] = pd.Timestamp.now()
#             while True:
#                 status = await yes_no("Weitere Parameter ändern?")
#                 if status:
#                     #df = await set_parameter(variables, df)
#                     df["Time"] = pd.Timestamp.now()
#                 else:
#                     break

#             df.to_sql(name="tblMeta", con=engine, if_exists="append", index=False)


# if __name__ == "__main__":

#     f = FileHandler("*", subdir=["data", "Settings", "opcua"])
#     setup = f.files["machine_control.json"].read()

#     try:
#         asyncio.run(main(setup))
#     except KeyboardInterrupt:
#         _logger.info("\nMachine Control OPCUA Server heruntergefahren.")
