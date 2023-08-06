# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['externaloverlayrep']
setup_kwargs = {
    'name': 'externaloverlayrep',
    'version': '1.0.0',
    'description': 'https://github.com/Xenely14/ExternalPyOverlay',
    'long_description': None,
    'author': 'Xenely14',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
