# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['rectools',
 'rectools.dataset',
 'rectools.metrics',
 'rectools.model_selection',
 'rectools.models',
 'rectools.tools',
 'rectools.utils']

package_data = \
{'': ['*']}

install_requires = \
['Markdown>=3.2,<3.3',
 'attrs>=19.1.0,<22.0.0',
 'implicit==0.4.4',
 'lightfm>=1.16,<2.0',
 'nmslib>=2.0.4,<3.0.0',
 'numpy>=1.19.5,<2.0.0',
 'pandas>=0.25.3,<2.0.0',
 'scipy>=1.5.4,<2.0.0',
 'tqdm>=4.27.0,<5.0.0',
 'typeguard>=2.0.1,<3.0.0']

extras_require = \
{'all': ['torch>=1.6,<2.0', 'pytorch-lightning>=1.6,<2.0'],
 'nn': ['torch>=1.6,<2.0', 'pytorch-lightning>=1.6,<2.0']}

setup_kwargs = {
    'name': 'rectools',
    'version': '0.0.3',
    'description': 'An easy-to-use Python library for building recommendation systems',
    'long_description': '# RecTools',
    'author': 'Daniil Potapov',
    'author_email': 'mars-team@mts.ru',
    'maintainer': 'Daniil Potapov',
    'maintainer_email': 'mars-team@mts.ru',
    'url': 'https://github.com/MobileTeleSystems/RecTools',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.1,<3.10.0',
}


setup(**setup_kwargs)
