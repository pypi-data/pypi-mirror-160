# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['gekkota']
setup_kwargs = {
    'name': 'gekkota',
    'version': '0.1.0',
    'description': 'Python code-generation for Python',
    'long_description': None,
    'author': 'Dmitry Gritsenko',
    'author_email': 'k01419q45@ya.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
