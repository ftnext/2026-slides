# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "httpxyz",
#     "rich",
#     "structlog",
# ]
# ///
import logging
from datetime import datetime

import httpxyz
import structlog
from rich.pretty import pprint

structlog.stdlib.recreate_defaults(log_level=logging.DEBUG)

root_handler = logging.getLogger().handlers[0]
root_handler.setFormatter(
    logging.Formatter(
        "%(asctime)s | %(levelname)s (%(name)s) | %(filename)s:%(funcName)s:%(lineno)d - %(message)s"
    )
)
root_handler.addFilter(logging.Filter("httpxyz"))

resp = httpxyz.get("https://peps.python.org/api/peps.json")
data = resp.json()
peps_desc_created = sorted(
    data.items(),
    key=lambda item: datetime.strptime(item[1]["created"], "%d-%b-%Y"),
    reverse=True,
)
pprint([(k, v["title"], v["created"]) for k, v in peps_desc_created][:10])
