# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['poolcontrolpy']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0', 'asyncio>=3.4.3,<4.0.0']

setup_kwargs = {
    'name': 'poolcontrolpy',
    'version': '0.0.0',
    'description': 'Package for accessing nodejs-poolController',
    'long_description': '# poolcontrolpy\n\nPackage for accessing nodejs-poolController\n\n## Installation\n\n```bash\n$ pip install poolcontrolpy\n```\n\n## Usage\n\n- TODO\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`poolcontrolpy` was created by Kevin Robinson. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`poolcontrolpy` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Kevin Robinson',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
