"""creates an OPCUA server for the output of the machine control
"""
import asyncio
import logging
import pandas as pd
from atoolbox import FileHandler
#from sqlalchemy import create_engine

from .common import publish_dataframe, BROKER, set_parameter

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

_logger = logging.getLogger("user_control_cmd")
_logger.setLevel(logging.WARNING)

async def cmd_input():

    # load format json into an dataframe
    f= FileHandler(filename="user_control.json", subdir=["data", "Settings", "opcua"])
    setup = f.read()
    variables = setup["label"]["Variables"]
    df = pd.DataFrame({key: [val["Value"]] for key, val in variables.items()})

    #engine = create_engine("sqlite:///data/Measurements/user.db", echo=False)

    while True:
        df = await set_parameter({"Event":variables["Event"]}, df)
        df["Time"] = pd.Timestamp.now()
        #df.to_sql(name="tblUser", con=engine, if_exists="append", index=False)
        await publish_dataframe(broker=BROKER, name="User", df=df)

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