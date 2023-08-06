# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['sherlockeys']
install_requires = \
['colorama>=0.4.5,<0.5.0',
 'requests>=2.28.1,<3.0.0',
 'validators>=0.20.0,<0.21.0']

entry_points = \
{'console_scripts': ['APPLICATION-NAME = sherlockeys:main']}

setup_kwargs = {
    'name': 'sherlockeys',
    'version': '0.1.0',
    'description': 'Sherlockeys is a usefull tool for pen-tester. It can quickly try to discover if a given api key works against the most common saas applications.',
    'long_description': None,
    'author': 's2b1n0',
    'author_email': 'joao.nsabino@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
