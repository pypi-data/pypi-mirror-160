from __future__ import annotations

"""Custom jinja filters

https://jinja.palletsprojects.com/en/3.1.x/api/#custom-filters
"""

from jinja2.filters import do_indent


def _indent_block(content: str, strip_whitespace: bool = True) -> str:
    if strip_whitespace:
        content = content.strip()
    return "\n\n" + do_indent(content, width=4, first=True) + "\n\n"


def wrap_in_code_block(
    content: str, language: str = "", strip_whitespace: bool = True
) -> str:
    """https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-code-block

    https://pygments.org/docs/lexers/
    """
    return "\n.. code-block:: " + language + _indent_block(content, strip_whitespace)


def wrap_in_literal_block(content: str, strip_whitespace: bool = True) -> str:
    """
    https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html#literal-blocks
    """
    return "\n:: " + _indent_block(content, strip_whitespace)


collection = {"code": wrap_in_code_block, "literal": wrap_in_literal_block}
