# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "httpx",
#     "rich",
# ]
# ///
from datetime import datetime

import httpx
from rich.pretty import pprint

resp = httpx.get("https://peps.python.org/api/peps.json")
data = resp.json()
peps_desc_created = sorted(
    data.items(),
    key=lambda item: datetime.strptime(item[1]["created"], "%d-%b-%Y"),
    reverse=True,
)
pprint([(k, v["title"], v["created"]) for k, v in peps_desc_created][:10])
