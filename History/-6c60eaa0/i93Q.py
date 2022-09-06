"""creates an OPCUA server for the output of the machine control
"""
import asyncio
import logging
from datetime import datetime

import pandas as pd
from atoolbox import FileHandler

from fyrsonic.mqtt_pub.common import BROKER, publish_dataframe, set_parameter

# from sqlalchemy import create_engine


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

_logger = logging.getLogger("user_control_cmd")
_logger.setLevel(logging.WARNING)


TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


async def cmd_input():

    # load format json into an dataframe
    f = FileHandler(filename="user_control.json", subdir=["data", "Settings", "opcua"])
    setup = f.read()
    variables = setup["label"]["Variables"]
    df = pd.DataFrame({key: [val["Value"]] for key, val in variables.items()})

    # engine = create_engine("sqlite:///data/Measurements/user.db", echo=False)
    meta = setup["user_metadata"]["Variables"]
    df2 = pd.DataFrame({key: [val["Value"]] for key, val in meta.items()})
    await publish_dataframe(broker=BROKER, topic="user_meta", df=df2, retain=True)

    while True:
        df = await set_parameter(variables, df)
        df["timestamp"] = datetime.now().strftime(TIMESTAMP_FORMAT)
        # df.to_sql(name="tblUser", con=engine, if_exists="append", index=False)
        # df["material"] = df["material"].astype("category")
        # encode_map = {"Federstahl": 0, "Baustahl": 1, "Edelstahl": 2}
        # df = df["material"].replace(encode_map)
        # df["greasing"] = df["greasing"].astype("category")
        # encode_map = {"Federstahl": 0, "Baustahl": 1, "Edelstahl": 2}
        # df = df["greasing"].replace(encode_map)
        # df["cooling"] = df["cooling"].astype("category")
        # encode_map = {"Federstahl": 0, "Baustahl": 1, "Edelstahl": 2}
        # df = df["cooling"].replace(encode_map)
        await publish_dataframe(broker=BROKER, topic="user_data", df=df, retain=True)


async def main():
    print(
        """

    ~~~~~~~~~~~~~~~~~~~~~~~
    ~~~~~USER CONTROL~~~~~~
    ~~~~~~~~~~~~~~~~~~~~~~~


    """
    )
    # Run the advanced_example indefinitely. Reconnect automatically
    # if the connection is lost.
    reconnect_interval = 3  # [seconds]
    while True:
        try:
            await cmd_input()
        except Exception as error:
            print(f'Error "{error}". Reconnecting in {reconnect_interval} seconds.')
        finally:
            await asyncio.sleep(reconnect_interval)


asyncio.run(main())
