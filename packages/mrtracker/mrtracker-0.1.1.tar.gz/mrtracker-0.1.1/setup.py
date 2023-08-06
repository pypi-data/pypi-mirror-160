# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mrtracker', 'mrtracker.views', 'mrtracker.widgets']

package_data = \
{'': ['*']}

install_requires = \
['jsonmerge>=1.8.0,<2.0.0',
 'platformdirs>=2.5.2,<3.0.0',
 'textual>=0.1.18,<0.2.0']

entry_points = \
{'console_scripts': ['mrtracker = mrtracker.__main__:main']}

setup_kwargs = {
    'name': 'mrtracker',
    'version': '0.1.1',
    'description': 'A TUI time tracker',
    'long_description': None,
    'author': 'Mark Bragin',
    'author_email': 'm4rk.brag1n@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/markbragin/mrtracker',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
