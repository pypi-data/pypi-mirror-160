# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['certbot_aws_store']

package_data = \
{'': ['*']}

install_requires = \
['argparse>=1.4.0,<2.0.0',
 'certbot-route53>=0.2.0,<0.3.0',
 'certbot>=1.29.0,<2.0.0',
 'compose-x-common>=1.0.4,<2.0.0',
 'pyOpenSSL>=22.0.0,<23.0.0',
 'pynamodb>=5.2.1,<6.0.0']

entry_points = \
{'console_scripts': ['certbot-aws-store = '
                     'certbot_aws_store.cli:cli_entrypoint']}

setup_kwargs = {
    'name': 'certbot-aws-store',
    'version': '0.1.0',
    'description': "Generate Let's Encrypt certificates and store into AWS",
    'long_description': None,
    'author': 'John Preston',
    'author_email': 'john@ews-network.net',
    'maintainer': 'John Preston',
    'maintainer_email': 'john@ews-network.net',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
