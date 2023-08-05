# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xfers_sdk',
 'xfers_sdk.models',
 'xfers_sdk.models.balance',
 'xfers_sdk.models.balance.entity',
 'xfers_sdk.models.bank',
 'xfers_sdk.models.bank.entity',
 'xfers_sdk.models.disbursements',
 'xfers_sdk.models.disbursements.entity',
 'xfers_sdk.models.payment',
 'xfers_sdk.models.payment.entity',
 'xfers_sdk.models.payment_link',
 'xfers_sdk.models.payment_link.entity',
 'xfers_sdk.models.payment_methods',
 'xfers_sdk.models.payment_methods.entity',
 'xfers_sdk.network']

package_data = \
{'': ['*']}

install_requires = \
['dacite>=1.6.0,<2.0.0', 'pyhumps>=3.5.3,<4.0.0', 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'xfers-sdk',
    'version': '1.0',
    'description': '',
    'long_description': None,
    'author': 'LandX Engineering',
    'author_email': 'tech@landx.id',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
