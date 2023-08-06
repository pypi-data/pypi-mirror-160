# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sqlalchemy_extras']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.0,<2.0.0']

extras_require = \
{'fastapi': ['fastapi>=0.60.0,<1.0.0']}

setup_kwargs = {
    'name': 'sqlalchemy-extras',
    'version': '1.2.3',
    'description': '',
    'long_description': '',
    'author': 'Francisco Del Roio',
    'author_email': 'francipvb@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
