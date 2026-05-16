# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "httpxyz",
#     "rich",
# ]
# ///
import logging.config
from datetime import datetime

import httpxyz
from rich.pretty import pprint

logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "root": {
            "level": "DEBUG",
            "handlers": ["console"],
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "detailed",
                "filters": ["httpxyz"],
            },
        },
        "formatters": {
            "detailed": {
                "format": "%(asctime)s | %(levelname)s (%(name)s) | %(filename)s:%(funcName)s:%(lineno)d - %(message)s"
            },
        },
        "filters": {
            "httpxyz": {
                "name": "httpxyz",
            },
        },
    }
)

resp = httpxyz.get("https://peps.python.org/api/peps.json")
data = resp.json()
peps_desc_created = sorted(
    data.items(),
    key=lambda item: datetime.strptime(item[1]["created"], "%d-%b-%Y"),
    reverse=True,
)
pprint([(k, v["title"], v["created"]) for k, v in peps_desc_created][:10])
