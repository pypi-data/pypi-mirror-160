# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aymara']

package_data = \
{'': ['*']}

install_requires = \
['pip>=22.0,<23.0',
 'pyconll>=2.0,<3.0',
 'pydantic>=1.8.2,<2.0.0',
 'requests>=2.22,<3.0',
 'shiboken2>=5.15.2,<6.0.0',
 'tqdm>=4.56.0,<5.0.0',
 'unix-ar>=0.2.1b,<0.3.0']

setup_kwargs = {
    'name': 'aymara',
    'version': '0.4.0',
    'description': 'Python bindings to the LIMA linguistic analyzer',
    'long_description': None,
    'author': 'Gael de Chalendar',
    'author_email': 'gael.de-chalendar@cea.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
