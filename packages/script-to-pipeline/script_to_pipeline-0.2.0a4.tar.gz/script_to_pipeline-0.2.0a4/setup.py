# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['script_to_pipeline', 'script_to_pipeline.entrypoint']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['script_to_pipeline = script_to_pipeline.__main__:main']}

setup_kwargs = {
    'name': 'script-to-pipeline',
    'version': '0.2.0a4',
    'description': 'Tool for converting python scripts into Pachyderm pipelines.',
    'long_description': None,
    'author': 'Ben Bonenfant',
    'author_email': 'bonenfan5ben@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
