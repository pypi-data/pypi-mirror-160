# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rsa']

package_data = \
{'': ['*']}

install_requires = \
['pyasn1>=0.1.3']

entry_points = \
{'console_scripts': ['pyrsa-decrypt = rsa.cli:decrypt',
                     'pyrsa-encrypt = rsa.cli:encrypt',
                     'pyrsa-keygen = rsa.cli:keygen',
                     'pyrsa-priv2pub = rsa.util:private_to_public',
                     'pyrsa-sign = rsa.cli:sign',
                     'pyrsa-verify = rsa.cli:verify']}

setup_kwargs = {
    'name': 'rsa',
    'version': '4.9',
    'description': 'Pure-Python RSA implementation',
    'long_description': '# Pure Python RSA implementation\n\n[![PyPI](https://img.shields.io/pypi/v/rsa.svg)](https://pypi.org/project/rsa/)\n[![Build Status](https://travis-ci.org/sybrenstuvel/python-rsa.svg?branch=master)](https://travis-ci.org/sybrenstuvel/python-rsa)\n[![Coverage Status](https://coveralls.io/repos/github/sybrenstuvel/python-rsa/badge.svg?branch=master)](https://coveralls.io/github/sybrenstuvel/python-rsa?branch=master)\n[![Code Climate](https://api.codeclimate.com/v1/badges/a99a88d28ad37a79dbf6/maintainability)](https://codeclimate.com/github/codeclimate/codeclimate/maintainability)\n\n[Python-RSA](https://stuvel.eu/rsa) is a pure-Python RSA implementation. It supports\nencryption and decryption, signing and verifying signatures, and key\ngeneration according to PKCS#1 version 1.5. It can be used as a Python\nlibrary as well as on the commandline. The code was mostly written by\nSybren A.  Stüvel.\n\nDocumentation can be found at the [Python-RSA homepage](https://stuvel.eu/rsa). For all changes, check [the changelog](https://github.com/sybrenstuvel/python-rsa/blob/master/CHANGELOG.md).\n\nDownload and install using:\n\n    pip install rsa\n\nor download it from the [Python Package Index](https://pypi.org/project/rsa/).\n\nThe source code is maintained at [GitHub](https://github.com/sybrenstuvel/python-rsa/) and is\nlicensed under the [Apache License, version 2.0](https://www.apache.org/licenses/LICENSE-2.0)\n\n## Security\n\nBecause of how Python internally stores numbers, it is very hard (if not impossible) to make a pure-Python program secure against timing attacks. This library is no exception, so use it with care. See https://securitypitfalls.wordpress.com/2018/08/03/constant-time-compare-in-python/ for more info.\n\n## Setup of Development Environment\n\n```\npython3 -m venv .venv\n. ./.venv/bin/activate\npip install poetry\npoetry install\n```\n\n## Publishing a New Release\n\nSince this project is considered critical on the Python Package Index,\ntwo-factor authentication is required. For uploading packages to PyPi, an API\nkey is required; username+password will not work.\n\nFirst, generate an API token at https://pypi.org/manage/account/token/. Then,\nuse this token when publishing instead of your username and password.\n\nAs username, use `__token__`.\nAs password, use the token itself, including the `pypi-` prefix.\n\nSee https://pypi.org/help/#apitoken for help using API tokens to publish. This\nis what I have in `~/.pypirc`:\n\n```\n[distutils]\nindex-servers =\n    rsa\n\n# Use `twine upload -r rsa` to upload with this token.\n[rsa]\n  repository = https://upload.pypi.org/legacy/\n  username = __token__\n  password = pypi-token\n```\n\n```\n. ./.venv/bin/activate\npip install twine\n\npoetry build\ntwine check dist/rsa-4.9.tar.gz dist/rsa-4.9-*.whl\ntwine upload -r rsa dist/rsa-4.9.tar.gz dist/rsa-4.9-*.whl\n```\n\nThe `pip install twine` is necessary as Python-RSA requires Python >= 3.6, and\nTwine requires at least version 3.7. This means Poetry refuses to add it as\ndependency.\n',
    'author': 'Sybren A. Stüvel',
    'author_email': 'sybren@stuvel.eu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://stuvel.eu/rsa',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4',
}


setup(**setup_kwargs)
