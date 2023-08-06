# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['raesl',
 'raesl.compile',
 'raesl.compile.ast',
 'raesl.compile.instantiating',
 'raesl.compile.machine_files',
 'raesl.compile.typechecking',
 'raesl.datasets',
 'raesl.doc',
 'raesl.doc.locales',
 'raesl.excel',
 'raesl.jupyter',
 'raesl.plot',
 'raesl.server']

package_data = \
{'': ['*'], 'raesl.doc': ['templates/*']}

install_requires = \
['click-log>=0.3.2,<0.4.0',
 'click>=8.0.0,<9.0.0',
 'graphviz>=0.17,<0.18',
 'numpy>=1.21.1,<2.0.0',
 'openpyxl>=3.0.8,<4.0.0',
 'ragraph>=1.15.1,<2.0.0',
 'sly>=0.4.0,<0.5.0']

extras_require = \
{'doc': ['pandoc_fignos>=2.4.0,<3.0.0',
         'pluggy>=1.0.0,<2.0.0',
         'pypandoc>=1.4.0,<2.0.0'],
 'jupyter': ['ipykernel>=6.4.1,<7.0.0',
             'IPython>=7.13.0,<8.0.0',
             'ipywidgets>=7.5,<8.0',
             'jupyter_client>=7.0.6,<8.0.0',
             'notebook>=6.0.0,<7.0.0'],
 'rich': ['kaleido==0.2.1', 'plotly>=5.0.0,<6.0.0'],
 'server': ['pygls>=0.11.0,<0.12.0']}

entry_points = \
{'console_scripts': ['raesl = raesl.cli:cli']}

setup_kwargs = {
    'name': 'raesl',
    'version': '0.11.0',
    'description': 'Ratio ESL support in Python.',
    'long_description': "#########\nRatio ESL\n#########\n\nRatio support for the  Elephant Specification Language (ESL) in Python.\n\n\n**********\nQuickstart\n**********\n\nInstallation\n============\n\nRaESL can be installed using ``pip install raesl`` for any Python version >=3.9. Or,\nfor Poetry managed projects, use ``poetry add raesl`` to add it as a dependency.\n\nFor RaESL's different subcommands and functionality, the wheel provides extras:\n\n* doc: documentation generation using pandoc, Markdown and optionally LaTeX.\n* jupyter: a Jupyter ESL kernel.\n* pygments: an ESL syntax highlighter for pygments.\n* rich: Rich doc output in the form of Plotly images.\n* server: A language server to parse documents.\n\n\nThe default ``compile`` command is always available.\n\nPlease refer to the `usage documentation <https://raesl.ratio-case.nl>`_ for more info\non how to use RaESL.\n\n\n***************\nDeveloper guide\n***************\n\nPython packaging information\n============================\n\nThis project is packaged using `poetry <https://python-poetry.org/>`_. Packaging\ninformation as well as dependencies are stored in `pyproject.toml <./pyproject.toml>`_.\n\nInstalling the project and its development dependencies can be done using ``poetry install``.\n\n\nInvoke tasks\n============\n\nMost elemental maintenance tasks can be accomplished using\n[Invoke](https://www.pyinvoke.org/). After installing using ``poetry install`` and\nenabling the environment using ``poetry shell``, you can run all tasks using ``inv\n[taskname]`` or ``invoke [taskname]``. E.g. ``inv docs`` builds the documentation.\n\n\nVersioning\n==========\n\nThis project uses `semantic versioning <https://semver.org>`_. Version increments are\nchecked using `Raver <https://raver.ratio-case.nl>`_.\n\n\nChangelog\n=========\n\nChangelog format as described by https://keepachangelog.com/ has been adopted.\n",
    'author': 'Ratio Innovations B.V.',
    'author_email': 'info@ratio-case.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/ratio-case/python/raesl',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
