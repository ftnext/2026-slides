import logging.config
from datetime import datetime

import httpxyz
import tomllib
from rich.pretty import pprint

with open("config.toml", "rb") as f:
    config = tomllib.load(f)

logging.config.dictConfig(config)

resp = httpxyz.get("https://peps.python.org/api/peps.json")
data = resp.json()
peps_desc_created = sorted(
    data.items(),
    key=lambda item: datetime.strptime(item[1]["created"], "%d-%b-%Y"),
    reverse=True,
)
pprint([(k, v["title"], v["created"]) for k, v in peps_desc_created][:10])
