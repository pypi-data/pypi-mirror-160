from __future__ import annotations

import re
from typing import Any

import requests


class Github:

    response: Any

    def __init__(self, url: str):
        match = re.match(".*github\\.com/([^/]*/[^/]*).*", url)
        if not match:
            raise Exception("Wrong github URL.")
        response = requests.get("https://api.github.com/repos/{}".format(match[1]))
        response.raise_for_status()
        self.response = response.json()

    @property
    def name(self) -> str:
        return self.response["name"]

    @property
    def full_name(self) -> str:
        return self.response["full_name"]

    @property
    def description(self) -> str:
        return self.response["description"]
