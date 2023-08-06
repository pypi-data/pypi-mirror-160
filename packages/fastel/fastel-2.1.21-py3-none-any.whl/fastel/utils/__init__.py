# utils
import time

import pytz

TW = pytz.timezone("Asia/Taipei")


def timestamp_postfix(name: str) -> str:
    return name + "_" + str(int(time.time()))
