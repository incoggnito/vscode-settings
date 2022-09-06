"""creates an OPCUA server for the output of the machine control
"""
import asyncio
import logging
import pandas as pd
from atoolbox import FileHandler
from sqlalchemy import create_engine

from fyrsonic.utils.input_handler import (
    cautious_float_input,
    select_list_entry,
    yes_no,
)

from fyrsonic.u.common import publish_dataframe, select_parameter

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

_logger = logging.getLogger("maschine_control_cmd")
_logger.setLevel(logging.WARNING)


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

    # TODO update to mqtt instead -> await update_variable(var["NodeID"], sel)

    record.loc[0, param] = sel
    return record

async def cmd_input():

    # load format json into an dataframe
    f= FileHandler(filename="machine_control.json", subdir=["data", "Settings", "opcua"])
    setup = f.read()
    variables = setup["process_data"]["Variables"]
    df = pd.DataFrame({key: [val["Value"]] for key, val in variables.items()})

    engine = create_engine("sqlite:///data/Measurements/meta.db", echo=False)
    while True:
        print("\nNeues Setup anlegen!")
        df = await set_parameter(variables, df)
        df["Time"] = pd.Timestamp.now()
        while True:
            status = await yes_no("Weitere Parameter ändern?")
            if status:
                df = await set_parameter(variables, df)
                df["Time"] = pd.Timestamp.now()
            else:
                break
        df.to_sql(name="tblMeta", con=engine, if_exists="append", index=False)
        await publish_dataframe(broker="192.168.102.109", name="Machine", df=df)

async def main():
    print(
        """
    
    ~~~~~~~~~~~~~~~~~~~~~~~
    ~~~~MACHINE CONTROL~~~~
    ~~~~~~~~~~~~~~~~~~~~~~~


    """
    )
    # Run the advanced_example indefinitely. Reconnect automatically
    # if the connection is lost.
    reconnect_interval = 3  # [seconds]
    while True:
        try:
            df = await cmd_input()
            #await publish_machine_state()
        except Exception as error:
            print(f'Error "{error}". Reconnecting in {reconnect_interval} seconds.')
        finally:
            await asyncio.sleep(reconnect_interval)


asyncio.run(main())