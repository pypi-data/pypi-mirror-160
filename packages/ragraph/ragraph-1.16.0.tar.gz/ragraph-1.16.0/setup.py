# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ragraph',
 'ragraph.analysis',
 'ragraph.analysis.bus',
 'ragraph.analysis.cluster',
 'ragraph.analysis.comparison',
 'ragraph.analysis.compatibility',
 'ragraph.analysis.heuristics',
 'ragraph.analysis.sequence',
 'ragraph.analysis.similarity',
 'ragraph.colors',
 'ragraph.datasets',
 'ragraph.datasets.aircraft_engine',
 'ragraph.datasets.architecture_integral',
 'ragraph.datasets.architecture_mix',
 'ragraph.datasets.architecture_modular',
 'ragraph.datasets.climate_control',
 'ragraph.datasets.climate_control_mg',
 'ragraph.datasets.compatibility',
 'ragraph.datasets.design',
 'ragraph.datasets.eefde_lock',
 'ragraph.datasets.elevator175',
 'ragraph.datasets.elevator45',
 'ragraph.datasets.esl',
 'ragraph.datasets.esl.pump',
 'ragraph.datasets.ford_hood',
 'ragraph.datasets.kodak3d',
 'ragraph.datasets.ledsip',
 'ragraph.datasets.localbus',
 'ragraph.datasets.overlap',
 'ragraph.datasets.pathfinder',
 'ragraph.datasets.shaja8',
 'ragraph.datasets.similarity',
 'ragraph.datasets.tarjans8',
 'ragraph.datasets.ucav',
 'ragraph.io',
 'ragraph.io.archimate',
 'ragraph.io.xml',
 'ragraph.plot',
 'ragraph.plot.components']

package_data = \
{'': ['*']}

install_requires = \
['dd>=0.5.7,<0.6.0',
 'lxml>=4.8.0,<5.0.0',
 'numpy>=1.22.3,<2.0.0',
 'plotly>=5.7.0,<6.0.0',
 'ruamel.yaml>=0.17.21,<0.18.0']

extras_require = \
{'esl': ['raesl'], 'plot': ['kaleido==0.2.1']}

setup_kwargs = {
    'name': 'ragraph',
    'version': '1.16.0',
    'description': 'Ratio graph handling in Python.',
    'long_description': "#######\nRaGraph\n#######\n\nRaGraph is a package to create, manipulate, and analyze graphs consisting of nodes and\nedges. Nodes usually represent (hierarchies of) objects and edges the dependencies or\nrelationships between them.\n\nThese graphs, or networks if you will, lend themselves well to applied analyses like\nclustering and sequencing, as well as analyses involving the calculation of various\ninsightful metrics.\n\n\n**********\nQuickstart\n**********\n\nInstallation\n============\n\nRaGraph can be installed using ``pip install ragraph`` for any Python version >=3.9. Or,\nfor Poetry managed projects, use ``poetry add ragraph`` to add it as a dependency.\n\n\nUsing RaGraph\n=============\n\nRaGraph's primary use is working with Graph objects that contain Nodes and Eges between\nNodes. See the `usage documentation <https://ragraph.ratio-case.nl/usage/index.html>`_\nfor more info!\n\n\n***************\nDeveloper guide\n***************\n\nPython packaging information\n============================\n\nThis project is packaged using `poetry <https://python-poetry.org/>`_. Packaging\ninformation as well as dependencies are stored in `pyproject.toml <./pyproject.toml>`_.\n\nInstalling the project and its development dependencies can be done using ``poetry install``.\n\n\nInvoke tasks\n============\n\nMost elemental maintenance tasks can be accomplished using\n[Invoke](https://www.pyinvoke.org/). After installing using ``poetry install`` and\nenabling the environment using ``poetry shell``, you can run all tasks using ``inv\n[taskname]`` or ``invoke [taskname]``. E.g. ``inv docs`` builds the documentation.\n\n\nVersioning\n==========\n\nThis project uses `semantic versioning <https://semver.org>`_. Version increments are\nchecked using `Raver <https://raver.ratio-case.nl>`_.\n\n\nChangelog\n=========\n\nChangelog format as described by https://keepachangelog.com/ has been adopted.\n",
    'author': 'Ratio Innovations B.V.',
    'author_email': 'info@ratio-case.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/ratio-case/python/ragraph',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
