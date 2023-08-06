# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['timezones']

package_data = \
{'': ['*']}

install_requires = \
['pytz']

extras_require = \
{'geoip': ['geoip2>=4.5.0,<5.0.0']}

setup_kwargs = {
    'name': 'timezones',
    'version': '2.1.0',
    'description': "A Python library that provides better selection of common timezones, can output HTML and auto select the best timezone based on user's IP.",
    'long_description': "python-timezones\n----------------\n\n![](https://github.com/Doist/python-timezones/workflows/Tests/badge.svg)\n\nA Python library that provides better selection of common timezones,\ncan output HTML and auto select the best timezone based on user's IP.\n\nVisit https://doist.github.io/python-timezones/ for more information.\n\nCopyright: 2012-2022 by Doist\nLicense: MIT.\n",
    'author': 'Doist Developers',
    'author_email': 'dev@doist.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://doist.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
