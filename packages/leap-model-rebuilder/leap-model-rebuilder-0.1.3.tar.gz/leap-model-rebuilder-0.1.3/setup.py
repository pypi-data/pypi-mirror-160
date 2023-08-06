# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['leap_model_rebuilder']

package_data = \
{'': ['*']}

install_requires = \
['protobuf>=3.19.4,<4.0.0']

extras_require = \
{':platform_machine == "arm64"': ['tensorflow-macos==2.8.0'],
 ':platform_machine == "x86_64"': ['tensorflow==2.8.0']}

setup_kwargs = {
    'name': 'leap-model-rebuilder',
    'version': '0.1.3',
    'description': '',
    'long_description': '# leap-model-rebuilder\nKeras model rebuilder tool for model rebuilding with alterations\n',
    'author': 'dorhar',
    'author_email': 'doron.harnoy@tensorleap.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tensorleap/leap-model-rebuilder',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
