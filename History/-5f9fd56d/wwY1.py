"""creates an OPCUA server for the output of the machine control
"""
import asyncio
import logging
import pandas as pd

from typing import Dict

from atoolbox import FileHandler
from sqlalchemy import create_engine

from fyrsonic.opcua_servers import update_variable, utils
from fyrsonic.utils.input_handler import (
    cautious_float_input,
    select_list_entry,
)

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

    await update_variable(var["NodeID"], sel)

    record.loc[0, param] = sel
    return record


async def main(setup: Dict, opcua_server: bool = True) -> None:
    print(
        """
    
    ~~~~~~~~~~~~~~~~~~~~~~~
    ~~~~~USER CONTROL~~~~~~
    ~~~~~~~~~~~~~~~~~~~~~~~


    """
    )
    server_info = setup["server_info"]["Variables"]
    server = {
        k: v["Value"] for k, v in server_info.items()
    }  # TODO Avoid this workaround
    (server, setup) = await utils.initialize_opcua_sever(server, setup)

    _logger.info("Starting machine control OPCUA server!")
    engine = create_engine("sqlite:///data/Measurements/user.db", echo=False)
    async with server["server"]:

        variables = setup["label"]["Variables"]
        df = pd.DataFrame({key: [val["Value"]] for key, val in variables.items()})
        while True:
            df = await set_parameter(variables, df)
            df["Time"] = pd.Timestamp.now()
            df.to_sql(name="tblUser", con=engine, if_exists="append", index=False)


if __name__ == "__main__":

    f = FileHandler("*", subdir=["data", "Settings", "opcua"])
    setup = f.files["user_control.json"].read()

    try:
        asyncio.run(main(setup))
    except KeyboardInterrupt:
        _logger.info("\n User Control OPCUA Server heruntergefahren.")
