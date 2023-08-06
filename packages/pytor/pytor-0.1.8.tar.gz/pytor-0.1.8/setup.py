# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytor', 'pytor.test']

package_data = \
{'': ['*']}

install_requires = \
['fire>=0.3.1', 'pycryptodome>=3.9.4', 'pyyaml>=5.3.1']

entry_points = \
{'console_scripts': ['pytor = pytor.__main__:main']}

setup_kwargs = {
    'name': 'pytor',
    'version': '0.1.8',
    'description': 'Manage Tor hidden services keys',
    'long_description': None,
    'author': 'Christophe Mehay',
    'author_email': 'cmehay@nospam.student.42.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://github.com/cmehay/pytor',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.12,<3.10',
}


setup(**setup_kwargs)
