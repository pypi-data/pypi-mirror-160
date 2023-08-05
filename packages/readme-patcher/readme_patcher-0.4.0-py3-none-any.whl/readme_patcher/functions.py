from __future__ import annotations

"""https://jinja.palletsprojects.com/en/3.1.x/api/#custom-filters"""


import importlib
import re
import subprocess

from jinja2 import pass_context
from jinja2.runtime import Context


def read_cli_output(command: str, strip_whitespaces: bool = True) -> str:
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    output = result.stdout + result.stderr
    # clean ansi codes
    output = re.sub(r"\x1b.*?m", "", output)
    if strip_whitespaces:
        output = output.strip()
    return output


def read_func_output(function_spec: str) -> str:
    module, func_name = function_spec.rsplit(".", 1)
    func = getattr(importlib.import_module(module), func_name)
    return func()


@pass_context
def generate_github_workflow_badge(context: Context, workflow: str = "tests"):
    github = context.get('github')
    if not github:
        raise Exception('No github repo found')
    url = "https://github.com/{}/actions/workflows/{}.yml".format(
        github.full_name, workflow
    )

    return (
        ".. image:: {}/badge.svg\n".format(url)
        + "    :target: {}\n".format(url)
        + "    :alt: Tests"
    )


collection = {
    "cli": read_cli_output,
    "func": read_func_output,
    "github_workflow_badge": generate_github_workflow_badge,
}
