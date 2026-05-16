# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "httpxyz",
#     "python-json-logger",
#     "rich",
# ]
# ///
import logging
from datetime import datetime

import httpxyz
from pythonjsonlogger.json import JsonFormatter
from rich.pretty import pprint

root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
json_formatter = JsonFormatter(
    "%(asctime)s | %(levelname)s (%(name)s) | %(filename)s:%(funcName)s:%(lineno)d - %(message)s"
)
console_handler.setFormatter(json_formatter)
root_logger.addHandler(console_handler)
console_handler.addFilter(logging.Filter("httpxyz"))

resp = httpxyz.get("https://peps.python.org/api/peps.json")
data = resp.json()
peps_desc_created = sorted(
    data.items(),
    key=lambda item: datetime.strptime(item[1]["created"], "%d-%b-%Y"),
    reverse=True,
)
pprint([(k, v["title"], v["created"]) for k, v in peps_desc_created][:10])
