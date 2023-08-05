# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['network3_medusa']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'click>=8.1.3,<9.0.0',
 'hedera-sdk-py>=2.16.3,<3.0.0',
 'requests>=2.28.1,<3.0.0']

entry_points = \
{'console_scripts': ['network3_medusa = network3_medusa.script:run']}

setup_kwargs = {
    'name': 'network3-medusa',
    'version': '1.0.39',
    'description': '',
    'long_description': None,
    'author': 'John Capobianco',
    'author_email': 'ptcapo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
