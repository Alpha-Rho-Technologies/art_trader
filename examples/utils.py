import logging
import sys
from pathlib import Path

import MetaTrader5 as mt5


def get_script_name() -> str:
    return Path(sys.argv[0]).stem


def init_mt5(login: int, password: str, server: str):
    logging.info(f"MetaTRADER5 package author: {mt5.__author__}")
    logging.info(f"MetaTRADER5 package version: {mt5.__version__}")
    if not mt5.initialize(login=login, password=password, server=server):
        print("initialize() failed, error code ={}".format(mt5.last_error()))
        quit()
    return mt5.last_error()


def configLogger(log_level=logging.INFO):

    logging.basicConfig(
        force=True,
        level=log_level,
        format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
        handlers=[
            logging.StreamHandler()
        ]
    )

    logging.getLogger("apscheduler").setLevel(logging.WARN)
