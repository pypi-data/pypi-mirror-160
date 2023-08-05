# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jsonc']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'json-with-comments',
    'version': '1.0.0',
    'description': 'JSON with Comments for Python',
    'long_description': '# JSON with Comments for Python\n\n## Features\n* Remove single line (`//`) and block comments (`/* */`)\n* Remove trailing commas from arrays and objects\n\n## Usage\n\n```py\nimport jsonc\n```\nAnd just like `json` module\n',
    'author': 'Takumasa Nakamura',
    'author_email': 'n.takumasa@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/n-takumasa/json-with-comments',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
