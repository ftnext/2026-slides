# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "httpxyz",
#     "PyYAML",
#     "rich",
# ]
# ///
import logging.config
from datetime import datetime
from pathlib import Path

import httpxyz
import yaml
from rich.pretty import pprint

config_path = Path(__file__).parent / "config.yml"
with config_path.open() as f:
    config = yaml.safe_load(f)
logging.config.dictConfig(config)

resp = httpxyz.get("https://peps.python.org/api/peps.json")
data = resp.json()
peps_desc_created = sorted(
    data.items(),
    key=lambda item: datetime.strptime(item[1]["created"], "%d-%b-%Y"),
    reverse=True,
)
pprint([(k, v["title"], v["created"]) for k, v in peps_desc_created][:10])
