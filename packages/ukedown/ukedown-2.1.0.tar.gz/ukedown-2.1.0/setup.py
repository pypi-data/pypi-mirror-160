# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ukedown']

package_data = \
{'': ['*']}

install_requires = \
['Markdown>=3']

setup_kwargs = {
    'name': 'ukedown',
    'version': '2.1.0',
    'description': 'Markdown extensions for songsheet creation',
    'long_description': None,
    'author': 'Stuart Sears',
    'author_email': 'stuart@sjsears.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
