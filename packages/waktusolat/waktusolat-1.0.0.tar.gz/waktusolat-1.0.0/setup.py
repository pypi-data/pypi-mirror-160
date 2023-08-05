# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['waktusolat']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'waktusolat',
    'version': '1.0.0',
    'description': 'Prayer times API wrapper',
    'long_description': '# python-waktu-solat\nA simple API wrapper for [waktu-solat-api](https://zaimramlan.github.io/waktu-solat-api/). (Malaysia only)\n\n# Installation\n```sh\npip install waktusolat\n```\n\n# Basic usage\nList all states:\n```python\nfrom waktusolat import WaktuSolat\n\nclient = WaktuSolat()\nprint(client.states())\n```\n\nList all zones:\n```python\nfrom waktusolat import WaktuSolat\n\nclient = WaktuSolat()\nprint(client.zones())\n```\n\nList all prayer times:\n```python\nfrom waktusolat import WaktuSolat\n\nclient = WaktuSolat()\nprint(client.prayer_times())\n```\n\n# License\n[MIT](./LICENSE)\n',
    'author': 'sypleks',
    'author_email': 'adamshafiq2008@outlook.com',
    'maintainer': 'sypleks',
    'maintainer_email': 'adamshafiq2008@outlook.com',
    'url': 'https://github.com/sypleks/python-waktu-solat',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
