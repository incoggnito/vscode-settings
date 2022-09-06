"""creates an OPCUA server for the output of the machine control
"""
import asyncio
import logging
import pandas as pd
from atoolbox import FileHandler
#from sqlalchemy import create_engine

from fyrsonic.utils.input_handler import (
    cautious_float_input,
    select_list_entry,
)

from .common import publish_dataframe

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

_logger = logging.getLogger("user_control_cmd")
_logger.setLevel(logging.WARNING)


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

async def cmd_input():

    # load format json into an dataframe
    f= FileHandler(filename="user_control.json", subdir=["data", "Settings", "opcua"])
    setup = f.read()
    variables = setup["label"]["Variables"]
    df = pd.DataFrame({key: [val["Value"]] for key, val in variables.items()})

    #engine = create_engine("sqlite:///data/Measurements/user.db", echo=False)

    while True:
        df = await set_parameter(variables, df)
        df["Time"] = pd.Timestamp.now()
        #df.to_sql(name="tblUser", con=engine, if_exists="append", index=False)
        await publish_dataframe(broker="192.168.102.109", name="User", df=df)

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