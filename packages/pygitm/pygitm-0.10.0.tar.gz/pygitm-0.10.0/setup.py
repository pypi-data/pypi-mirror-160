# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pygitm']

package_data = \
{'': ['*']}

install_requires = \
['pytcm>=0.5.6,<0.6.0']

setup_kwargs = {
    'name': 'pygitm',
    'version': '0.10.0',
    'description': 'A git library written in Python',
    'long_description': '# pygitm\n\nA git library written in Python\n\n## Installation\n\n```\n$ pip install pygitm\n```\n\n## Usage\n\nCOMING SOON\n\n## Contributing\n\nThank you for considering making pytcm better.\n\nPlease refer to [docs](docs/CONTRIBUTING.md).\n\n## Change Log\n\nSee [CHANGELOG](CHANGELOG.md)\n\n## License\n\nMIT',
    'author': 'Alexis Beaulieu',
    'author_email': 'alexisbeaulieu97@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/alexisbeaulieu97/pygitm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
