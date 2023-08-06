# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['excelerate']

package_data = \
{'': ['*']}

install_requires = \
['openpyxl>=3.0.10,<4.0.0']

setup_kwargs = {
    'name': 'excelerate',
    'version': '0.1.0',
    'description': 'Easily generate beautiful excel reports in python',
    'long_description': '# Excelerate\n\nAccelerate your project with beautiful excel reports\n',
    'author': 'Yosi Frost',
    'author_email': 'yosi_frost@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/FrostyTheSouthernSnowman/excelerate',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
