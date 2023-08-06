# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['epyg']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.23.1,<2.0.0']

setup_kwargs = {
    'name': 'epyg',
    'version': '0.2.0',
    'description': 'Python implementation of the Extended Phase Graph algorithm for simulation of MRI signals',
    'long_description': 'EpyG - Extended Phase Graphs in Python\n======================================\nAuthor: Daniel Brenner, (formerly) DZNE Bonn, \nStarted in: 2016, continued in 2022\n\nExtended Phase Graphs (EPG) are mathematical model of the signal evolution in magnetic resonance with particular applications\nimaging (MRI). \nThis python implementation of the EPG formalism aim at being usable from a user perspective, being suited for educational\nuses as well as providing adequate performance to allow \'real\' applicaltions e.g. for more "heavy" simulations.\nThe overall implementation follows the Operator notation as e.g. shown by Weigel.\n\nThe code is currently works in progress! Use with great care!\n\n## Installation\nEpyG is a pure python module built upon numpy.\n\nit uses [poetry](https://python-poetry.org) as build and distribution tool.\n\n## Package structure\nThe EpyG package is structured in 3 modules\n * EpyG - the actual representation of an Extended Phase Grap\n * Operators - implementation of Operators that manipulate EpyG\n * Applications - combinations of operators and looping to simulate real life MRI problems\n\n\n## First steps\nFor first steps it is advised to look at the example ipython/jupyter notebook(s) in the examples directory\n\n \n## Testing\nThe folder tests/ contains a set of unit/integration tests to prove basic functionality.\nFurther application examples can be found in the examples subfolder where Jupyter notebooks illustrating the major concepts are distributed\n\n',
    'author': 'Daniel Brenner',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/brennerd11/EpyG',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
