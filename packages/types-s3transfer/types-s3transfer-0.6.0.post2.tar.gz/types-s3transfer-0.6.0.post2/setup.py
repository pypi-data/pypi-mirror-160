# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['s3transfer-stubs']

package_data = \
{'': ['*']}

install_requires = \
['pip']

setup_kwargs = {
    'name': 'types-s3transfer',
    'version': '0.6.0.post2',
    'description': 'Type annotations and code completion for s3transfer',
    'long_description': '# types-s3transfer\n\n[![PyPI - types-s3transfer](https://img.shields.io/pypi/v/types-s3transfer.svg?color=blue)](https://pypi.org/project/types-s3transfer)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/types-s3transfer.svg?color=blue)](https://pypi.org/project/types-s3transfer)\n[![PyPI - Downloads](https://img.shields.io/pypi/dm/types-s3transfer?color=blue)](https://pypistats.org/packages/types-s3transfer)\n\n![boto3.typed](https://github.com/youtype/mypy_boto3_builder/raw/main/logo.png)\n\nType annotations and code completion for [s3transfer](https://pypi.org/project/s3transfer/) package.\nThis package is a part of [mypy_boto3_builder](https://github.com/youtype/mypy_boto3_builder) project.\n\n## Installation\n\n```bash\npython -m pip install types-s3transfer\n```\n\n## Usage\n\nUse [mypy](https://github.com/python/mypy) or [pyright](https://github.com/microsoft/pyright) for type checking.\n\n### Latest changes\n\nBuilder changelog can be found in [Releases](https://github.com/youtype/mypy_boto3_builder/releases).\n\n## Versioning\n\n`types-s3transfer` version is the same as related `s3transfer` version and follows\n[PEP 440](https://www.python.org/dev/peps/pep-0440/) format.\n\n## Support and contributing\n\nPlease reports any bugs or request new features in\n[mypy-boto3-builder](https://github.com/youtype/mypy_boto3_builder/issues/) repository.\n',
    'author': 'Vlad Emelianov',
    'author_email': 'vlad.emelianov.nz@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://youtype.github.io/mypy_boto3_builder/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
