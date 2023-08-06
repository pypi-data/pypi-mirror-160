# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tcgplayersdk', 'tcgplayersdk.schemas']

package_data = \
{'': ['*']}

install_requires = \
['marshmallow>=3.17.0,<4.0.0',
 'marshmallow_dataclass>=8.5.8,<9.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'requests>=2.28.1,<3.0.0',
 'stringcase>=1.2.0,<2.0.0']

setup_kwargs = {
    'name': 'tcgplayersdk',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'CptSpaceToaster',
    'author_email': 'cptspacetoaster@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
