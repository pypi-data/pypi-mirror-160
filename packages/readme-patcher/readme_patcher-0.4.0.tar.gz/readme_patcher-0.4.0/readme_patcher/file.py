from __future__ import annotations

import os
import re
import typing
from typing import Dict, Optional, TypedDict

from jinja2 import Environment, FileSystemLoader, Template, select_autoescape

from readme_patcher.badge import Badge
from readme_patcher.github import Github

from . import filters, functions
from .config import args

if typing.TYPE_CHECKING:
    from .project import Project


class Replacement:
    """A variable and its replacement text."""

    raw: str

    def __init__(self, raw: str):
        self.raw = raw.strip()

    def get(self) -> str:
        output: str
        if self.raw.startswith("cli:"):
            output = functions.read_cli_output(self.raw[4:].strip())
        elif self.raw.startswith("func:"):
            output = functions.read_func_output(self.raw[5:].strip())
        else:
            output = self.raw
        return str(output)


class FileConfig(TypedDict):
    src: str
    dest: str
    variables: Optional[Dict[str, str]]


Variables = Dict[str, str]


def setup_template_env(search_path: "os.PathLike[str]") -> Environment:
    """
    Setup the search paths for the template engine Jinja2. ``os.path.sep`` is

    required to be able to include absolute paths, quotes around
    ``os.PathLike[str]`` to get py38 compatibility."""
    return Environment(
        loader=FileSystemLoader([search_path, os.path.sep]),
        autoescape=select_autoescape(),
        keep_trailing_newline=True,
    )


class File:
    """A file to patch."""

    project: "Project"
    src: str
    dest: str
    variables: Optional[Variables] = None

    def __init__(
        self,
        project: "Project",
        src: Optional[str] = None,
        dest: Optional[str] = None,
        variables: Optional[Variables] = None,
        config: Optional[FileConfig] = None,
    ):
        self.project = project
        if config:
            self.src = config["src"]
            self.dest = config["dest"]
            if "variables" in config:
                self.variables = config["variables"]
        if src:
            self.src = src
        if dest:
            self.dest = dest
        if variables:
            self.variables = variables

    def _setup_template(self) -> Template:
        env = setup_template_env(self.project.base_dir)
        env.filters.update(filters.collection)  # type: ignore
        template = env.get_template(self.src)
        template.globals.update(functions.collection)
        if self.project.py_project:
            template.globals.update(py_project=self.project.py_project)
            if self.project.py_project.repository:
                try:
                    github = Github(self.project.py_project.repository)
                    template.globals.update(github=github)
                except Exception:
                    pass

        template.globals.update(badge=Badge(self.project))
        return template

    def patch(self) -> str:
        if args.verbosity > 0:
            print("Patch file dest: {} src: {}".format(self.src, self.dest))
        template = self._setup_template()
        variables: Dict[str, str] = {}
        if self.variables:
            for k, v in self.variables.items():
                variables[k] = Replacement(v).get()
        rendered = template.render(**variables)
        # Remove multiple newlines
        rendered = re.sub(r"\n\s*\n", "\n\n", rendered)
        if args.verbosity > 1:
            print(rendered)
        dest = self.project.base_dir / self.dest
        dest.write_text(rendered)
        return rendered
