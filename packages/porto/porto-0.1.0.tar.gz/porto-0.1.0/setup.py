# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['porto', 'porto.providers']

package_data = \
{'': ['*']}

install_requires = \
['inema>=0.8.6,<0.9.0', 'py-moneyed>=2.0,<3.0', 'pycountry>=22.3.5,<23.0.0']

setup_kwargs = {
    'name': 'porto',
    'version': '0.1.0',
    'description': 'Porto provides a unified and simple interface to various online stamp services.',
    'long_description': 'Porto\n=====\n\nPorto provides an unified and simplified access to various online stamp services. Currently supported are the following services:\n\n* Deutsche Post: Internetmarke (Germany)\n\nInstallation\n------------\n\nThe simplest way to install Porto is using pip:\n\n..\n\n  pip install porto\n\nAdditionally, you can checkout the source code:\n\n..\n\n  git clone https://edugit.org/hansegucker/porto\n\nLicense\n-------\n\nCopyright 2022 Jonathan Weth <dev@jonathanweth.de>\n\nLicensed under the MIT License (see LICENSE for more information).\n',
    'author': 'Jonathan Weth',
    'author_email': 'dev@jonathanweth.de',
    'maintainer': 'Jonathan Weth',
    'maintainer_email': 'dev@jonathanweth.de',
    'url': 'https://edugit.org/hansegucker/porto',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
