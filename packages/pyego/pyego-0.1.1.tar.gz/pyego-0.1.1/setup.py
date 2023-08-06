# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pyego', 'tests']

package_data = \
{'': ['*']}

modules = \
['Makefile']
install_requires = \
['requests>=2.28.1,<3.0.0', 'ujson>=5.4.0,<6.0.0']

entry_points = \
{'console_scripts': ['ego-cli = pyego.cli:execute']}

setup_kwargs = {
    'name': 'pyego',
    'version': '0.1.1',
    'description': 'Short distribution description.',
    'long_description': '# Coming soon.\n',
    'author': 'John Doe',
    'author_email': 'john.doe@ema.il',
    'maintainer': 'Smith Doe',
    'maintainer_email': 'smith.doe@ema.il',
    'url': 'https://github.com/johndoe/reponame/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
