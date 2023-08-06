# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['color_scheme_utils']

package_data = \
{'': ['*']}

install_requires = \
['stringcase>=1.2.0,<2.0.0']

entry_points = \
{'console_scripts': ['kitty-conf-extract-theme = '
                     'color_scheme_utils.kitty_conf_extract_theme:main']}

setup_kwargs = {
    'name': 'color-scheme-utils',
    'version': '0.1.1',
    'description': '',
    'long_description': '',
    'author': 'Teddy Xinyuan Chen',
    'author_email': '45612704+tddschn@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tddschn/color-scheme-utils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
