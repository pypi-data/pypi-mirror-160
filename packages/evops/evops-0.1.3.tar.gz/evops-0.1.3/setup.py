# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['evops', 'evops.metrics', 'evops.utils']

package_data = \
{'': ['*']}

install_requires = \
['importlib-metadata==4.8.3',
 'importlib-resources>=5.7.1,<6.0.0',
 'nptyping>=1.4.4,<2.0.0',
 'numpy>=1.19.0,<2.0.0']

setup_kwargs = {
    'name': 'evops',
    'version': '0.1.3',
    'description': 'Evaluation of Plane Segmentation.',
    'long_description': None,
    'author': 'Pavel Mokeev',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
