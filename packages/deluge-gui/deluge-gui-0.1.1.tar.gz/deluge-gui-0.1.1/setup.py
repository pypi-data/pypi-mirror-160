# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deluge_gui']

package_data = \
{'': ['*']}

install_requires = \
['PySimpleGUI>=4.60.1,<5.0.0',
 'SoundFile>=0.10.3,<0.11.0',
 'deluge-card==0.7.2',
 'numpy>=1.23.1,<2.0.0',
 'pydel>=0.5.3,<0.6.0',
 'sounddevice>=0.4.4,<0.5.0']

entry_points = \
{'console_scripts': ['delgui = scripts.delgui:main']}

setup_kwargs = {
    'name': 'deluge-gui',
    'version': '0.1.1',
    'description': 'GUI for deluge-card and related for Mac, Linux & Windows..',
    'long_description': '# deluge-gui\n\n\n[![pypi](https://img.shields.io/pypi/v/deluge-gui.svg)](https://pypi.org/project/deluge-gui/)\n[![python](https://img.shields.io/pypi/pyversions/deluge-gui.svg)](https://pypi.org/project/deluge-gui/)\n[![Build Status](https://github.com/mupaduw/deluge-gui/actions/workflows/dev.yml/badge.svg)](https://github.com/mupaduw/deluge-gui/actions/workflows/dev.yml)\n[![codecov](https://codecov.io/gh/mupaduw/deluge-gui/branch/main/graphs/badge.svg)](https://codecov.io/github/mupaduw/deluge-gui)\n\n\n\nGUI for deluge-card and related for Mac, Linux & Windows.\n\n\n* Documentation: <https://mupaduw.github.io/deluge-gui>\n* GitHub: <https://github.com/mupaduw/deluge-gui>\n* PyPI: <https://pypi.org/project/deluge-gui/>\n* Free software: GPL-3.0-only\n\n\n## Features\n\n* TODO\n\n## Credits\n\nThis package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [waynerv/cookiecutter-pypackage](https://github.com/waynerv/cookiecutter-pypackage) project template.\n',
    'author': 'Chris B Chamberlain',
    'author_email': 'chrisbc@artisan.co.nz',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mupaduw/deluge-gui',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
