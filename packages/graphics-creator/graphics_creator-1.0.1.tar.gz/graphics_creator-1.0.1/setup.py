# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['graphics_creator']
setup_kwargs = {
    'name': 'graphics-creator',
    'version': '1.0.1',
    'description': 'Python project for creation graphics',
    'long_description': None,
    'author': 'He1TPOH',
    'author_email': 'nikulin.vlad07@mail.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
