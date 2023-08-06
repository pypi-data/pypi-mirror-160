# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['qlient', 'qlient.core', 'qlient.core.schema']

package_data = \
{'': ['*']}

install_requires = \
['importlib-metadata>=4.11.4,<5.0.0']

setup_kwargs = {
    'name': 'qlient-core',
    'version': '1.0.0',
    'description': 'The core for a blazingly fast and modern graphql client designed with simplicity in mind.',
    'long_description': '# Qlient Core: Python GraphQL Client Core Library\n\n[![DeepSource](https://deepsource.io/gh/qlient-org/python-qlient-core.svg/?label=active+issues&token=B71TvEVbDX-5GynnxfPlumBi)](https://deepsource.io/gh/qlient-org/python-qlient-core/?ref=repository-badge)\n[![DeepSource](https://deepsource.io/gh/qlient-org/python-qlient-core.svg/?label=resolved+issues&token=B71TvEVbDX-5GynnxfPlumBi)](https://deepsource.io/gh/qlient-org/python-qlient-core/?ref=repository-badge)\n[![pypi](https://img.shields.io/pypi/v/qlient-core.svg)](https://pypi.python.org/pypi/qlient-core)\n[![versions](https://img.shields.io/pypi/pyversions/qlient-core.svg)](https://github.com/qlient-org/python-qlient-core)\n[![license](https://img.shields.io/github/license/qlient-org/python-qlient-core.svg)](https://github.com/qlient-org/python-qlient-core/blob/master/LICENSE)\n\nThis is the core for a blazingly fast and modern graphql client that was designed with simplicity in mind.\n\n## Help\n\nSee the [documentation](https://qlient-org.github.io/python-qlient-core/site/) for more details.\n\n## Quick Preview\n\n```python\nfrom qlient.core import Client, Backend, GraphQLResponse\n\n\nclass MyBackend(Backend):\n    """Must be implemented by you"""\n\n\nclient = Client(MyBackend())\n\nres: GraphQLResponse = client.query.get_my_thing("name")\n\nprint(res.request.query)  # "query get_my_thing { get_my_thing { name } }"\n```',
    'author': 'Daniel Seifert',
    'author_email': 'info@danielseifert.ch',
    'maintainer': 'Daniel Seifert',
    'maintainer_email': 'info@danielseifert.ch',
    'url': 'https://qlient-org.github.io/python-qlient-core/site/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
