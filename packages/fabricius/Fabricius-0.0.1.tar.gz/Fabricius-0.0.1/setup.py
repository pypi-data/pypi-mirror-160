# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fabricius', 'fabricius.contracts']

package_data = \
{'': ['*']}

install_requires = \
['chevron>=0.14.0,<0.15.0',
 'inflection>=0.5.1,<0.6.0',
 'rich>=12.4.4,<13.0.0',
 'typing-extensions>=4.2.0,<5.0.0']

setup_kwargs = {
    'name': 'fabricius',
    'version': '0.0.1',
    'description': 'Fabricius: The supportive templating engine for Python!',
    'long_description': None,
    'author': 'Predeactor',
    'author_email': 'pro.julien.mauroy@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
