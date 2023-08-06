# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['hsmap']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.22', 'python-dateutil>=2.8.2']

setup_kwargs = {
    'name': 'hsmap',
    'version': '0.1.6',
    'description': 'Python Utils for Hsmap project.',
    'long_description': '# Hsmap Utils\n\nPython Hsmap Utils.',
    'author': 'someone',
    'author_email': 'some@hsmap.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/hsmap',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2',
}


setup(**setup_kwargs)
