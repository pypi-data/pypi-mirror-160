# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sapcloudsdk']

package_data = \
{'': ['*']}

install_requires = \
['Markdown>=3.3.7,<4.0.0', 'requests>=2.27.1,<3.0.0']

entry_points = \
{'console_scripts': ['sapcloudsdk = sapcloudsdk.run:main']}

setup_kwargs = {
    'name': 'sapcloudsdk',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Florian Richter',
    'author_email': 'florian.richter@sap.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
