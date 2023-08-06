# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['strawman']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.17.3,<2.0.0', 'pandas>=1.3.0,<2.0.0']

extras_require = \
{'docs': ['Sphinx>=5.0.0,<6.0.0', 'insegel>=1.3.1,<2.0.0']}

setup_kwargs = {
    'name': 'strawman',
    'version': '0.1.0',
    'description': 'Library for simple dummy dataframes',
    'long_description': '<p align="center">\n<img src="https://github.com/dobraczka/strawman/raw/main/docs/strawman.png" alt="strawman logo", width=200/>\n<h2 align="center"> strawman</h2>\n</p>\n\n\n<p align="center">\n<a href="https://github.com/dobraczka/strawman/actions/workflows/main.yml"><img alt="Actions Status" src="https://github.com/dobraczka/strawman/actions/workflows/main.yml/badge.svg?branch=main"></a>\n<a href=\'https://strawman.readthedocs.io/en/latest/?badge=latest\'><img src=\'https://readthedocs.org/projects/strawman/badge/?version=latest\' alt=\'Documentation Status\' /></a>\n<a href="https://codecov.io/gh/dobraczka/strawman"><img src="https://codecov.io/gh/dobraczka/strawman/branch/main/graph/badge.svg"/></a>\n<a href="https://pypi.org/project/strawman"/><img alt="Stable python versions" src="https://img.shields.io/pypi/pyversions/strawman"></a>\n<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>\n</p>\n\nUsage\n=====\n\nCreate a dummy DataFrame:\n\n```python\n    >>> from strawman import dummy_df\n    >>> dummy_df((5,3))\n             0    1    2\n    0  Ass  wEB  jEx\n    1  xxD  TtW  Xzs\n    2  ITh  mpj  tgy\n    3  rgN  ZyW  kzR\n    4  FPO  XiY  ARn\n```\n\nOr create a triples DataFrame:\n\n```python\n    >>> from strawman import dummy_triples\n    >>> dummy_triples(5)\n      head relation tail\n    0   e2     rel0   e1\n    1   e1     rel0   e0\n    2   e1     rel0   e2\n    3   e0     rel0   e2\n    4   e1     rel1   e0\n```\n\nInstallation\n============\n\nVia pip:\n\n```bash\npip install strawman\n```\n',
    'author': 'Daniel Obraczka',
    'author_email': 'obraczka@informatik.uni-leipzig.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dobraczka/strawman',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
