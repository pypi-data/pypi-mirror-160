# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zdppy_requests',
 'zdppy_requests.libs',
 'zdppy_requests.libs.certifi',
 'zdppy_requests.libs.charset_normalizer',
 'zdppy_requests.libs.charset_normalizer.assets',
 'zdppy_requests.libs.charset_normalizer.cli',
 'zdppy_requests.libs.idna',
 'zdppy_requests.libs.urllib3',
 'zdppy_requests.libs.urllib3.contrib',
 'zdppy_requests.libs.urllib3.contrib._securetransport',
 'zdppy_requests.libs.urllib3.packages',
 'zdppy_requests.libs.urllib3.packages.backports',
 'zdppy_requests.libs.urllib3.util']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'zdppy-requests',
    'version': '0.1.2',
    'description': '发送HTTP请求的库',
    'long_description': None,
    'author': 'zhangdapeng',
    'author_email': 'pygosuperman@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
