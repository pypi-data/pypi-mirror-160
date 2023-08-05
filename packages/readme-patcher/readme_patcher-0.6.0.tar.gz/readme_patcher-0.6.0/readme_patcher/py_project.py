from __future__ import annotations

import re
from functools import cached_property

from pyproject_parser import PyProject


class SimplePyProject:
    """Contain the attributes of a pyproject.toml file that interest us"""

    py_project: PyProject

    def __init__(self, py_project: PyProject):
        self.py_project = py_project

    @cached_property
    def name(self) -> str | None:
        if self.py_project.tool and self.py_project.tool["poetry"]["name"]:
            return self.py_project.tool["poetry"]["name"]
        return None

    @cached_property
    def name_normalized(self) -> str | None:
        if self.name:
            return re.sub(r"[-_.]+", "-", self.name).lower()
        return None

    @cached_property
    def repository(self) -> str | None:
        if self.py_project.tool and self.py_project.tool["poetry"]["repository"]:
            return self.py_project.tool["poetry"]["repository"]
        return None
