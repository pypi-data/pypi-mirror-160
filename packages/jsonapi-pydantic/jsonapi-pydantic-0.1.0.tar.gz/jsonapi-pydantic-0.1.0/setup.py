# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jsonapi_pydantic', 'jsonapi_pydantic.v1_0', 'jsonapi_pydantic.v1_0.resource']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.9.1,<2.0.0']

setup_kwargs = {
    'name': 'jsonapi-pydantic',
    'version': '0.1.0',
    'description': 'JSON:API implementation with pydantic.',
    'long_description': '# jsonapi-pydantic\n',
    'author': 'impocode',
    'author_email': 'impocode@impocode.com',
    'maintainer': 'impocode',
    'maintainer_email': 'impocode@impocode.com',
    'url': 'https://github.com/impocode/jsonapi-pydantic',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
