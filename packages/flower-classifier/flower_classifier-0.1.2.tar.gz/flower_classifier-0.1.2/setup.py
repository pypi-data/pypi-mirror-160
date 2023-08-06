# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flower_classifier',
 'flower_classifier.configs',
 'flower_classifier.dataload',
 'flower_classifier.model',
 'flower_classifier.utils']

package_data = \
{'': ['*'], 'flower_classifier': ['references/*']}

install_requires = \
['black>=22.6.0,<23.0.0',
 'isort>=5.10.1,<6.0.0',
 'pylint>=2.14.4,<3.0.0',
 'wandb>=0.12.21,<0.13.0',
 'yacs>=0.1.8,<0.2.0']

setup_kwargs = {
    'name': 'flower-classifier',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'hoopoes',
    'author_email': 'pushkin522@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
