# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['truss',
 'truss.contexts',
 'truss.contexts.image_builder',
 'truss.contexts.local_loader',
 'truss.local',
 'truss.model_frameworks',
 'truss.templates',
 'truss.templates.custom.model',
 'truss.templates.huggingface_transformer.model',
 'truss.templates.keras.model',
 'truss.templates.lightgbm.model',
 'truss.templates.pytorch.model',
 'truss.templates.server',
 'truss.templates.server.common',
 'truss.templates.sklearn.model',
 'truss.templates.xgboost.model',
 'truss.tests',
 'truss.tests.contexts.local_loader',
 'truss.tests.local',
 'truss.tests.model_frameworks',
 'truss.tests.templates.core.server',
 'truss.tests.templates.core.server.common']

package_data = \
{'': ['*'],
 'truss': ['test_data/*'],
 'truss.templates': ['custom/*',
                     'docs/*',
                     'huggingface_transformer/*',
                     'keras/*',
                     'lightgbm/*',
                     'pytorch/*',
                     'sklearn/*',
                     'xgboost/*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'PyYAML>=6.0,<7.0',
 'msgpack-numpy>=0.4.7.1',
 'msgpack>=1.0.2',
 'numpy>=1.18',
 'packaging>=20.9,<21.0',
 'python-json-logger>=2.0.2',
 'python-on-whales>=0.46.0,<0.47.0',
 'tenacity>=8.0.1,<9.0.0']

entry_points = \
{'console_scripts': ['truss = truss.cli:cli_group']}

setup_kwargs = {
    'name': 'truss',
    'version': '0.0.29',
    'description': '',
    'long_description': None,
    'author': 'Pankaj Gupta',
    'author_email': 'pankaj@baseten.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
