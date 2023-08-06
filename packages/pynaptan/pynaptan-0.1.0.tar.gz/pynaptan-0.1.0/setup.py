# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pynaptan']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.0,<0.24.0', 'pydantic>=1.9.1,<2.0.0']

setup_kwargs = {
    'name': 'pynaptan',
    'version': '0.1.0',
    'description': 'Python package for naptan',
    'long_description': '# pynaptan\n\n',
    'author': 'Ciaran McCormick',
    'author_email': 'ciaranmccormick@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ciaranmccormick/pynaptan',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
