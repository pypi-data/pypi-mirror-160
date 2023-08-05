# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['readme_patcher']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'pyproject-parser>=0.7.0,<0.8.0',
 'requests>=2,<3',
 'types-requests>=2.28.2,<3.0.0']

entry_points = \
{'console_scripts': ['readme-patcher = readme_patcher:main']}

setup_kwargs = {
    'name': 'readme-patcher',
    'version': '0.5.0',
    'description': 'Generate README files from templates. Allow input from functions calls and cli output.',
    'long_description': '.. image:: http://img.shields.io/pypi/v/readme-patcher.svg\n    :target: https://pypi.org/project/readme-patcher\n    :alt: This package on the Python Package Index\n\n.. image:: https://github.com/Josef-Friedrich/readme_patcher/actions/workflows/tests.yml/badge.svg\n    :target: https://github.com/Josef-Friedrich/readme_patcher/actions/workflows/tests.yml\n    :alt: Tests\n\nreadme_patcher\n==============\n\nGenerate README files from templates. Allow input from functions calls and cli\noutput.\n\n.. code-block:: shell\n\n    cd your-project\n    vim README_template.rst\n    poetry add --group dev readme-patcher\n    poetry shell\n    readme-patcher # README.rst\n\nGlobal objects\n--------------\n\npy_project\n^^^^^^^^^^\n\n.. code-block:: jinja\n\n    {{ py_project.repository }}\n\ngithub\n^^^^^^\n\n.. code-block:: jinja\n\n    {{ github.name }}\n    {{ github.full_name }}\n    {{ github.description }}\n\nbadge\n^^^^^\n\n.. code-block:: jinja\n\n    {{ badge.pypi }}\n    {{ badge.github_workflow(\'tests\' \'Tests\') }}\n    {{ badge.readthedocs }}\n\nFunctions\n---------\n\ncli: Combined output (stdout and stderr) of command line interfaces (scripts / binaries)\n\n.. code-block:: jinja\n\n    {{ cli(\'awk --help\') }}\n\nfunc: return values of Python functions\n\n.. code-block:: jinja\n\n    {{ func(\'os.getcwd\') }}\n\nread: read text files\n\n.. code-block:: jinja\n\n    {{ read(\'code/example.py\') | code(\'python\') }}\n\nFilters\n-------\n\ncode\n\n.. code-block:: jinja\n\n    {{ \'print("example")\' | code(\'python\') }}\n\n::\n\n    .. code-block:: python\n\n        print("example")\n\nliteral\n\n.. code-block:: jinja\n\n    {{ func(\'os.getcwd\') | literal }}\n\n::\n\n    ::\n\n        /home/repos/project\n\nConfiguration\n-------------\n\n.. code-block:: toml\n\n    [[tool.readme_patcher.file]]\n    src = "README_template.rst"\n    dest = "README.rst"\n    variables = { cwd = "func:os.getcwd", fortune = "cli:fortune --help" }\n',
    'author': 'Josef Friedrich',
    'author_email': 'josef@friedrich.rocks',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Josef-Friedrich/readme_patcher',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
