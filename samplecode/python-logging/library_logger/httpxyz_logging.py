# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "httpxyz",
#     "rich",
# ]
# ///
import logging
from datetime import datetime

import httpxyz
from rich.pretty import pprint

httpxyz_logger = logging.getLogger("httpxyz")
httpxyz_logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
detailed_formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s (%(name)s) | %(filename)s:%(funcName)s:%(lineno)d - %(message)s"
)
console_handler.setFormatter(detailed_formatter)
httpxyz_logger.addHandler(console_handler)

resp = httpxyz.get("https://peps.python.org/api/peps.json")
data = resp.json()
peps_desc_created = sorted(
    data.items(),
    key=lambda item: datetime.strptime(item[1]["created"], "%d-%b-%Y"),
    reverse=True,
)
pprint([(k, v["title"], v["created"]) for k, v in peps_desc_created][:10])
